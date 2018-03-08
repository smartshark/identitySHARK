from mongoengine import connect
from pycoshark.mongomodels import Identity
from pycoshark.utils import create_mongodb_uri_string

user = ''
password = ''
host = ''
port = ''
authentication_db = ''
database = "smartshark_test"
ssl_enabled = None

uri = create_mongodb_uri_string(user, password, host, port, authentication_db, ssl_enabled)
connect(database, host=uri)

# Get all identities
identities = list(Identity.objects.all())
for identity in identities:
    # Check if another identity with the same people exist already
    exist_identity = Identity.objects(people__size=len(identity.people), people__all=identity.people).all()
    if len(exist_identity) > 1:
        for found_identity in exist_identity:
            if found_identity.id != identity.id:
                print("Identity %s equals Identity %s" % (identity.id, found_identity.id))
                print("Identity people: %s" % identity.people)
                print("Deleting identity with people: %s" % found_identity.people)
                Identity.objects(id=found_identity.id).delete()
