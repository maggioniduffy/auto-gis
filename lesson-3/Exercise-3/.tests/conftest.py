#!/usr/bin/env python


"""Define fixtures shared among all tests."""


import pathlib
import pytest
import os
from import_notebook import import_notebook


TESTS_PATH = pathlib.Path(__file__).absolute().parent
NOTEBOOKS_PATH = TESTS_PATH.parent


@pytest.fixture(scope="session")
def notebooks_path():
    yield NOTEBOOKS_PATH


@pytest.fixture(scope="session")
def problem1(notebooks_path):
    section_data, namespace = import_notebook(notebooks_path / "Exercise-3-Problem-1.ipynb")
    yield section_data, namespace
    

@pytest.fixture(scope="session")
def problem2(notebooks_path):
    section_data, namespace = import_notebook(notebooks_path / "Exercise-3-Problem-2.ipynb")
    yield section_data, namespace  

@pytest.fixture(scope="session")
def problem3(notebooks_path):
    section_data, namespace = import_notebook(notebooks_path / "Exercise-3-Problem-3.ipynb")
    yield section_data, namespace  





