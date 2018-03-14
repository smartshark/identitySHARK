import sys
import timeit

from mongoengine import connect
from pycoshark.mongomodels import Identity
from pycoshark.utils import create_mongodb_uri_string

start_time = timeit.default_timer()

user = ''
password = ''
host = ''
port = ''
authentication_db = ''
database = ""
ssl_enabled = None

uri = create_mongodb_uri_string(user, password, host, port, authentication_db, ssl_enabled)
connect(database, host=uri)

print("fetching identities...")
# identities = list(Identity.objects[:200000])
identities = list(Identity.objects.all())
print("%s identities found" % len(identities))
peopleset = set()
for identity in identities:
    people = tuple(sorted(list(identity.people)))
    if len(people) > 2:
        print("found identity with more than two people: ", people)
        print("aborting")
        sys.exit()
    peopleset.add(people)

print("%i identities in peopleset" % len(peopleset))

print("deleting current identites")
Identity.objects().delete()

print("creating new identities")
identities_to_store = []
for people in peopleset:
    identity = Identity()
    identity.people = list(people)
    identities_to_store.append(identity)
    if len(identities_to_store) >= 100000:
        # store in between to keep size of inserts under control
        Identity.objects.insert(identities_to_store)
        identities_to_store = []

# store remaining identities
Identity.objects.insert(identities_to_store)

print("done")
elapsed = timeit.default_timer() - start_time
print("Execution time: %0.5f s" % elapsed)
