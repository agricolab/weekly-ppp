import datetime
from pathlib import Path
from typing import Union, List, Tuple
from subprocess import Popen, PIPE
import time
from unicodedata import normalize

# settings
root = Path(__file__).parent
omit_employees: List[str] = ["test-candidate"]
pr_folder: str = "personal-reports"
# code
def get_current_cw() -> Tuple[int, int]:
    "return the current year and calendarweek"
    return datetime.datetime.now().isocalendar()[0:2]


def collect_employees():
    employees = []
    for f in (root / pr_folder).iterdir():
        if f.is_dir():
            if f.stem in omit_employees:
                print(f"Omitting {f.stem}")
            else:
                employees.append(f.stem)
    return employees


def append_wr(fname: Path):
    dest = build / "weekly-report.md"
    with fname.open("r") as src:
        with dest.open("a") as dest:
            dest.write(f"#[{fname.stem}")
            dest.write(src.read())
            dest.write("\n\pagebreak")


class Weekly:
    build = root / "build"
    header = """\
---
title: Weekly Report {cw}/{year}
date: {compiledate}
output:
    pdf_document:
        toc: true
        number_sections: true
---"""

    def __init__(self, year=None, cw=None):
        self.year, self.cw = get_current_cw()
        if year is not None:
            self.year = year
        if cw is not None:
            self.cw = cw
        self.now = datetime.datetime.now().strftime("%d.%m.%Y at %H:%M:%S")
        self.build.mkdir(exist_ok=True, parents=True)
        self.fname = self.build / f"{self.year}-{self.cw}.md"
        with self.fname.open("w") as f:
            _header = self.header.format(
                year=self.year, cw=self.cw, compiledate=self.now
            )
            f.write(_header)
            f.write("\n\pagebreak\n")

    @classmethod
    def clean_build(cls):
        print("Cleaning build folder")
        for f in cls.build.glob("*"):
            f.unlink()

    def _append(self, fname: Path):
        if fname.suffix != ".md":
            raise ValueError("Only markdown files can be appended.")
        with self.fname.open("a") as dest:
            with fname.open("r") as src:
                employee = " ".join(
                    e.capitalize() for e in fname.parent.name.split("-")
                )
                dest.write(f"# {employee}\n\n")
                # content = src.read()
                # print(content)
                content = src.readlines()
                for line in content:
                    if "#" in line:
                        line = "##" + line.split("#")[-1]
                        line = line.replace("*", "")

                    valid_headers = ["Progress", "Plans", "Problems"]
                    for vh in valid_headers:
                        if line.startswith(vh):
                            print(f'Correcting "{line}" for missing #')
                            line = line.replace("#", "")
                            line = "## " + line

                    line = (
                        normalize("NFKD", line)
                        .encode("ascii", "ignore")
                        .decode("ascii")
                    )
                    dest.write(line)
                dest.write("\n\n\pagebreak\n\n")

    def _missing(self, ename: str):
        with self.fname.open("a") as dest:
            employee = " ".join(e.capitalize() for e in ename.split("-"))
            dest.write(f"# {employee}\n\n")
            dest.write("## Missing")
            dest.write("\n\pagebreak\n\n")

    def _get_employee_weekly(self, ename: str) -> Path:
        """get the filename of the weekly report for a given calendarweek and employee"""
        fname = root / pr_folder / ename / f"{self.year}-{self.cw}.md"
        if fname.exists():
            return fname
        else:
            return None

    def append_employee(self, ename: str):
        print(ename, end="...")
        fname = self._get_employee_weekly(ename)
        if fname is not None:
            print("found")
            self._append(fname)
        else:
            print("missing")
            self._missing(ename)

    def compile(self, suffix: str = "pdf"):
        suffix = "." + suffix
        dest = self.build / f"{self.fname.with_suffix(suffix).name}"
        cmd = [
            "pandoc",
            "--toc",
            str(self.fname),
            "-o",
            str(dest),
            # "--pdf-engine=xelatex",
        ]
        sub = Popen(cmd, stderr=PIPE, stdout=PIPE)
        o, e = sub.communicate()

        if e == b"":
            print(f"Compiled {suffix[1:]} to {dest}")
            print(o.decode())
        else:
            print(e.decode())


# script
if __name__ == "__main__":
    from sys import argv

    employees = collect_employees()
    if argv[1] == "clean":
        Weekly.clean_build()
        print("Cleaned build folder")
        exit(0)
    weekly = Weekly()
    print(f"Current year: {weekly.year:13.0f}")
    print(f"Current calendarweek: {weekly.cw:5.0f}")
    print("Compiling reports for")

    for ename in sorted(employees):
        weekly.append_employee(ename)
    if len(argv) > 1:
        weekly.compile(argv[1])
    else:
        print(
            "Compiled only to markdown for speed. Trigger compilation of pdf manually"
        )
