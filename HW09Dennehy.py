"""HW 9
@author: Ruth Dennehy"""

from prettytable import PrettyTable
import os
from collections import defaultdict

class Org_Repository:
    """ This class opens a directory and uses the "students.txt, instructors,txt, grades.txt" files to create a dictionary of all_students with each key representing the cwid of that instance of the student class. Similarly a dictionary of all_instructors is created with each key representing the cwid of the professor. A table of students is then printed showing the cwid, name, and completed courses. A table of data for the professor is also printed with the cwid, name, department, course taught, and number of students in that course."""

    def __init__(self, dir_path):
        """Open directory and use functions to store data in a dictionary for instructors and students in a dictionary"""
        self.dir_path = dir_path
        
        try:
             os.chdir(dir_path)
        except FileNotFoundError:
            raise FileNotFoundError('Directory {} was not found'.format(dir_path))
        else:
            self.all_students, self.all_instructors = {}, {} #add all students to self so available throughout class

            for (scwid, name, major) in self.file_read("students.txt", 3, "CWID\tName\tMajor"):
                self.all_students[scwid] = Student(scwid, name, major)
            
            for (icwid, name, dept) in self.file_read("instructors.txt", 3, "CWID\tName\tDepartment"):
                self.all_instructors[icwid] = Instructor(icwid, name, dept)
            
            for (scwid, course, grade, icwid) in self.file_read("grades.txt", 4, "Student CWID\tCourse\tLetterGrade\tInstructor CWID"):
                self.all_students[scwid].add_grade(course, grade)
                self.all_instructors[icwid].add_stud_count(course)
            
            self.stud_print()
            self.instruc_print()
    
    def file_read(self, path, num_fields, expected_fields, sep = "\t"):
        """Reads a generic file and generates a tuple of fields for each line in the file"""
        try:
            fp = fp = open (os.path.join(path), "r")
        except:
            print("Can't open{}".format(path))
        else:
            with fp:
                for line in fp:
                    fields = line.strip().split(sep) 
                    if len(fields) == num_fields:
                        yield fields
                    else:
                        raise ValueError("Was exepcting {} number of fields in the format {}".format(num_fields, expected_fields))


    
    def stud_print(self):
        """Will print a table of all student data including: the CWID, name, and courses the students has taken"""
        pt = PrettyTable(field_names =["CWID", "Name", "Completed Courses"])

        for scwid in self.all_students:
            pt.add_row(self.all_students[scwid].info_pt()) 
        # if stud_dict[Letter_Grade] not "":  #if grade isn't empty
            #pt.add_row( [self.all_students[scwid].scwid, self.all_students[scwid].name, sorted(self.all_students[scwid].stud_grades.keys()) ]) 
        
        print("\n")
        print("Student Summary")
        print (pt)
        
    def instruc_print(self):
        """Will print a table of all instructors data including: the CWID, name, department, course taught and number of students in that course"""
        pt = PrettyTable(field_names =["CWID", "Name", "Dept", "Course", "Students"])

        for icwid in self.all_instructors:
            for row in self.all_instructors[icwid].info_instruc():
                pt.add_row (row)

        print("\n")
        print("Instructor Summary")
        print (pt)

        

class Student:
    """This class creates an instance of student including the attributes: CWID, name, major, courses the students has taken, and grades received"""

    __slots__ = ["scwid", "name", "major", "stud_grades"]

    def __init__(self, scwid, name, major): 
        """Creates instance of class student"""
        self.scwid = scwid
        self.name = name
        self.major = major
        self.stud_grades = defaultdict(str)
        
    
    def add_grade(self, course, grade):
        """Adds a course and grade for student"""
        self.stud_grades[course] = grade
    
    def info_pt(self):
        """Returns a row of data for a student including the:  CWID, Name, Completed Courses"""  

        return [self.scwid, self.name, sorted(self.stud_grades.keys())]  


class Instructor:
    """This class creates an instance of instructor including the attributes: CWID, name, dept, courses taught, and number of students in that class"""
     
    __slots__ = ["icwid", "name", "dept", "instruc_dd"]

    def __init__(self, icwid, name, dept): 
        """This function creates instance of class student"""
        self.icwid = icwid
        self.name = name
        self.dept = dept
        self.instruc_dd = defaultdict(int)
    
    def add_stud_count(self, course):
        """This function counts the number of students for each class"""
        self.instruc_dd[course] += 1
    
    def info_instruc(self):
        """Returns a row of data for an instructor based on each class including the:  CWID, Name, Dept, Course, and Number of Students in that course"""  

        for course in self.instruc_dd:
            yield [self.icwid, self.name, self.dept, course, self.instruc_dd[course]]

        """for course in self.all_instructors[icwid].instruc_dd.keys():
                pt.add_row([  self.all_instructors[icwid].icwid, self.all_instructors[icwid].name, self.all_instructors[icwid].dept, course, self.all_instructors[icwid].instruc_dd[course] ]) 
                """

if __name__ == "__main__":
    my_test = Org_Repository ("/Users/rudenn/Desktop/Lab9Test")



   




