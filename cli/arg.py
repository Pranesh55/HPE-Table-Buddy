import argparse 

parser = argparse.ArgumentParser(add_help=False,description="thid ihbjkb")

#user type parser
parser.add_argument("--help",help='Help for the particular command',action="store_true")
parser.add_argument('user', help='To login as a student and view the timetable for the given class and section.')
parser.add_argument("--generate",help='Generate timetable for all classes at once.',action="store_true")
parser.add_argument("--standard",help='Specify class in Roman Numerals ranging from I to X.')
parser.add_argument("--section",help='Either "A" or "B".')
parser.add_argument("--subject",help='The specific subject for which the time table is about to be viewed.')


args=parser.parse_args()
print(args.__dict__)


class CLI():
    def __init__(self,args):
        self.args = args
        self.setup()
    def setup(self):

        fcd={
            ('student','standard','section'):self.student_std_section,
            ('student','standard'):self.student_std,
            ('student','help'):self.student_help,
            ('teacher','standard','section'):self.teacher_std_section,
            ('teacher','standard'):self.teacher_std,
            ('teacher','help'):self.teacher_help,
            ('admin','generate'):self.admin_generate,
            ('admin','standard','section'):self.admin_std_section,
            ('admin','standard'):self.admin_std,
            ('admin','help'):self.admin_help
            
        }
        actual_args=sorted(i for i,j in args.__dict__.items() if j and i!='user')
        #print(actual_args)
        for item,func in (fcd.items()):
            #print(item)
            
            if self.args.user==item[0]:
                #print('test')
                if sorted(item[1:])==actual_args:
                    func()
                    break
        else:
            print("Invalid arguments")

    def student_std_section(self):
        print("Student: {}".format(self.args.user))
        print("Class: {}".format(self.args.standard))
        print("Section: {}".format(self.args.section))
    
    def student_std(self):
        print("Student: {}".format(self.args.user))
        print("Class: {}".format(self.args.standard))


    def student_help(self):
        print("Student: {}".format(self.args.user))
        print("Usage:")
        print("student  [standard]   (or)")
        print("student  [standard]  - - section [section]")
        print("[standard] - Specify class in Roman Numerals ranging from I to X.")
        print("[section] - Either 'A' or 'B'")
        print("Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed.")
    
    def teacher_std_section(self):
        print("Teacher: {}".format(self.args.user))
        print("Class: {}".format(self.args.standard))
        print("Section: {}".format(self.args.section))
    
    def teacher_std(self):
        print("Teacher: {}".format(self.args.user))
        print("Class: {}".format(self.args.standard))
    
    def teacher_help(self):
        print("Teacher: {}".format(self.args.user))
        print("Usage:")
        print("teacher  [standard]   (or)")
        print("teacher  [standard]  - - section [section]")
        print("[standard] - Specify class in Roman Numerals ranging from I to X.")
        print("[section] - Either 'A' or 'B'")
        print("Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed.")

    def admin_generate(self):
        print("Admin: {}".format(self.args.user))
        print("Generate timetable for all classes at once.")
    
    def admin_std_section(self):
        print("Admin: {}".format(self.args.user))
        print("Class: {}".format(self.args.standard))
        print("Section: {}".format(self.args.section))
    
    def admin_std(self):
        print("Admin: {}".format(self.args.user))
        print("Class: {}".format(self.args.standard))

    def admin_help(self):
        print("Admin: {}".format(self.args.user))
        print("Usage:")
        print("admin - - generate")
        print("Generates timetables for all the classes at once.")
        print("admin - -standard [standard] - -section [section]")
        print("[standard] - Specify class in Roman Numerals ranging from I to X.")
        print("[section] - Either 'A' or 'B'")
        print("Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed.")
    

    

obj = CLI(args)

# if args.user == 'student':
#     if args.standard and args.section:
#         print("Section timetable")
#     if args.standard and not args.section:
#         print("Standard timetable")
#     if args.section and not args.standard:
#         print("Invalid format")
    
# if args.user == 'admin':
#     if args.generate:
#         print("Generating timetable for all classes at once.")
#     if args.standard and not (args.section or args.generate):
#         print(f"timetable for {args.standard}")
#     if args.standard and args.section and not args.generate:
#         print(f"{args.standard} - {args.section}")
#     if args.section and not args.standard and not args.generate:
#         print("Invalid format")
        

# if args.user == 'teacher':
#     #show timetable with respect to subject
#     if not args.subject:
#         print("enter subject")
#     if args.subject and args.standard and args.section:
#         print(f"{args.subject} in {args.standard} - {args.section}")
#     if args.subject and args.standard and not args.section:
#         print(f"{args.subject} in {args.standard}")
#     if args.subject and args.section and not args.standard :
#         print("Invalid format")
#     if args.subject and not (args.standard or args.section):
#         print("Invalid format")
    
