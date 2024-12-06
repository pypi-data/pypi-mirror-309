# Running Tests

To run the tests for this project, you need to use the `make test` command. Before running the tests, ensure that the path to the virtual environment is correctly configured.

## Steps to Run Tests

1. **Configure the Virtual Environment Path:**
    Open the `Makefile` and set the `VENV_PATH` variable to the path of your virtual environment. For example:
    ```makefile
    VENV_PATH=~/Desktop/Environments/base_computing/micro_dlts_chain/smart_contracts_client/bin/activate
    ```

2. **Run the Tests:**
    Execute the following command in your terminal:
    ```sh
    make test
    ```

    This command will:
    - Activate the virtual environment.
    - Run the tests using `unittest` framework.

## Steps to Generate Coverage Report

1. **Run the Coverage Command:**
    Execute the following command in your terminal:
    ```sh
    make coverage
    ```

    This command will:
    - Activate the virtual environment.
    - Run the tests and measure code coverage.
    - Generate a coverage report.
    - Generate an HTML report in the `htmlcov` directory.

## Example

Here is an example of the `Makefile` configuration:
```makefile
VENV_PATH=~/Desktop/Environments/base_computing/micro_dlts_chain/smart_contracts_client/bin/activate

.PHONY: test coverage

test:
    source $(VENV_PATH) && python -m unittest discover -s tests

coverage:
    source $(VENV_PATH) && coverage run -m unittest discover -s tests
    coverage report
    coverage html
    echo "Informe HTML generado en la carpeta 'htmlcov'."
```

Make sure the `VENV_PATH` points to the correct location of your virtual environment's `activate` script.
