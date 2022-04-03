from tabulate import tabulate
from rich.logging import RichHandler
import logging
from collections import defaultdict

from db import DBHelper
import argparse
import sys

sys.path.append("..")
from timetable_generator.backtrack import generate as timetable_generator

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

LOG = logging.getLogger("table_buddy.cli")


# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
header_mapper = {
    "day": "Day",
    "p_1": "Period 1",
    "p_2": "Period 2",
    "p_3": "Period 3",
    "p_4": "Period 4",
    "p_5": "Period 5",
    "p_6": "Period 6",
}

db_helper = DBHelper()


class CLI:
    def __init__(self, args):
        self.args = args
        self.setup()

    def setup(self):

        fcd = {
            ("student", "standard", "section"): self.student_std_section,
            ("student", "help"): self.student_help,
            ("teacher", "subject", "standard"): self.teacher_sub_std,
            ("teacher", "help"): self.teacher_help,
            ("admin", "generate"): self.admin_generate,
            ("admin", "standard", "section"): self.admin_std_section,
            ("admin", "standard"): self.admin_std,
            ("admin", "help"): self.admin_help,
        }
        actual_args = sorted(i for i, j in args.__dict__.items() if j and i != "user")
        for item, func in fcd.items():
            if self.args.user == item[0]:
                if sorted(item[1:]) == actual_args:
                    func()
                    break
        else:
            print("Invalid arguments")

    def student_std_section(self):
        self.admin_std_section()

    def student_std(self):
        self.admin_std()

    def student_help(self):
        """
        student - To login as a student and view the timetable for the given class and section.

        Usage:

        tablebuddy student  - -help
		    Displays the usage of the command

        tablebuddy student  <standard> <section>
			
        standard - Specify class in Roman Numerals ranging from I to X.

        section - Either 'A' or 'B'

        Note: 
            If both `standard` and `section` were not provided the help for `student` command will be executed.

        """
        print(self.student_help.__doc__)

    def teacher_sub_std(self):
        LOG.debug(self.args)
        result = db_helper.getTimeTableStd(self.args.standard)
        LOG.debug(result)
        table = convertToTeacherTimeTable(result, self.args.subject)
        if all(j == "-" for i in table for j in i):
            print("No timetable found for the given subject")
            return
        print("Subject:", self.args.subject)
        print(tabulate(table, headers=tuple(header_mapper.values()), tablefmt="fancy_grid"))

    def teacher_help(self):
        """
        teacher- To login as a teacher and view the timetable for the given subject, class and section.

        Usage:

        tablebuddy teacher  - -help
             Displays the usage of the command

        tablebuddy teacher <standard> <subject_name> 
	
        subject_name - The specific subject for which the time table is about to be viewed.

        standard - Specify class in Roman Numerals ranging from I to X.

        Note: 
            If both `subject_name` and `standard` were not provided the help for `teacher` command will be executed.

        """

        print(self.teacher_help.__doc__)

    def admin_generate(self):
        """Generating admin timetable information"""
        timetable_rows = []
        final_timetable = timetable_generator()
        for class_, timetable in final_timetable.items():
            for day_index, row in enumerate(timetable):
                timetable_rows.append(
                    (*class_, DAYS[day_index], *[period.subject.name for period in row])
                )
        db_helper.generateDB(timetable_rows)
        LOG.info("Sucessfully generated timetable")

    def admin_std_section(self):
        result = db_helper.getTimeTable(self.args.standard, self.args.section)
        table = [[row[i] for i in header_mapper.keys()] for row in result]
        print(f"Class: {self.args.standard}-{self.args.section}")
        print(tabulate(table, headers=tuple(header_mapper.values()), tablefmt="fancy_grid"))

    def admin_std(self):
        result = db_helper.getTimeTableStd(self.args.standard)
        table_a = []
        table_b = []
        for row in result:
            if row["section"] == "A":
                table_a.append([row[i] for i in header_mapper.keys()])
            else:
                table_b.append([row[i] for i in header_mapper.keys()])

        for key, value in {"A": table_a, "B": table_b}.items():
            print(f"Class: {self.args.standard}-{key}")
            print(tabulate(value, headers=tuple(header_mapper.values()), tablefmt="fancy_grid"))
            print()
        # converted = convertToTeacherTimeTable(result, self.args.subject)

    def admin_help(self):
        """
        admin: To login as an admin, generate the timetable for all classes, view the time tables of specific classes and sections.

        Usage:

        tablebuddy admin  - -help
            Displays the usage of the command

        tablebuddy admin - - generate
            Generates timetables for all the classes at once.

        tablebuddy admin - - standard [standard]  - - section [section]
            Displays the timetable of specified [standard] and [section] .

        [standard] - Specify class in Roman Numerals ranging from I to X.

        [section] - Either 'A' or 'B'

        tablebuddy admin - - standard [standard]

        [standard] - Specify class in Roman Numerals ranging from I to X.

        Note: 
            Displays the timetable of both the sections when [section] is not provided. 
            Displays the timetable for a particular section when both [standard] and [section] was provided.
            If just `tablebuddy admin` was given , the help for `admin` command will be executed.

        """
        print(self.admin_help.__doc__)


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        if message.startswith("the following arguments are required"):
            print(
                CLI.student_help.__doc__,
                CLI.teacher_help.__doc__,
                CLI.admin_help.__doc__,
                sep="\n<" + "-" * 100 + ">\n",
            )
        else:
            print("error : " + message + "\n")
            self.print_help()
        sys.exit(2)


parser = ArgumentParser(add_help=False)
# ArgParse Arguments
parser.add_argument(
    "user", help=""
)

if "--help" in sys.argv:
    parser.add_argument("--help", "-h", help="Help for the particular command", action="store_true")
elif "student" == sys.argv[1]:
    parser.add_argument(
    "standard", help="Specify class in Roman Numerals ranging from I to X."
    )
    parser.add_argument("section", help='Either "A" or "B".')

elif "teacher" == sys.argv[1]:
    parser.add_argument(
        "standard", help="Specify class in Roman Numerals ranging from I to X."
    )
    parser.add_argument(
    "subject",
    help="The specific subject for which the time table is about to be viewed.",
    )
else:
    parser.add_argument(
        "--generate", help="Generate timetable for all classes at once.", action="store_true"
    )
    parser.add_argument(
            "--standard","--std", help="Specify class in Roman Numerals ranging from I to X."
        )
    parser.add_argument("--section", "--sec",help='Either "A" or "B".')

args = parser.parse_args()
LOG.debug("Arguments passed %s" % args.__dict__)

# Utils


def convertToTeacherTimeTable(timetable, subject):
    """Convert the given timetable for the teacher's perspective."""
    LOG.debug(timetable)
    columns = ["p_1", "p_2", "p_3", "p_4", "p_5", "p_6"]
    final = [["-"] * 7 for _ in DAYS]
    for index, row in enumerate(timetable):
        print(index)
        final[DAYS.index(row["day"])][0] = row["day"]
        for col in columns:
            if row[col] == subject:
                final[DAYS.index(row["day"])][int(col[-1])] = f"{row['std']}-{row['section']}"
    LOG.debug("Timetable\n %s" % final)
    return final


if __name__ == "__main__":
    CLI(args)

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
