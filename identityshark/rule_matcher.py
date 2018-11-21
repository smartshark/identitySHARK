import sys
import jellyfish
#from pyjarowinkler import distance

def prepare_data(id, name, email, frequent_emails, bots_names, bots_emails):
    name, is_jira = _normalize_name(name)
    email = _normalize_email(email, frequent_emails)
    is_bot = name in bots_names or email in bots_emails
    return {'id':id,'name':name, 'email':email, 'is_jira':is_jira, 'is_bot':is_bot}


def compare_people(person_one, person_two):
    if person_one['is_bot'] or person_two['is_bot']:
        # never match bots
        return -1
    if (person_one['is_jira'] or person_two['is_jira']) and _match_name(person_one['name'],person_two['name']):
        return 3
    if _match_email(person_one['email'], person_two['email']):
        return 2
    if _match_similarity(person_one['name'], person_one['email'], person_two['name'], person_two['email']):
        return 1

    # return 0 for non-matches
    return 0

def _normalize_name(name):
    # make everything lower case and remove digits
    name = name.lower()
    name = ''.join(c for c in name if not c.isdigit())
    # in case name is an email address, only use part before @
    name = name.split("@")[0]
    # remove punctuation
    for char in ["'", "-"]:
        name = name.replace(char, '')
    # replace split characters with spaces
    for char in ["_","."]:
        name = name.replace(char, ' ')
    # handle JIRA additions
    if "(jira)" in name:
        is_jira = True
        # drop JIRA name additions
        for jirastr in ["(jira)", "(commented)", "(assigned)", "(updated)", "(created)", "(reopened)", "(resolved)"]:
            name = name.replace(jirastr, '')
    else:
        is_jira = False
    # harmonize whitespaces and remove preceeding/trailing whitespaces
    name = ' '.join(name.split())
    return name,is_jira

def _normalize_email(email, frequent_emails):
    if email is not None and (email.lower() in frequent_emails or "@" not in email):
        return None
    return email

def _match_email(email_one, email_two):
    # check if both are real email addresses
    if email_one is None or email_two is None:
        return False
    return email_one.lower()==email_two.lower()

def _match_name(name_one, name_two):
    if len(name_one)==0 or len(name_two)==0 or len(name_one.split(" "))==1 or len(name_two.split(" "))==1:
        return False
    return name_one==name_two

def _split_name(name):
    name_split = name.split(" ")
    if len(name_split) > 1:
        first_name = name_split[0]
        last_name = name_split[-1]
    else:
        first_name = name
        last_name = None
    return first_name,last_name

def _get_email_prefix(email):
    if email is None:
        return None
    prefix = email.split("@")[0]
    if len(prefix)==0:
        prefix = None
    return prefix

def _match_similarity(name_one, email_one, name_two, email_two):
    first_name_one,last_name_one = _split_name(name_one)
    first_name_two, last_name_two = _split_name(name_two)
    prefix_email_one = _get_email_prefix(email_one)
    prefix_email_two = _get_email_prefix(email_two)

    if last_name_one is None or last_name_two is None:
        # allow only matches with defined names
        return False

    ff = jellyfish.jaro_winkler(first_name_one, first_name_two)
    ll = jellyfish.jaro_winkler(last_name_one, last_name_two)
    fl = jellyfish.jaro_winkler(first_name_one, last_name_two)
    lf = jellyfish.jaro_winkler(last_name_one, first_name_two)

    if prefix_email_one is None or prefix_email_two is None:
        ee = 0
    else:
        try:
            ee = jellyfish.jaro_winkler(prefix_email_one, prefix_email_two)
        except:
            print(email_one," ; ", email_two)
            sys.exit(1)

    # rule based matching
    if ff>0.95 and ll>0.95 and ee>0.92:
        return True
    if fl>0.96 and lf>0.96 and ee>0.92:
        return True

    return False