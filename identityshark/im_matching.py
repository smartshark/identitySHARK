import heapq
import re

from pyjarowinkler import distance

splits = {
    0: 0.25,
    1: 0.50,
    2: 0.75,
}


def _jaro_winkler(name1, name2):
    try:
        distances = distance.get_jaro_distance(name1, name2, winkler=True, scaling=0.1)
    except:
        distances = 0.0
    return distances


def _common_split(name1, name2):
    if name1 is not None and name2 is not None:
        split_name_1 = name1.split(" ")
        split_name_2 = name2.split(" ")
        size_of_list = len(list(set(split_name_1).intersection(split_name_2)))

        try:
            return splits[size_of_list]
        except Exception:
            return 1.0

    return 0.0


def _name_split(name):
    return len(name.split(" "))


def _list_distance(name1, name2):
    split_name1 = list(set(filter(None, name1.split(" "))))
    split_name2 = list(set(filter(None, name2.split(" "))))
    distances = []
    for el1 in split_name1:
        for el2 in split_name2:
            distances.append(_jaro_winkler(el1, el2))
    return distances


def _two_top_distances(name1, name2):
    if name1 is None or name2 is None:
        return [0.0, 0.0]

    distances = _list_distance(name1, name2)
    top_distances = heapq.nlargest(2, distances)
    if len(top_distances) == 0:
        top_distances = [0.0, 0.0]
    if len(top_distances) == 1:
        top_distances.append(0.0)
    return top_distances


def _normalize_name(name):
    try:
        dsl_name = re.sub(r'([^A-Za-z ])', ' ', re.sub("[(\[].*?[)\]]", "", name).split('@')[0]).strip().lower()
        names = [str(n) for n in re.split("[_,|;\W]+", dsl_name) if n != '']
        normalized_name = ' '.join(names)
    except:
        normalized_name = ""
    return normalized_name


def _email_similarity(email1, email2):

    # either email is None we can return Now
    if not email1 or not email2:
        return False

    if email1 == email2:
        return True

    if email1.lower() == email2.lower():
        return True

    # no numbers and no empty / None after removing numbers
    table = str.maketrans(dict.fromkeys('0123456789'))
    email1 = str(email1).translate(table).lower()
    email2 = str(email2).translate(table).lower()

    # if only @domain.tld is left we can not really match
    if email1.startswith('@') or email2.startswith('@'):
        return False

    if email1 and email2 and email1 == email2:
        return True

    # default is no match
    return False


def prepare_single_data(email_1, name_1, email_2, name_2, frequent_emails):
    normalized_name_1 = _normalize_name(name_1)
    normalized_name_2 = _normalize_name(name_2)

    prefix_1 = _normalize_name(email_1.split('@')[0])
    prefix_2 = _normalize_name(email_2.split('@')[0])

    # only do email matching if they are not frequent
    e1 = False
    s4 = 0.0
    t7 = 0.0
    t8 = 0.0
    if email_1 not in frequent_emails and email_2 not in frequent_emails:
        e1 = _email_similarity(email_1, email_2)
        s4 = _common_split(prefix_2, prefix_1)
        t7 = _two_top_distances(prefix_1, prefix_2)[0]
        t8 = _two_top_distances(prefix_1, prefix_2)[1]

    s3 = 0.0
    t5 = 0.0
    t6 = 0.0
    ns3 = 0
    in1 = 0.0
    if email_1 not in frequent_emails:
        s3 = _common_split(normalized_name_2, prefix_1)
        t5 = _two_top_distances(normalized_name_2, prefix_1)[0]
        t6 = _two_top_distances(normalized_name_2, prefix_1)[1]
        ns3 = _name_split(prefix_1)
        in1 = _jaro_winkler(prefix_1, normalized_name_1)

    s2 = 0.0
    t3 = 0.0
    t4 = 0.0
    ns4 = 0
    in2 = 0.0
    if email_2 not in frequent_emails:
        s2 = _common_split(normalized_name_1, prefix_2)
        t3 = _two_top_distances(normalized_name_1, prefix_2)[0]
        t4 = _two_top_distances(normalized_name_1, prefix_2)[1]
        ns4 = _name_split(prefix_2)
        in2 = _jaro_winkler(prefix_2, normalized_name_2)

    s1 = _common_split(normalized_name_1, normalized_name_2)

    t1 = _two_top_distances(normalized_name_1, normalized_name_2)[0]
    t2 = _two_top_distances(normalized_name_1, normalized_name_2)[1]

    ns1 = _name_split(normalized_name_1)
    ns2 = _name_split(normalized_name_2)

    return e1, s1, s2, s3, s4, t1, t2, t3, t4, t5, t6, t7, t8, ns1, ns2, ns3, ns4, in1, in2
