# Moving a project into aio-libs

This page describes how an existing project moves into the [aio-libs]
GitHub organization and the [aio-libs organization on PyPI][pypi-org].
It is for the project's maintainer and for the organization owners who
do the move.

aiofastnet was the first project moved this way, in September 2026
([discussion][d55], [migration issues][af-tasks]). The GitHub and PyPI
steps below follow what happened then. The notes on Read the Docs,
removing the old trusted publisher, pending publishers and repositories
owned by another organization come from the GitHub, PyPI and Read the
Docs documentation and have not been tried yet.

## Who does what

- You: whoever owns the project today on GitHub and PyPI.
- A GitHub owner: an owner of the aio-libs GitHub organization. Members
  of aio-libs cannot create repositories in it, so only an owner can
  receive a transferred repository. Inviting you to [aio-libs-limbo]
  needs an owner of that organization, and the move out of it needs
  someone who owns both.
- A PyPI owner: an Owner of the aio-libs organization on PyPI. Only
  Owners can invite people to the organization. Owners and Managers can
  move a project in and manage teams.

Ask in your discussion thread who can help with each part.

## The order, in short

1. You open a thread in the [discussions] and wait until an owner
   agrees.
2. GitHub: you move the repository into aio-libs-limbo, and a GitHub
   owner moves it on into aio-libs.
3. PyPI: you make a PyPI owner an owner of the project, they move the
   project into the organization and invite you, you accept, and they
   give you the Maintainer role.
4. Trusted publishing: a publisher for `aio-libs/<repository>` replaces
   the one for your account.
5. Checks: a release waits for approval and reaches PyPI, and nothing
   links to the old location anymore.

Don't tag a release between steps 2 and 4 unless the new publisher
already exists. Uploads fail until it does.

## Before you start

- Open a thread in the [discussions]. Say what the project is, who will
  maintain it and whether the PyPI project should move too. [#55][d55]
  and [#45][d45] are examples.
- In [#55][bdraco], an organization owner wrote that aio-libs does not
  require political statements, banners or a modified license from any
  project, that plain MIT is fine, and that the [Code of Conduct][coc]
  applies in the project's spaces without covering project content,
  licensing or dependencies.
- After the move, the aio-libs organizations own the repository and the
  PyPI project. You keep administering the repository through a team
  created for the project, and you get the Maintainer role on PyPI. A
  Maintainer can upload releases. Adding collaborators, deleting
  releases and changing trusted publishers need owner access to the
  project.
- Joining that team makes you a member of the aio-libs GitHub
  organization. aio-libs requires two-factor authentication without SMS
  ([#53][d53]), so set it up first. Organization invitations expire
  after seven days.
- Write down who is assigned to which open issues and which third-party
  services the repository uses, such as Read the Docs, Codecov or
  CodSpeed. The move can clear assignees, and those services may need
  to be connected again.

## Why a direct transfer fails

GitHub's rule is: "To transfer a repository that you own to an
organization, you must have permission to create a repository in the
target organization." Members of aio-libs cannot create repositories
there, so for anyone but an owner the transfer fails with "You don't
have the permission to create public repositories on aio-libs".

Adding an owner as a collaborator does not help. A personal repository
can have collaborators, but not a second owner.

## Moving the GitHub repository

[aio-libs-limbo] is a staging organization whose members can create
repositories, so they can transfer repositories into it.

1. An owner of aio-libs-limbo checks in its settings (Member
   privileges) that members can still create public repositories, since
   this route depends on it, and invites you as a member, not an owner.
   Accept the invitation before the next step, or you get the same error
   as above.
2. You [transfer the repository][gh-transfer] to aio-libs-limbo and say
   so in your thread. Don't merge, release or change settings until it
   reaches aio-libs.
3. An owner of both organizations transfers it from aio-libs-limbo to
   aio-libs. Creating the project's teams first lets them get access in
   the same step.
4. The owner removes you from aio-libs-limbo, revokes any pending
   invitations there, checks that it holds no repositories and says in
   the thread that the move is done.

If the limbo route fails, transfer the repository to a GitHub owner's
personal account instead. They have one day to accept it and then move
it into aio-libs.

If the repository belongs to an organization rather than a personal
account, you can make a GitHub owner of aio-libs an owner of that
organization for the move. They can then transfer the repository
straight into aio-libs.

A transfer fails if the target already has a repository with the same
name or a fork in the same network.

### Redirects

GitHub redirects links, `git clone`, `git fetch` and `git push` from the
old location to the new one. Through aio-libs-limbo there are two old
locations: your account and aio-libs-limbo. A redirect is deleted for
good when someone creates a repository or a fork at an old location, so
don't reuse the name in aio-libs-limbo, and give your own fork a
different name. If the repository had more than 100 clones or more than
100 GitHub Actions uses in the week before the move, GitHub also retires
the old name, and creating a repository with it fails. Update local
clones with `git remote set-url origin <new URL>`.

### What comes along

Issues, pull requests, the wiki, stars, watchers, forks, webhooks,
secrets, deploy keys and the commit history move with the repository.
GitHub Pages are not redirected, and GitHub Packages may lose their link
to the repository. The organization's default permissions and settings,
such as its Actions policies, apply from then on.

GitHub keeps issue assignees who are members of the receiving
organization and clears the others. aio-libs-limbo has few members, so
expect most assignees to be cleared at the first step, and reassign them
from your list afterwards.

GitHub's transfer documentation does not cover environments, rulesets,
branch protection or Actions variables. aiofastnet kept its environment
and rulesets, but check them after the move. Third-party GitHub Apps may
need an owner's approval: for aiofastnet, CodSpeed uploads failed until
the app was approved ([#80][af80]).

## Moving the PyPI project

Projects in the [aio-libs PyPI organization][pypi-org] are owned by the
organization. Their maintainers are added back with the Maintainer role.

Only a project owner who is also an Owner or Manager of the
organization can move a project in. A project owner who isn't sees
"Project owners can transfer the project to organizations that they own
or manage." These are the steps used for aiofastnet ([#76][af76]):

1. You add a PyPI owner as an owner of the project. PyPI sends them an
   invitation, which they accept. If your PyPI username differs from
   your GitHub one, say so in the thread.
2. They [move the project][pypi-transfer] into the organization, from
   the project settings or from the organization's project list.
3. They invite you to the organization by your PyPI username. Accept it
   from the email or the banner on PyPI.
4. Once you have accepted, they give you the Maintainer role through a
   team. You may lose access to the project until then ([#26][d26]).

If the project isn't on PyPI yet, a PyPI owner can add a pending
publisher at the organization level, and the first upload creates the
project inside the organization.

## Trusted publishing

PyPI checks the ID of the repository owner when GitHub Actions
publishes. Your [trusted publisher][pypi-tp] stops matching as soon as
the repository leaves your account, and uploads fail with
`invalid-publisher` until there is a publisher with owner `aio-libs`,
the repository name, the workflow filename and, if you use one, the
environment name. It can be added in two ways:

- A PyPI owner adds it after the PyPI move. This order is preferred
  because of problems seen with earlier transfers ([#77][af77]).
- You add it before the PyPI move, while you still own the project.
  That is what happened for aiofastnet, and its next release published
  from aio-libs/aiofastnet.

After that:

- A PyPI owner removes the publisher for the old location. A repository
  created there later could match it. Nobody adds a publisher for
  aio-libs-limbo, where members can create repositories.
- A GitHub owner protects the `pypi` environment. aiofastnet releases
  wait for an approval and a 15 minute timer ([#77][af77]). A workflow
  that uses a missing environment creates it without any protection, so
  a release that works does not prove the protection is there. Check it
  by hand.
- If the project also uploads to TestPyPI, update the publisher there
  too. TestPyPI has its own accounts and organizations.
- If the project publishes with an API token stored as a secret, switch
  to trusted publishing, revoke the token on PyPI and delete the secret.
  Give `id-token: write` only to the jobs that upload or sign, never to
  the jobs that build ([#45][d45]).

## After the move

A GitHub owner:

- Gives the maintainers access through teams for the project, if that
  didn't happen during the move.
- Reviews the webhooks, deploy keys and secrets that came along and
  removes the ones nobody needs.
- Approves the third-party GitHub Apps the project needs in the
  [organization settings][gh-apps].
- Checks the environments, rulesets and branch protection of the
  repository.

A PyPI owner checks the project's collaborators: ownership sits with the
organization and the maintainers have the Maintainer role.

Then you make a release, and the owners check that it waited for
approval and reached PyPI.

If the documentation is built on Read the Docs, check that it still
builds. If it doesn't, the Read the Docs GitHub App needs access to the
repository and the project needs to be [connected to it again][rtd-git].
Ask an owner if you want a `<project>.aio-libs.org` domain like
[aiosmtpd's][aiosmtpd-docs], or a Matrix room for the project.

You also:

- Search the repository for the old `<owner>/<repository>` and replace
  it: badges, images and clone commands in the README, `project.urls`
  in `pyproject.toml`, the documentation configuration, release note
  link templates, and `if: github.repository == ...` conditions in
  workflows, which otherwise skip jobs silently. PyPI shows the new
  project URLs from the next release on.
- Note that any community health file the repository lacks now comes
  from [aio-libs/.github][dotgithub]: `CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md` (including its rules on LLM use), `SECURITY.md`,
  `FUNDING.yml` and the issue and pull request templates. If
  sponsorships are turned on, the Sponsor button shows the
  organization's `FUNDING.yml`. Add your own file for anything you want
  to keep different.

## Suggested follow-ups

Owners may open issues titled "[aio-libs migration task] ..." for these.
They are suggestions: banners, license, branch name and the rest are the
project's call. Close the ones you don't want.

- Keep topic branches in a personal fork instead of the main repository
  ([#81][af81]). See the redirect note above before naming it.
- Set your local Git author email so that your commits are linked to
  your GitHub account ([#83][af83]).
- Borrow the issue and pull request templates of other aio-libs
  projects such as yarl, multidict or aiohttp ([#78][af78]).
- Adapt the organization's [security policy][security]. Say that
  private vulnerability reporting is enabled and preferred
  ([#79][af79]).
- Link the community spaces from the README, such as the Code of
  Conduct, the project's Matrix room or GitHub Sponsors ([#80][af80]).
- Manage release notes with Towncrier ([#82][af82]).
- Add one `alls-green` job that branch rulesets can require
  ([#84][af84]).
- Run linters and formatters through pre-commit ([#87][af87]).
- If you rename the default branch, use the rename button in the
  repository settings so that GitHub adds redirects ([#88][af88]).

If the original repository or PyPI name can't be transferred, for
example because its author can't be reached, this page doesn't apply.
See [#45][d45].

[aio-libs]: https://github.com/aio-libs
[aio-libs-limbo]: https://github.com/aio-libs-limbo
[pypi-org]: https://pypi.org/org/aio-libs/
[discussions]: https://github.com/orgs/aio-libs/discussions
[dotgithub]: https://github.com/aio-libs/.github
[d26]: https://github.com/orgs/aio-libs/discussions/26
[d45]: https://github.com/orgs/aio-libs/discussions/45
[d53]: https://github.com/orgs/aio-libs/discussions/53
[d55]: https://github.com/orgs/aio-libs/discussions/55
[bdraco]:
https://github.com/orgs/aio-libs/discussions/55#discussioncomment-18587207
[coc]: CODE_OF_CONDUCT.md
[security]: SECURITY.md
[af-tasks]:
https://github.com/aio-libs/aiofastnet/issues?q=is%3Aissue%20%22aio-libs%20migration%20task%22
[af76]: https://github.com/aio-libs/aiofastnet/issues/76
[af77]: https://github.com/aio-libs/aiofastnet/issues/77
[af78]: https://github.com/aio-libs/aiofastnet/issues/78
[af79]: https://github.com/aio-libs/aiofastnet/issues/79
[af80]: https://github.com/aio-libs/aiofastnet/issues/80
[af81]: https://github.com/aio-libs/aiofastnet/issues/81
[af82]: https://github.com/aio-libs/aiofastnet/issues/82
[af83]: https://github.com/aio-libs/aiofastnet/issues/83
[af84]: https://github.com/aio-libs/aiofastnet/issues/84
[af87]: https://github.com/aio-libs/aiofastnet/issues/87
[af88]: https://github.com/aio-libs/aiofastnet/issues/88
[gh-transfer]:
https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository
[gh-apps]: https://github.com/organizations/aio-libs/settings/installations
[pypi-transfer]:
https://docs.pypi.org/organization-accounts/actions/project-actions/#transfer-a-project
[pypi-tp]: https://docs.pypi.org/trusted-publishers/adding-a-publisher/
[rtd-git]:
https://docs.readthedocs.com/platform/stable/reference/git-integration.html
[aiosmtpd-docs]: https://aiosmtpd.aio-libs.org
