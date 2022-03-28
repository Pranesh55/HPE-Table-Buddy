import argparse 

parser = argparse.ArgumentParser()

#user type parser
parser.add_argument('user', help='To login as a student and view the timetable for the given class and section.')
parser.add_argument("--generate",help='Generate timetable for all classes at once.',action="store_true")
parser.add_argument("--standard",help='Specify class in Roman Numerals ranging from I to X.')
parser.add_argument("--section",help='Either "A" or "B".')
parser.add_argument("--subject",help='The specific subject for which the time table is about to be viewed.')


args=parser.parse_args()
print(args.user)
print(args.std)



if args.user == 'student':
    if args.standard and args.section:
        print("Section timetable")
    if args.standard and not args.section:
        print("Standard timetable")
    if args.section and not args.standard:
        print("Invalid format")
    
if args.user == 'admin':
    if args.generate:
        print("Generating timetable for all classes at once.")
    if args.standard and not (args.section or args.generate):
        print(f"timetable for {args.standard}")
    if args.standard and args.section and not args.generate:
        print(f"{args.standard} - {args.section}")
    if args.section and not args.standard and not args.generate:
        print("Invalid format")
        

if args.user == 'teacher':
    #show timetable with respect to subject
    if not args.subject:
        print("enter subject")
    if args.subject and args.standard and args.section:
        print(f"{args.subject} in {args.standard} - {args.section}")
    if args.subject and args.standard and not args.section:
        print(f"{args.subject} in {args.standard}")
    if args.subject and args.section and not args.standard :
        print("Invalid format")
    if args.subject and not (args.standard or args.section):
        print("Invalid format")
    
