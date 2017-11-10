import logging
import timeit

from mongoengine import connect

from pycoshark.mongomodels import People, Identity
from pycoshark.utils import create_mongodb_uri_string

logger = logging.getLogger("main")


class IdentitySHARK(object):

    def __init__(self):
        pass

    def start(self, cfg):
        logger.setLevel(cfg.get_debug_level())
        start_time = timeit.default_timer()

        # Connect to mongodb
        uri = create_mongodb_uri_string(cfg.user, cfg.password, cfg.host, cfg.port, cfg.authentication_db,
                                        cfg.ssl_enabled)
        connect(cfg.database, host=uri)

        # Get all people
        people = list(People.objects.all())
        logger.info("Found %d people..." % len(people))

        # Clear identity collection
        Identity.objects.all().delete()

        # Array in which all identities that should be stored are kept
        identities_to_store = []

        # This gives us a speed up, as the function references do not need to be reevaluated each time
        identities_to_store_append = identities_to_store.append

        # Start index is used so that we can exclude some persons from comparison. E.g., if PersonA was
        # already compared with PersonB, we do not need to compare PersonB with PersonA again
        start_index = 1

        # Todo: Could be paralleled easily (using multiprocessing here?)
        for outer_person in people:
            identity = Identity()

            # This gives us a speed up, as the function references do not need to be reevaluated each time
            append_to_identity_list = identity.people.append
            append_to_identity_list(outer_person.id)

            for inner_person in people[start_index:]:

                # Call algorithm, if it returns True, we need to add the persons id
                if self.improved_algorithm(outer_person, inner_person):
                    append_to_identity_list(inner_person.id)

            identities_to_store_append(identity)
            start_index += 1

        # Todo: Check if a person is in multiple lists

        # Insert identities
        if identities_to_store:
            Identity.objects.insert(identities_to_store)

        elapsed = timeit.default_timer() - start_time
        logger.info("Execution time: %0.5f s" % elapsed)

    def improved_algorithm(self, person1, person2):
        name_person1 = person1.name
        email_person1 = person1.email
        name_person2 = person2.name
        email_person2 = person2.email

        return False