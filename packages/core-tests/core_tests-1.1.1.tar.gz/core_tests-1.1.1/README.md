# core-tests
_______________________________________________________________________________

This project contains basic elements for testing purposes and the ability 
to run (via console commands) tests and code coverage (unittest-based). This way, we can 
stick to the `DRY -- Don't Repeat Yourself` principle...

## How to Use
```shell
pip install core-tests
```

```python
# manager.py

from click.core import CommandCollection
from core_tests.tests.runner import cli_tests

if __name__ == "__main__":
    cli = CommandCollection(sources=[cli_tests()])
    cli()
```

```shell
python manager.py run-tests --test-type unit
python manager.py run-tests --test-type integration
python manager.py run-tests --test-type "another folder that contains test cases under ./tests"
python manager.py run-coverage
```

## Execution Environment

### Install libraries
```commandline
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```commandline
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```commandline
source .venv/bin/activate
```

### Install required libraries.
```commandline
pip install .
```

### Check tests and coverage...
```commandline
python manager.py run-tests
python manager.py run-coverage
```
