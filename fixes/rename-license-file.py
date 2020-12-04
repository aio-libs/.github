import argparse
import subprocess
from pathlib import Path
from typing import Optional, Sequence, Set

from all_repos import autofix_lib
from all_repos.config import Config
from all_repos.util import zsplit


def find_repos(config: Config) -> Set[str]:
    return {str(Path(config.output_dir) / repo) for repo in config.get_cloned_repos()}


def apply_fix() -> None:
    # Fix CI config
    path = Path("LICENSE.txt")
    if path.exists():
        newpath = path.rename("LICENSE")
        autofix_lib.run("git", "rm", str(path))
        autofix_lib.run("git", "add", str(newpath))

    filenames_b = zsplit(subprocess.check_output(["git", "ls-files", "-z"]))
    filenames = [f.decode() for f in filenames_b]
    autofix_lib.run("sed", "-i", "s/LICENSE.txt/LICENSE/g", *filenames)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    autofix_lib.add_fixer_args(parser)
    args = parser.parse_args(argv)

    repos, config, commit, autofix_settings = autofix_lib.from_cli(
        args,
        find_repos=find_repos,
        msg="Add Apache 2 licences",
        branch_name="rename-license-file",
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
