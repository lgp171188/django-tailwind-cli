# Changelog

## 2.8.0

- Bumped default Tailwind CLI version to 3.4.0.

## 2.7.3

- [#80](https://github.com/oliverandrich/django-tailwind-cli/pull/80)
  by [@joshuadavidthomas](https://github.com/joshuadavidthomas) added document for using the
  management commands inside a docker container.
- [#81](https://github.com/oliverandrich/django-tailwind-cli/pull/81)
  by [@joshuadavidthomas](https://github.com/joshuadavidthomas) fixed typos in the documentation.

## 2.7.2

- Fixed broken commit for 2.7.1. Sorry guys.

## 2.7.1

- Bumped default Tailwind CLI version to 3.3.6.

## 2.7.0

- Added more command line arguments to `tailwind runserver` and `tailwind runserver_plus`.
    - `tailwind runserver`
        - `--skip-checks` [#69](https://github.com/oliverandrich/django-tailwind-cli/issues/69)
        - `--noreload`
        - `--nothreading`
        - `--ipv6`
    - `tailwind runserver_plus`
        - `--noreload`
        - `--nothreading`
        - `--ipv6`
        - `--pdb`
        - `--ipdb`
        - `--pm`
        - `--print-sql`
- Fixed [#67](https://github.com/oliverandrich/django-tailwind-cli/issues/67) to fetch the correct
  CLI on the Windows platform.
- `TAILWIND_CLI_PATH` can also point to a pre-installed binary from a package manager.
- Added a new setting `TAILWIND_CLI_AUTOMATIC_DOWNLOAD` to steer if you want the library to download
  the CLI binary or not. This comes in handy with the additional option for `TAILWIND_CLI_PATH` to
  point to a pre-installed binary.

## 2.6.0

- Added 'support' for Django 5.0.
    - Extended the tox configuration to include Django 5.0b1 and beyond.
    - Added the trove classifiert.
    - Removed the upper boundary of the django version.

## 2.5.0

- Bumped default version of Tailwind CSS CLI to 3.3.5.

## 2.4.5

- Moved coverage to the dev depencies. Somehow it ended up in the package dependencies.

## 2.4.4

- [#59](https://github.com/oliverandrich/django-tailwind-cli/pull/59)
  by [@killianarts](https://github.com/killianarts) fixed a regression from 2.4.3 that used the
  wrong runserver for the runserver_plus command.

## 2.4.3

- Code and project cleanup.
- Switched back to `unittest` for testing purposes.

## 2.4.2

- Correctly map aarch64 machine architecture to arm64 for downloading the CLI.

## 2.4.1

- Added checks for `runserver_plus` management command to give a nice error message,
  when `django-extensions` and `Werkzeug` are not properly installed.

## 2.4.0

- Back to Poetry for project management.
- [#57](https://github.com/oliverandrich/django-tailwind-cli/pull/57)
  by [@wshayes](https://github.com/wshayes) added optional django-extensions for the runserver_plus
  command.

## 2.3.0

- Changed default config to support lsp-tailwindcss

  "python3 -m django" was replaced with "python manage.py" so that the dynamic
  configuration of the content selector in tailwind.config.js also works inside
  the language server for Tailwind CSS in VSCode, Sublime, etc.

## 2.2.3

- Fixed a copy&paste error introduced by pasting the tailwind.config.js without proper escaping.

## 2.2.2

- Fixed an error locating templates from the global template directories configured
  via `settings.TEMPLATES[0]["DIRS"]`.

## 2.2.1

- Fixed a bug introduced by refactoring the changes
  from [#49](https://github.com/oliverandrich/django-tailwind-cli/pull/49).

## 2.2.0

- [#49](https://github.com/oliverandrich/django-tailwind-cli/pull/49)
  by [@andrlik](https://github.com/andrlik) added a new management
  command `tailwind list_templates`.
- The new default config uses this command to implent the idea of Calton Gibson outlined in his blog
  post [Using Django’s template loaders to configure Tailwind](https://noumenal.es/notes/tailwind/django-integration/).

## 2.1.1

- Switched from poetry to hatch for package management.

## 2.0.6

- Bugfix for default tailwind.config.js.

## 2.0.5

- Fixed a regression with the default path for the Tailwind CLI.

## 2.0.4

- The reworked testing setup broke the package. Had to pull 2.0.3 from PyPI.

## 2.0.3

- Readded support for Python 3.8.
- Added Python 3.12 to the testing matrix.

## 2.0.2

- Bugfixes for typing errors.
- Added missing test code.

## 2.0.0

- Version 2.0.0 is major refactoring compared to version 1.4.3.
- No more theme app required.
- Easier to install.
- Better out-of-the-box DX.
- A custom runserver that starts the Tailwind CLI watcher and the debug server in a single terminal
  session.
- Less dependencies.

## 1.4.3

- Fixed broken links in the documentation and README.

## 1.4.0

- Refactored the project for future extensions.
- Added proper documetation which is hosted
  at <https://oliverandrich.github.io/django-tailwind-cli/>.
- Swichted from django-click to django-rich to implement the management commands.

## 1.3.1

- Switched back to poetry after a long discussion.

## 1.3.0

- Switched from poetry to pdm.

## 1.2.2

- Fixed docstrings.
- Extended ruff configuration.

## 1.2.1

- Bumped default tailwind version to 3.2.7.

## 1.2.0

- Added support for Django 4.2.

## 1.1.0

- Fixes for documentation.
- Bumped Tailwind CSS default version to 3.2.4.
- Updated dependencies.

## 1.0.0

- Introduced django-click to the project.
- Refactored the management commands to use [django-click](https://pypi.org/project/django-click/).
- Renamed the `startwatcher` command to `watch`. I'm a lazy guy. :smile:
- Switched to tox for local and CI testing.

## 0.9.2

- Removed `httpx` as a dependency. Downloading the cli is done with `urllib.request.urlopen` once
  again. Fixes [\#4](https://github.com/oliverandrich/django-tailwind-cli/issues/4)
- Removed rich-styling information from error strings.
  Fixes [\#5](https://github.com/oliverandrich/django-tailwind-cli/issues/5)
- Fixing more typos in the README.md.

## 0.9.1

- Fixing some typos in the documentation.

## 0.9.0

- Inital public release.
