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
    level="DEBUG",
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


parser = argparse.ArgumentParser(add_help=False)

# ArgParse Arguments
parser.add_argument(
    "--help", help="Help for the particular command", action="store_true")
parser.add_argument(
    "user", help="To login as a student and view the timetable for the given class and section."
)
parser.add_argument(
    "--generate", help="Generate timetable for all classes at once.", action="store_true"
)
parser.add_argument(
    "--standard", "--std", help="Specify class in Roman Numerals ranging from I to X."
)
parser.add_argument("--section", "--sec", help='Either "A" or "B".')
parser.add_argument(
    "--subject", help="The specific subject for which the time table is about to be viewed."
)


args = parser.parse_args()
LOG.debug("Arguments passed %s" % args.__dict__)

# Utils


def convertToTeacherTimeTable(timetable, subject):
    """Convert the given timetable for the teacher's perspective."""
    LOG.debug(timetable)
    columns = ["p_1", "p_2", "p_3", "p_4", "p_5", "p_6"]
    final = [["-"] * 6 for _ in DAYS]
    for row in timetable:
        for col in columns:
            if row[col] == subject:
                final[DAYS.index(row["day"])][int(col[-1]) -
                                              1] = f"{row['std']}-{row['section']}"
    LOG.debug("Timetable\n %s" % final)
    return final


class CLI:
    def __init__(self, args):
        self.args = args
        self.setup()

    def setup(self):

        fcd = {
            ("student", "standard", "section"): self.student_std_section,
            ("student", "standard"): self.student_std,
            ("student", "help"): self.student_help,
            ("teacher", "subject", "standard"): self.teacher_sub_std,
            ("teacher", "help"): self.teacher_help,
            ("admin", "generate"): self.admin_generate,
            ("admin", "standard", "section"): self.admin_std_section,
            ("admin", "standard"): self.admin_std,
            ("admin", "help"): self.admin_help,
        }
        actual_args = sorted(
            i for i, j in args.__dict__.items() if j and i != "user")
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
        print("Student: {}".format(self.args.user))
        print("Usage:")
        print("student  [standard]   (or)")
        print("student  [standard]  - - section [section]")
        print("[standard] - Specify class in Roman Numerals ranging from I to X.")
        print("[section] - Either 'A' or 'B'")
        print(
            "Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed."
        )

    def teacher_sub_std(self):
        LOG.debug(self.args)
        result = db_helper.getTimeTableStd(self.args.standard)
        LOG.debug(result)
        table = convertToTeacherTimeTable(result, self.args.subject)
        if all(j == "-" for i in table for j in i):
            print("No timetable found for the given subject")
            return
        print("Subject:", self.args.subject)
        print(tabulate(table, headers=header_mapper.values(), tablefmt="fancy_grid"))

    def teacher_help(self):
        print("Teacher: {}".format(self.args.user))
        print("Usage:")
        print("teacher  [standard]   (or)")
        print("teacher  [standard]  - - section [section]")
        print("[standard] - Specify class in Roman Numerals ranging from I to X.")
        print("[section] - Either 'A' or 'B'")
        print(
            "Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed."
        )

    def admin_generate(self):
        """Generating admin timetable information"""
        timetable_rows = []
        final_timetable = timetable_generator()
        for class_, timetable in final_timetable.items():
            for day_index, row in enumerate(timetable):
                timetable_rows.append(
                    (*class_, DAYS[day_index], *
                     [period.subject.name for period in row])
                )
        db_helper.generateDB(timetable_rows)
        LOG.info("Sucessfully generated timetable")

    def admin_std_section(self):
        result = db_helper.getTimeTable(self.args.standard, self.args.section)
        table = [[row[i] for i in header_mapper.keys()] for row in result]
        print(f"Class: {self.args.standard}-{self.args.section}")
        print(tabulate(table, headers=header_mapper.values(), tablefmt="fancy_grid"))

    def admin_std(self):
        result = db_helper.getTimeTableStd(self.args.standard)
        table_a = []
        table_b = []
        for row in result:
            if row["section"] == "A":
                table_a.append([row[i] for i in header_mapper.keys()])
            else:
                table_b.append([row[i] for i in header_mapper.keys()])

        print(f"Class: {self.args.standard}-A")
        print(tabulate(table_a, headers=header_mapper.values(), tablefmt="fancy_grid"))
        print()
        print(f"Class: {self.args.standard}-B")
        print(tabulate(table_b, headers=header_mapper.values(), tablefmt="fancy_grid"))
        # converted = convertToTeacherTimeTable(result, self.args.subject)

    def admin_help(self):
        print("""
        COMMAND 3:

admin: To login as an admin, generate the timetable for all classes, view the time tables of specific classes and sections.

Usage:

tablebuddy admin  - -help
		Displays the usage of the command

tablebuddy admin - - generate

Generates timetables for all the classes at once.

tablebuddy admin [standard] [section]

	Displays the timetable of specified [standard] and [section] .

[standard] - Specify class in Roman Numerals ranging from I to X.

[section] - Either ‘A’ or ‘B’

tablebuddy admin [standard]

[standard] - Specify class in Roman Numerals ranging from I to X.


        """)


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
