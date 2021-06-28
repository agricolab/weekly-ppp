import datetime
from pathlib import Path
from typing import Union, List, Tuple
from subprocess import Popen, PIPE
import time
from compile import Weekly, collect_employees, root, pr_folder

# script
if __name__ == "__main__":

    from sys import argv

    employees = collect_employees()
    Weekly.clean_build()
    prs = []
    for e in employees:
        emf = root / pr_folder / e
        prs.extend([pr.stem for pr in emf.glob("*.md")])
    for pr in sorted(set(prs)):
        try:
            year, cw = pr.split("-")
            weekly = Weekly(year=int(year), cw=int(cw))
            print(f"Current year: {weekly.year:13.0f}")
            print(f"Current calendarweek: {weekly.cw:5.0f}")
            print("Compiling reports for")
        except Exception as e:
            print(e)
            continue

        for ename in sorted(employees):
            weekly.append_employee(ename)
        if len(argv) > 1 and argv[1] == "pdf":
            weekly.compile()
        else:
            print(
                "Compiled only to markdown for speed. Trigger compilation of pdf manually"
            )
