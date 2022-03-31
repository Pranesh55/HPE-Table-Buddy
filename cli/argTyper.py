from typing import Optional, Tuple

import typer

app = typer.Typer(
    help="""COMMAND 1:

student - To login as a student and view the timetable for the given class and section.

Usage:

student  [standard]  
	
			(or)

student  [standard]  - - section [section]

[standard] - Specify class in Roman Numerals ranging from I to X.

[section] - Either 'A' or 'B'

Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed.

_________________

COMMAND 2:

teacher- To login as a teacher and view the timetable for the given subject, class and section.

Usage:

teacher [subject_name]  [standard]  
	
			(or)

teacher [subject_name]  [standard]   - - section [section]

[subject_name] - The specific subject for which the time table is about to be viewed.

[standard] - Specify class in Roman Numerals ranging from I to X.

[section] - Either 'A' or 'B'

Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed.

_________________

COMMAND 3:

admin: To login as an admin, generate the timetable for all classes, view the time tables of specific classes and sections.


Usage:

admin - - generate

Generates timetables for all the classes at once.

admin - -standard [standard] - -section [section]

[standard] - Specify class in Roman Numerals ranging from I to X.

[section] - Either 'A' or 'B'

admin - - standard [standard]

[standard] - Specify class in Roman Numerals ranging from I to X.

Displays the timetable of both the sections when [section] is not provided. 
"""
)

STANDARDS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
SECTIONS = ["A", "B"]


@app.command()
def student(standard: str, section: Optional[str] = None):
    """ "student - To login as a student and view the timetable for the given class and section.

    Usage:

    student  [standard]

                            (or)

    student  [standard]  - - section [section]

    [standard] - Specify class in Roman Numerals ranging from I to X.

    [section] - Either 'A' or 'B'

    Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed."""
    standard = standard.upper()
    if standard and section:

        section = section.upper()
        if standard not in STANDARDS or section not in SECTIONS:
            typer.echo("Invalid Standard or Section")
            return
        typer.echo(f"Time Table for {standard} - {section}")
        return
    else:
        if standard not in STANDARDS:
            typer.echo("Invalid Standard")
            return
        typer.echo(f"Time Table for {standard}")


@app.command()
def teacher(subject: str, standard: str, section: Optional[str] = None):
    """ "teacher- To login as a teacher and view the timetable for the given subject, class and section.

    Usage:

    teacher [subject_name]  [standard]

                            (or)

    teacher [subject_name]  [standard]   - - section [section]

    [subject_name] - The specific subject for which the time table is about to be viewed.

    [standard] - Specify class in Roman Numerals ranging from I to X.

    [section] - Either 'A' or 'B'

    Note: The - - section flag is optional. If [section] was not provided, the time tables for both the classes are displayed."""
    standard = standard.upper()
    if standard and section:

        section = section.upper()
        if standard not in STANDARDS or section not in SECTIONS:
            typer.echo("Invalid Standard or Section")
            return
        typer.echo(f"Time Table for {subject} in {standard} - {section}")
        return

    else:

        if standard not in STANDARDS:
            typer.echo("Invalid Standard")
            return
        typer.echo(f"Time Table for  {subject} ,{standard} ")


@app.command()
def admin(
    generate: Optional[bool] = None, standard: Optional[str] = None, section: Optional[str] = None
):
    """admin: To login as an admin, generate the timetable for all classes, view the time tables of specific classes and sections.


    Usage:

    admin - - generate

    Generates timetables for all the classes at once.

    admin - -standard [standard] - -section [section]

    [standard] - Specify class in Roman Numerals ranging from I to X.

    [section] - Either 'A' or 'B'

    admin - - standard [standard]

    [standard] - Specify class in Roman Numerals ranging from I to X.

    Displays the timetable of both the sections when [section] is not provided."""
    # Generate function should be called alone, not with any other arguments
    if not (
        (generate and not standard and not section)
        or (standard and section and not generate)
        or (standard and not section and not generate)
    ):
        # if generate and standard and section or generate and section or generate and standard:
        typer.echo(f"Invalid order of parameters")
        return
    if standard and section:
        standard = standard.upper()
        section = section.upper()
        if standard not in STANDARDS:
            typer.echo(f"Invalid Standard")
            return
        if section not in SECTIONS:
            typer.echo(f"Invalid Section")
            return
        typer.echo(f"Time Table for  {standard} - {section} ")
        return
    if standard:
        standard = standard.upper()
        if standard not in STANDARDS:
            typer.echo(f"Invalid Standard")
            return
        typer.echo(f"Time Table for  {standard} ")
        return
    if section:
        section = section.upper()
        if section not in SECTIONS:
            typer.echo(f"Invalid Section")
            return
        typer.echo(f"Please enter standard for section - {section}")
        return
    if generate:

        typer.echo(f"generating timetable now.....")
        return


app()
