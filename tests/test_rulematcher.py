import unittest
from identityshark.rule_matcher import compare_people, prepare_data


class test_rule_matcher(unittest.TestCase):

    def test_compare_name(self):
        expected_matches  = [("Jane Doe", "jane@doe.com", "Jane Doe (Jira)", "jira@apache.org"),
                             ("Jane Doe1", "jane@doe.com", "Jane234 Doe (Jira)", "jira@apache.org"),
                            ]
        expected_nonmatches = [("Robert (Bobby) Evans", "evans@yahoo-inc.com", "robert", "robert@bull-enterprises.com"),
                               ("Jane Doe", "jane@doe.com", "John Doe (Jira)", "null"),
                               ("Jane Doe", "jane@doe.com", "John Doe (Jira)", None),
                               ("Jane1", "jane1@somecompany.com", "Jane2", "jane2@anothercompany.com"),
                               ("Tom (JIRA)", "jira@apache.org", "Tom","vandenberget@aciworldwide.com"),
                              ]
        frequent_emails = {"jira@apache.org"}

        print("expected matches:")
        mistakes_matches = 0
        for test_tuple in expected_matches:
            person_one = prepare_data("1", test_tuple[0],test_tuple[1], frequent_emails)
            person_two = prepare_data("2", test_tuple[2],test_tuple[3], frequent_emails)
            match = compare_people(person_one, person_two)
            if match>0:
                print("\tmatch (%i): (%s,%s)-(%s,%s)" % (match, test_tuple[0], test_tuple[1], test_tuple[2], test_tuple[3]))
            else:
                mistakes_matches = mistakes_matches+1
                print("\tno match (%i): (%s,%s)-(%s,%s)" % (match,test_tuple[0],test_tuple[1],test_tuple[2],test_tuple[3]))

        print("expected non-matches:")
        mistakes_nonmatches = 0
        for test_tuple in expected_nonmatches:
            person_1 = prepare_data("1", test_tuple[0], test_tuple[1], frequent_emails)
            person_2 = prepare_data("2", test_tuple[2], test_tuple[3], frequent_emails)
            match = compare_people(person_1, person_2)
            if match > 0:
                mistakes_nonmatches = mistakes_nonmatches+1
                print("\tmatch (%i): (%s,%s)-(%s,%s)" % (match, test_tuple[0], test_tuple[1], test_tuple[2], test_tuple[3]))
            else:
                print("\tno match (%i): (%s,%s)-(%s,%s)" % (match,test_tuple[0], test_tuple[1], test_tuple[2], test_tuple[3]))

        self.assertEqual(0,mistakes_nonmatches+mistakes_matches,
                         "%i incorrect non-matches (expected match); %i incorrect matches (expected non-match)" % (mistakes_matches,mistakes_nonmatches))