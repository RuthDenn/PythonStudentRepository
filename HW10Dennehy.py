"""HW 10
@author: Ruth Dennehy"""


class Major_Req: 
    """This class allows an instance of major to be created"""
    #Class Variable 
    valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

    __slots__ = ["major", "required", "elective"]

    def __init__(self, major):
        """Creates instance of major"""
        self.major = major
        self.required = set ()
        self.elective = set ()
    
    def add_required(self, course):
        """Adds required courses to list for specified major"""
        self.required.add(course)

    def add_elective(self, course):
        """Adds elective to list for specified major"""
        self.elective.add(course)
    
    def is_accepted(self, stud_gr):
        """Determines requirements and electives left"""
        accepted_classes = set()
        for course in stud_gr:
            if stud_gr[course] in Major_Req.valid_grades:
                accepted_classes.add(course)
        
        return accepted_classes

    def get_remaining(self, stud_grades):
        """Returns the remaining number of requirements, electives, and the accepted classes"""
        #Stud_grades holds a dictionary of courses and grades for the specific student passed in
        accepted = self.is_accepted(stud_grades)

        #Electives
        temp_elec = accepted.intersection(self.elective)

        if len(temp_elec) >= 1:
            elec= None
        else:
            elec = self.elective


        #Requirements
        req = self.required.difference(accepted) 
        
        return req, elec, accepted

    
    def info_maj(self):
        """Returns info for major table"""
        return [self.major, sorted(self.required), sorted(self.elective)]
