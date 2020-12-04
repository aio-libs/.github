aio-libs organization configuration
===================================

The repository contains default github templates and fixers
for https://github.com/asottile/all-repos


Setup
-----

Install requirements::

   $ pip install -r requirements.txt

Install pre-commit hooks::

   $ pre-commit install

Copy template::

   $ cp all-repos.json.template all-repos.json

and then replace ``$GITHUB_USENAME`` with your github usename
and ``$GITHUB_APIKEY`` with github token
(you can create generate new token at https://github.com/settings/tokens ).

Usage
-----

To change on all repos at once, you should write special "fixer" python script.
You can use existing one in ``fixes/`` directory as template or refer to
https://github.com/asottile/all-repos for details.

When fixer is ready, just run the following::

   $ all-repos-clone
   $ python fixes/your-new-fix.py

To check your changes before create PRs, you can use `--dry-run` option::

   $ python fixes/your-new-fix.py --dry-run
