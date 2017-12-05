import logging
import multiprocessing
import os
import pickle
import timeit

import pandas as pd
from mongoengine import connect, NotUniqueError
from mongoengine.connection import disconnect
from mongoengine.context_managers import switch_db
from pycoshark.mongomodels import People, Identity
from pycoshark.utils import create_mongodb_uri_string

from identityshark.im_matching import prepare_single_data

logger = logging.getLogger("main")


class Worker(multiprocessing.Process):
    def __init__(self, gbtModel, people, frequent_emails, task_queue, cfg, number):
        multiprocessing.Process.__init__(self)
        self.gbtModel = gbtModel
        self.frequent_emails = frequent_emails
        self.task_queue = task_queue
        self.people = people
        self.alias = "worker%s" % number

        uri = create_mongodb_uri_string(cfg.user, cfg.password, cfg.host, cfg.port, cfg.authentication_db,
                                        cfg.ssl_enabled)
        connect(cfg.database, host=uri, alias=self.alias, connect=False)

    def run(self):
        while True:
            person = self.task_queue.get()
            if person is None:
                self.task_queue.task_done()
                break

            with switch_db(Identity, self.alias) as Identity2:
                identity = Identity2()

                # Create a features list which contains a row for each person that the outer persons needs to be
                # compared with
                features = []
                for inner_person in self.people:
                    features.append(prepare_single_data(person.email, person.name, inner_person.email,
                                                        inner_person.name, self.frequent_emails))

                # Go through the results of the algorithm and if the result is 1 (True match) append it to the identity
                # list
                ids = []
                for i, x in enumerate(self.improved_algo_2(features)):
                    if x == 1:
                        ids.append(self.people[i].id)

                # Sort the ids so that the unique of the list field works
                ids.sort()
                identity.people = ids

                # Try to store it, but do not store it if there is already a list with these matches
                try:
                    identity.save()
                except NotUniqueError as e:
                    pass

            self.task_queue.task_done()

    def improved_algo_2(self, features):
        labels = ['e1', 's1', 's2', 's3', 's4', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 'ns1', 'ns2', 'ns3',
                  'ns4', 'in1', 'in2']
        df = pd.DataFrame.from_records(features, columns=labels)
        predicted = self.gbtModel.predict(df)
        return predicted


class IdentitySHARK(object):

    def __init__(self):
        # Load Model
        path_to_model = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gbt_final_model.sav')
        self.gbtModel = pickle.load(open(path_to_model, 'rb'))

    def start(self, cfg):
        logger.setLevel(cfg.get_debug_level())
        start_time = timeit.default_timer()

        # Connect to mongodb
        uri = create_mongodb_uri_string(cfg.user, cfg.password, cfg.host, cfg.port, cfg.authentication_db,
                                        cfg.ssl_enabled)
        connect(cfg.database, host=uri)

        # Get all people
        people = list(People.objects.all().order_by('id'))
        logger.info("Found %d people..." % len(people))
        # get all email addresses with more than 10 occurences
        email_counts = People.objects.aggregate(*[
            {'$group': {'_id': '$email', 'count': {'$sum': 1}}},
            {'$match': {'count': {'$gt': 9}}}
        ])
        frequent_emails = set([c['_id'] for c in email_counts])
        disconnect()

        num_worker = cfg.num_cores
        tasks = multiprocessing.JoinableQueue()
        workers = [Worker(self.gbtModel, people, frequent_emails, tasks, cfg, i) for i in range(0, num_worker)]

        for w in workers:
            w.start()

        for i in people[cfg.start_index:cfg.end_index]:
            tasks.put(i)

        # Poison pill
        for i in range(0, num_worker):
            tasks.put(None)

        tasks.join()
        elapsed = timeit.default_timer() - start_time
        logger.info("Execution time: %0.5f s" % elapsed)
