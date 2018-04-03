"""@author: Ruth Dennehy"""

import os
from prettytable import PrettyTable
from collections import defaultdict
from HW10Dennehy import Major_Req


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
            self.majors = {} #Key: Name of Major Value: Instance of class Major_Req

            #Major Info
            for (major, flag, course) in self.file_read("majors.txt", 3, "major\tflag\tcourse"):
                if major not in self.majors:
                     self.majors[major] = Major_Req(major)

                if (flag == "E"):
                    self.majors[major].add_elective(course)
                elif (flag == "R"):
                    self.majors[major].add_required(course)
                else:
                    raise ValueError ("Flag not recognized, needs to be either R or E")
            
            #Student Info
            for (scwid, name, major) in self.file_read("students.txt", 3, "CWID\tName\tMajor"):
                if major not in self.majors:
                    raise ValueError("Major was not found")
        
                self.all_students[scwid] = Student(scwid, name, major)
            
            #Instructor Info
            for (icwid, name, dept) in self.file_read("instructors.txt", 3, "CWID\tName\tDepartment"):
                self.all_instructors[icwid] = Instructor(icwid, name, dept)
            
            #Go through grade doc
            for (scwid, course, grade, icwid) in self.file_read("grades.txt", 4, "Student CWID\tCourse\tLetterGrade\tInstructor CWID"):
                if scwid in self.all_students:
                    self.all_students[scwid].add_grade(course, grade)
                else:
                    print ("Grade found that does not match student with ID: '{}'".format(scwid))
                
                if icwid in self.all_instructors:
                    self.all_instructors[icwid].add_stud_count(course)
                else:
                    print ("Unknown teacher found with ID: '{}'".format(icwid))

            self.major_print()
            self.stud_print()
            self.instruc_print()
            
    
    def file_read(self, path, num_fields, expected_fields, sep = "\t"):
        """Reads a generic file and generates a tuple of fields for each line in the file"""
        try:
            fp = fp = open (os.path.join(path), "r")
        except IOError:
            raise IOError("Can't open{}".format(path))
        else:
            with fp:
                for line_num, line in enumerate(fp):
                    fields = line.strip().split(sep) 
                    if len(fields) == num_fields:
                        yield fields
                    else:
                        raise ValueError("Was exepcting {} number of fields on line {} in the format {}".format(num_fields, line_num, expected_fields))


    
    def stud_print(self):
        """Will print a table of all student data including: the CWID, name, and courses the students has taken"""
        pt = PrettyTable(field_names =["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"])

        for scwid in self.all_students:
            stud_maj = self.all_students[scwid].major
            this_maj = self.majors[stud_maj]
            req, elec, accept = this_maj.get_remaining(self.all_students[scwid].stud_grades)
            sort_accept = sorted(accept) #didn't work when sorted in add_row?

            if len(req) == 0:
                req = None
            else:
                req = sorted(req)
            
            if elec is not None:
                elec = sorted(elec)
            
            scwid, name, major, courses = self.all_students[scwid].info_pt()

            pt.add_row([scwid, name, major, sort_accept, req, elec]) 
        
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
    
    def major_print(self):
        """Prints a table of majors and related Required and Elective Classes"""
        pt = PrettyTable(field_names =["Dept", "Required", "Electives"])

        for major in self.majors:
            pt.add_row(self.majors[major].info_maj())
        
        print("\n")
        print("Major Requirements Summary")
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

        return [self.scwid, self.name, self.major, sorted(self.stud_grades.keys())]  



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


if __name__ == "__main__":
    my_test = Org_Repository ("/Users/rudenn/Desktop/Lab9Test")
#    my_test = Org_Repository ("/Users/jrr/Downloads/Repository")