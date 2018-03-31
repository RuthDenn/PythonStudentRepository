"""HW 9 Testing
@author: Ruth Dennehy"""

import unittest
from HW09Dennehy import Org_Repository

class RepoTest(unittest.TestCase): 
    """Unit Tests for Lab 9"""

    def test_repo(self):
        """This function has a unit tests for Org_Repository"""
        my_test = Org_Repository("/Users/rudenn/Desktop/Lab9Test")

        self.assertEqual(my_test.all_students["11788"].name, "Fuller, E")
        self.assertEqual(my_test.all_students["11788"].major, "SYEN")
        self.assertEqual(my_test.all_students["11788"].stud_grades, {'SSW 540': 'A'} )
        self.assertEqual(my_test.all_students["11788"].stud_grades["SSW 540"], "A" )
        self.assertEqual(set(my_test.all_students["11714"].stud_grades.keys()), {'SYS 611', 'SYS 645'} )

        self.assertEqual(my_test.all_instructors["98760"].name, "Darwin, C")
        self.assertEqual(my_test.all_instructors["98760"].dept, "SYEN")
        self.assertEqual(str(my_test.all_instructors["98760"].instruc_dd["SYS 645"]), "1")



if __name__ == "__main__":
   unittest.main(exit=False, verbosity=2)