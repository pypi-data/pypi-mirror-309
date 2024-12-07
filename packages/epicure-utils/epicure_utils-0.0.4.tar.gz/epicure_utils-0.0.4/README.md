| Latest Version | Downloads | Tests |
|----------------|-----------|-------|
| [![PyPI version](pypi-badge.svg)](https://pypi.org/project/epicure-utils) | [![Downloads](https://pepy.tech/badge/epicure-utils)](https://pepy.tech/project/epicure-utils) | [![cov](https://raw.githubusercontent.com/patillacode/epicure/main/coverage.svg)](https://github.com/patillacode/epicure/actions) |

# epicure

```md
epicure | ˈɛpɪkjʊə, ˈɛpɪkjɔː |

noun

a person who takes particular pleasure in fine food and drink.
```

### What?

`epicure` is a collection of useful python methods and utils I tend to use in my personal projects.


### Why?

I like to keep my projects as clean as possible, and I don't like to add dependencies unless strictly necessary.

I usually end up writing the same little utils over and over again, so I decided to create a centralized place where I can keep them organized and ready to use in any project I'm working on.


### Installation

#### Plug & Play:
```bash
# Install via pip
pip install epicure-utils
```

#### Install for development:

Clone the repository:
```bash
git clone https://github.com/dvitto/epicure.git
cd epicure
```

Install the dependencies and the package:
```bash
make install

# or manually:

python -m venv venv
source venv/bin/activate
pip install -e .
```

#### System Requirements

Before using epicure, ensure you have the following installed:

- Python >= `3.10`


### Usage
Once installed you can import the package and use the methods as you would with any other python package.

Simple example:

```python
from epicure.output import colored_print

colored_print("Hello, World!", fg_color="magenta", bg_color="black")

# this will print a "Hello, World!" in your terminal
# foreground color will be magenta and background color will be black (if supported by your terminal)
```

To see an interactive example of all the things available, run the following command:

```bash
python -m epicure.demo
```

### Documentation

The documentation is generated using Sphinx.

Please generate the documentation by running the following command:

```bash
make documentation
```

The documentation will be available in the `docs` folder, open the `index.html` file in your browser to see the documentation.


### Features
- Simple and useful methods for everyday use.
- The package is organized in modules, so you can import only the methods you need.
- No dependencies other than the Python standard library.

#### Available Modules and Methods

##### `output`
- `colored_print`: Print colored text in the terminal.

----

##### `input`
- `ask_yes_no_question`: Ask the user a yes/no question.
- `multi_choice_question`: Ask the user to choose one option from a list of choices.
- `multi_choice_question_interactive`: Ask the user to choose multiple options from a list of choices. (works on Linux and macOS)
- `simple_choice_question`: Ask the user to choose multiple options from a list of choices using an interactive menu.

----

**And more to come...!**


### Testing
To run the tests, you can use the following command:

```bash
make test
# or
pytest
```

As for the coverage, you can run the following command:

```bash
make coverage
# or
coverage run -m pytest -x
coverage json -o "coverage-summary.json"
coverage report -m
```

Remember to install the testing dependencies before running the tests!

```bash
make install-test-requirements
# or
pip install -r install -r requirements/test.txt
```

### Known Issues
`multi_choice_question_interactive` does not work on Windows by default. You need to install the `windows-curses` package to use it on Windows.

### Acknowledgments
- Python community, for the amazing libraries and tools they provide.

### Contributing
Contributions are welcome!

If you have a feature request, bug report, or a pull request, please open an issue or submit a PR.


### License

epicure is released under [GNU GENERAL PUBLIC LICENSE Version 3](LICENSE).
