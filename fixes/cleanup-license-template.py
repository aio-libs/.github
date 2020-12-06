import argparse
import datetime
import re
from pathlib import Path
from typing import Optional, Sequence, Set

from all_repos import autofix_lib
from all_repos.config import Config
from all_repos.grep import repos_matching


def find_repos(config: Config) -> Set[str]:
    return repos_matching(
        config,
        (r"yyyy", "--", "LICENSE"),
    )


LICENCE_APACHE = """\
Copyright {years} {name}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


LICENCE_APACHE_RE = re.compile(
    r"^\s*Copyright\s+(?P<year>\d{4})(?:\s*[-,]?\s*\d{4})*,?\s+(?P<name>.+)\s*$",
    re.MULTILINE,
)


def new_license(licence: Optional[str]) -> str:
    NAME = "aio-libs collaboration."
    first_year = last_year = datetime.date.today().year
    if licence is not None:
        match = LICENCE_APACHE_RE.search(licence)
        if match is not None:
            first_year = int(match.group("year"))
    if first_year == last_year:
        years = last_year
    else:
        years = f"{first_year}-{last_year}"
    return LICENCE_APACHE.format(years=years, name=NAME)


def apply_fix() -> None:
    # Fix CI config
    path = Path("LICENSE")
    if not path.exists():
        license = None
    else:
        license = path.read_text()

    license2 = new_license(license)
    path.write_text(license2)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    autofix_lib.add_fixer_args(parser)
    args = parser.parse_args(argv)

    repos, config, commit, autofix_settings = autofix_lib.from_cli(
        args,
        find_repos=find_repos,
        msg="Cleanup Apache 2 licence templates, add ASL2 if absent",
        branch_name="cleanup-licence",
    )

    autofix_lib.fix(
        repos,
        apply_fix=apply_fix,
        config=config,
        commit=commit,
        autofix_settings=autofix_settings,
    )
    return 0


if __name__ == "__main__":
    exit(main())
