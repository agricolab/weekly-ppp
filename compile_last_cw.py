import datetime
from pathlib import Path
from typing import Union, List, Tuple
from subprocess import Popen, PIPE
import time
from compile import Weekly, collect_employees


def get_last_cw() -> Tuple[int, int]:
    "return the ear and calendarweek of last week"
    return (
        datetime.datetime.now() - datetime.timedelta(weeks=1)
    ).isocalendar()[0:2]


# script
if __name__ == "__main__":
    from sys import argv

    employees = collect_employees()
    year, cw = get_last_cw()
    if argv[1] == 'clean':
        Weekly.clean_build()
        quit()
    weekly = Weekly(year=year, cw=cw)
    print(f"Valid year: {weekly.year:12.0f}")
    print(f"Last calendarweek: {weekly.cw:5.0f}")
    print("Compiling reports for")

    for ename in sorted(employees):
        weekly.append_employee(ename)
    if len(argv) > 1:
        weekly.compile(argv[1])
    else:
        print(
            "Compiled only to markdown for speed. Trigger compilation of pdf manually"
        )
