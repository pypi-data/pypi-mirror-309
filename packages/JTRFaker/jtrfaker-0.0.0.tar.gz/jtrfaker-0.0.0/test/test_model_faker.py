import pytest
from unittest.mock import MagicMock
from sqlalchemy import Column, Integer, String, Table, MetaData
from ModelFaker import ModelFaker

from faker import Faker

# Initialisiere eine MetaData-Instanz, um eine SQLAlchemy-Tabellenstruktur zu erstellen
metadata = MetaData()

# Mock SQLAlchemy Model (z.B. eine User-Tabelle)
mock_model = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('age', Integer),
    Column('is_active', Integer, default=1)
)


@pytest.fixture
def faker_instance():
    """
    Fixture to return an instance of ModelFaker with the mocked model.
    """
    return ModelFaker(mock_model)


def test_generate_fake_data(faker_instance):
    """
    Test that the _generateFakeData method correctly generates fake data
    based on column types.
    """
    faker_instance.fake = Faker()

    data = {}

    for column in faker_instance._ModelFaker__getTableColumns():
        if not faker_instance._ModelFaker__isPrimaryKeyOrHasDefaultValue(column):
            data[column.name] = faker_instance._generateFakeData(column)

    assert 'name' in data
    assert 'email' in data
    assert 'age' in data
    assert isinstance(data['name'], str)
    assert isinstance(data['email'], str)
    assert isinstance(data['age'], int)
    assert isinstance(data['is_active'], int) or data['is_active'] is None


def test_create_data(faker_instance, mocker):
    """
    Test that the create method correctly adds data and commits the session.
    """
    # Mock the db session
    mock_session = mocker.patch('ModelFaker.db.session', autospec=True)

    # Call create method to add 2 rows
    faker_instance.create(amount=2)

    # Check if db.session.add() was called for both records
    assert mock_session.add.call_count == 2

    # Check if db.session.commit() was called once
    assert mock_session.commit.call_count == 1


def test_create_with_invalid_amount(faker_instance, mocker):
    """
    Test that the create method defaults to 1 entry if the amount is invalid.
    """
    # Mock the db session
    mock_session = mocker.patch('ModelFaker.db.session', autospec=True)

    # Call create method with an invalid amount (e.g., string instead of int)
    faker_instance.create(amount="invalid")

    # Check that db.session.add() was called once (default amount is 1)
    assert mock_session.add.call_count == 1

    # Check that db.session.commit() was called once
    assert mock_session.commit.call_count == 1


def test_generate_json_data(faker_instance):
    """
    Test the _generateJsonData method for generating fake JSON data.
    """
    docstring = '{"name": "string", "age": "integer", "is_active": "boolean"}'

    generated_data = faker_instance._generateJsonData(docstring)

    assert "name" in generated_data
    assert "age" in generated_data
    assert "is_active" in generated_data

    parsed_data = json.loads(generated_data)

    assert isinstance(parsed_data["name"], str)
    assert isinstance(parsed_data["age"], str)  # Because all fake data returns as strings
    assert isinstance(parsed_data["is_active"], str)
