


# Marketing Data Foundation Native App

This repository is the source code for the [Marketing Data Foundation V2 Quickstart](https://quickstarts.snowflake.com/guide/marketing_data_foundation_starter_v2/index.html). Please refer to the quickstart for all instructions.


## Introduction
The purpose of this application is to provide a framework to generate transformations and mapping rules that allow you to standardize and unify different data models into a known data-model that can be used to aggregate data and generate a single source of truth of your marketing campaing data.

## Setup

Steb by step installation is available in the [deployment notebook](/deployment.ipynb). Follow the instructions to get the native app deployed in your snowflake account.

## Repo structure

The source files for the application are under the directory _/data_harmonization_nativeapp/streamlit_, wich contains two entry points, _home.py_ and _landing-page.py_ the second one can be ingnore since it is for container services deployment also the _/frontend_ directory can be ingored for the same reason.

Under the _/data_harmonization_nativeapp/scripts_ there is a file named _setup.sql_ which is run when the native app is deployed

## Run streamlit locally

1. Update the _connection_config.json_ with your credentials
2. Run the following command `streamlit run data_harmonization_nativeapp/streamlit/home.py`

## Unit Test:
Set the testing virtual environment.
```
python3.9 -m venv data_harmonization-testing
source data_harmonization-testing/bin/activate
pip install -r requirements_test.txt
```

To run unit tests use the next command:
```
pytest -v --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html
```

To deactivate environment:
```
deactivate
```

To debug using breakpoints while testing add the flag `--pdb`, and to check the coverage percentage use the flag `--cov-fail-under=80`.
