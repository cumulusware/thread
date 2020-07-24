# README #

* **Project:** Thread
* **Goal:** Manage and deploy Ubuntu servers

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

## Purpose ##

The goal is to create a quick, repeatable, automated process to manage Ubuntu
servers running on either local hardware or a Virtual Private Server (VPS).
Thread uses the [Fabric][] Python "library and command-line tool designed to
streamline deploying applications or performing system administration tasks via
SSH."

## Installation ##

These are *rough* instructions for installing Fabric and Thread in a virtualenv.

1. Install virtualenv, virtualenvwrapper, and pip (Jesse Noller provides good
   instructions in his article [SO YOU WANT TO USE PYTHON ON THE
   MAC?][noller-python])
2. `mkvirtualenv thread`
3. `git clone git://github.com/cumulusware/thread.git` to whatever directory
   you want to use to store Thread
4. `fab -l` to list the available commands
5. Copy `fabrichosts_templates.py` to `fabrichosts.py` and customize for your
   hosts and roles
6. To configure a new VPS, add the VPS's IP to the `newslice` role in
   `fabrichosts.py` and then execute the `fab config_new_slice` command.


## Contributing

[thread][] is developed using [Scott Chacon][]'s [GitHub Flow][]. To
contribute, fork [thread][], create a feature branch, and then submit
a pull request.  [GitHub Flow][] is summarized as:

- Anything in the `master` branch is deployable
- To work on something new, create a descriptively named branch off of
  `master` (e.g., `new-oauth2-scopes`)
- Commit to that branch locally and regularly push your work to the same
  named branch on the server
- When you need feedback or help, or you think the brnach is ready for
  merging, open a [pull request][].
- After someone else has reviewed and signed off on the feature, you can
  merge it into master.
- Once it is merged and pushed to `master`, you can and *should* deploy
  immediately.

## License

[thread][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[coveralls image]: http://img.shields.io/coveralls/cumulusware/thread/master.svg
[coveralls link]: https://coveralls.io/r/cumulusware/thread
[fabric]: http://www.fabfile.org/
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[LICENSE.txt]: https://github.com/cumulusware/thread/blob/master/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/thread.svg
[noller-python]: http://jessenoller.com/2009/03/16/so-you-want-to-use-python-on-the-mac/
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: http://img.shields.io/pypi/v/thread.svg
[pypi ver link]: https://pypi.python.org/pypi/thread/
[scott chacon]: http://scottchacon.com/about.html
[thread]: https://github.com/cumulusware/thread
[travis image]: http://img.shields.io/travis/cumulusware/thread/master.svg
[travis link]: https://travis-ci.org/cumulusware/thread
