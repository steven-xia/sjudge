sjudge
======

[![Build Status](https://img.shields.io/travis/com/xtevenx/sjudge/master?logo=travis)](https://travis-ci.com/xtevenx/sjudge)
[![Coverage Status](https://img.shields.io/coveralls/github/xtevenx/sjudge/master?logo=coveralls&logoColor=blue)](https://coveralls.io/github/xtevenx/sjudge?branch=master)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/xtevenx/sjudge.svg?logo=lgtm&logoColor=pink)](https://lgtm.com/projects/g/xtevenx/sjudge/context:python)
[![Dependencies](https://img.shields.io/librariesio/github/xtevenx/sjudge?logo=python&logoColor=yellow)](https://github.com/xtevenx/sjudge/blob/master/requirements.txt)
[![License](https://img.shields.io/github/license/xtevenx/sjudge?logo=open-source-initiative&logoColor=white)](https://github.com/xtevenx/sjudge/blob/master/LICENSE)

`sjudge` is a client-side programming judge made for use as a teaching tool.
It is programmed in pure Python and designed to be as simple and robust as possible.

The differences between `sjudge` and the many available online judges is that `sjudge` is designed for small classroom 
use and the simplicity for a teacher to make their modifications if they so desire.

When (and why) I should use `sjudge`
------------------------------------

`sjudge` is a "programming judge", which means that it is a tool used to test programs to see if they work as expected.
However, contrary to most other judges, `sjudge` is locally run which results in a simpler design.
Along with it also comes with a set of advantages and disadvantages:

| Advantages                                            | Disadvantages                                                 |
| ------------------------------------------------------|---------------------------------------------------------------|
| Simple design for easy configurability.               | A program's performance will vary depending on the computer.  |
| No fear of students trying to undermine your machine. | The test cases are viewable by the students.                  |

### `sjudge` as a backend

Another method of utilizing `sjudge` is to use it to mark tests.
For example, one could pose a set of problems to the students, save their solutions, then run `sjudge` with a script to 
determine the results of the test.
One downside of this method is that students' solutions would need to be run on your machine, however, that can be 
easily overcome by creating a new user with no special permissions with which to run the marking script.

Supported Platforms
-------------------

| Operating Systems                 | Python Versions   |
| ----------------------------------|-------------------|
| Ubuntu 18.04 LTS (Bionic Beaver)  | Python 3.7.x      |
| Ubuntu 20.04 LTS (Focal Fossa)    | Python 3.8.x      |
| Windows 10                        |                   |

Setup
-----

### Installation

`sjudge` depends on the Python packages and versions listed in `requirements.txt`; use the following command to install them:

```bash
pip3 install -r requirements.txt
```

### Configuration

`sjudge` needs a public readable directory to store all the exercises. 
Edit `DEFAULT_EXERCISES` in `src/main.py` to point to the full path of that directory.

To have the students run `sjudge`, place it in a directory to which they have read access (usually `/usr/local/sbin/` on linux) and instruct them to add it to their `PATH` (if needed).
If hiding the location of the exercises is desired, you can compile `sjudge` into an executable with `pyinstaller`.

### Adding exercises

`sjudge` comes with a very minimal set of exercises.
To add more, look at the template files located in `exercises/` for guidance:

*   `exercises/_template.txt` is the template of an exercise description.
*   `exercises/_template.py` is the template of a test case generation script.

After the `.txt` (exercise description) and `.py` (test case generation) scripts have been created (both bearing the same name: the name of the new exercise), run the `.py` file to generate the test cases.
The new exercise name should now be listed when you run `python3 main.py --list_exercises`.

License
-------

`sjudge` is licensed under the [GNU General Public License v3.0](https://github.com/xtevenx/sjudge/blob/master/LICENSE).
