import logging
import multiprocessing
import timeit

from mongoengine import connect
from mongoengine.connection import disconnect
from mongoengine.context_managers import switch_db
from pycoshark.mongomodels import People, Identity
from pycoshark.utils import create_mongodb_uri_string

from identityshark.rule_matcher import compare_people,prepare_data

logger = logging.getLogger("main")


class Worker(multiprocessing.Process):
    def __init__(self, people, task_queue, cfg, number, started_tasks, logger):
        multiprocessing.Process.__init__(self)
        self.people = people
        self.task_queue = task_queue
        self.alias = "worker%s" % number
        self.started_tasks = started_tasks
        self.no_people = len(people)
        self.logger = logger
        uri = create_mongodb_uri_string(cfg.user, cfg.password, cfg.host, cfg.port, cfg.authentication_db,
                                        cfg.ssl_enabled)
        connect(cfg.database, host=uri, alias=self.alias, connect=False)

    def run(self):
        while True:
            person = self.task_queue.get()
            if person is None:
                self.task_queue.task_done()
                break
            self.started_tasks.put(1)
            current_progress = self.started_tasks.qsize()
            if current_progress%1000==0:
                self.logger.info("processing person %i/%i" % (current_progress,self.no_people))
            with switch_db(Identity, self.alias) as Identity2:
                identities_to_store = []
                for inner_person in self.people:
                    if person['id']==inner_person['id'] or inner_person['is_bot']:
                        continue
                    match = compare_people(person,inner_person)
                    if match>0:
                        identity = Identity2()
                        identity.people = [person['id'], inner_person['id']]
                        identities_to_store.append(identity)
                if not identities_to_store:
                    identity = Identity2()
                    identity.people = [person['id']]
                    identities_to_store.append(identity)
                Identity2.objects.insert(identities_to_store)
            self.task_queue.task_done()


class IdentitySHARK(object):

    def start(self, cfg):
        logger.setLevel(cfg.get_debug_level())
        start_time = timeit.default_timer()

        # Connect to mongodb
        uri = create_mongodb_uri_string(cfg.user, cfg.password, cfg.host, cfg.port, cfg.authentication_db,
                                        cfg.ssl_enabled)
        connect(cfg.database, host=uri, alias="default")

        # Get all people
        people = list(People.objects.all().order_by('id'))
        logger.info("Found %d people..." % len(people))

        # get all email addresses with more than 10 occurrences
        email_counts = People.objects.aggregate(*[
            {'$group': {'_id': '$email', 'count': {'$sum': 1}}},
            {'$match': {'count': {'$gt': 9}}}
        ])
        frequent_emails = set([c['_id'] for c in email_counts])
        disconnect()

        # use black and whitelist to modify frequent emails
        with open("blacklist_emails.txt") as f:
            blacklist_emails = f.readlines()
        blacklist_emails = set([x.strip() for x in blacklist_emails])
        whitelist_emails = set(cfg.whitelist_emails.split(','))
        print(whitelist_emails)
        print(blacklist_emails)
        frequent_emails = frequent_emails.difference(whitelist_emails)
        frequent_emails = frequent_emails.union(blacklist_emails)

        # prepare data
        people_prepared = []
        for person in people:
            people_prepared.append(prepare_data(person.id, person.name, person.email,frequent_emails))

        # setup worker processes and create tasks
        num_worker = cfg.num_cores
        tasks = multiprocessing.JoinableQueue()
        started_tasks = multiprocessing.Queue()
        workers = [Worker(people_prepared, tasks, cfg, i, started_tasks, logger) for i in range(0, num_worker)]

        for w in workers:
            w.start()

        if cfg.end_index==0 or cfg.end_index>len(people_prepared):
            cfg.end_index = len(people_prepared)
        for i in people_prepared[cfg.start_index:cfg.end_index]:
            tasks.put(i)

        # Poison pill
        for i in range(0, num_worker):
            tasks.put(None)

        tasks.join()
        elapsed = timeit.default_timer() - start_time
        logger.info("Execution time: %0.5f s" % elapsed)
