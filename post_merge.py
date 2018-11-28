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

identities = list(Identity.objects.all())
print("%s identities found" % len(identities))
peopleset = []
all_existing_people = set()
for i,identity in enumerate(identities):
    if i%1000==0:
        print("%i - current number of identities: %i" % (i,len(peopleset)))
    people = set(identity.people)
    is_existing = people.intersection(all_existing_people)
    if is_existing:
        for i,existing_people in enumerate(peopleset):
            if people.intersection(existing_people):
                peopleset[i] = existing_people.union(people)
    else:
        peopleset.append(people)
    all_existing_people = all_existing_people.union(people)

print("%i identities in peopleset" % len(peopleset))

print("deleting current identities")
Identity.objects().delete()

print("creating merged identities")
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
