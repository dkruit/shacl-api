from pathlib import Path
import pytest

from rdflib import Graph, URIRef
from shaclapi.api import app


TEST_DATA_DIR = Path(__file__).parent / "data"


TYPE_URI = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
VAL_REPORT_URI = URIRef("http://www.w3.org/ns/shacl#ValidationReport")
CONFORMS_URI = URIRef("http://www.w3.org/ns/shacl#conforms")


@pytest.fixture(scope="session")
def valid_turtle_data():
    with open(TEST_DATA_DIR / "minimal_good.ttl", "r") as f:
        return f.read()


@pytest.fixture(scope="session")
def invalid_turtle_data():
    with open(TEST_DATA_DIR / "minimal_bad.ttl", "r") as f:
        return f.read()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def check_response_content_is_validation_report(data):
    """
    Check that the response can be parsed as turtle RDF and contains one or more ValidationReports which declare conforms.
    """
    graph = Graph()
    graph.parse(data=data, format="turtle")

    reports = [report for report in graph.subjects(TYPE_URI, VAL_REPORT_URI)]
    
    assert len(reports) == 1
    for report in reports: 
        conforms = [value for value in graph.objects(report, CONFORMS_URI)]
        assert len(conforms) == 1


def test_index_page(client):
    """Test that the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'SHACL Validator' in response.data


def test_validate_with_form_data(client, valid_turtle_data):
    """Test the validate endpoint with form data."""
    data = {
        'rdf_data': valid_turtle_data
    }
    response = client.post('/validate', data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == 200
    assert response.content_type == 'text/turtle; charset=utf-8'
    check_response_content_is_validation_report(response.data)


def test_validate_with_turtle_data(client, valid_turtle_data):
    """Test the validate endpoint with Turtle data."""
    data = valid_turtle_data
    response = client.post('/validate', data=data, content_type='text/turtle')
    assert response.status_code == 200
    assert response.content_type == 'text/turtle; charset=utf-8'
    check_response_content_is_validation_report(response.data)


def test_validate_with_invalid_turtle_data(client, invalid_turtle_data):
    """Test the validate endpoint with Turtle data."""
    data = invalid_turtle_data
    response = client.post('/validate', data=data, content_type='text/turtle')
    assert response.status_code == 200
    assert response.content_type == 'text/turtle; charset=utf-8'
    check_response_content_is_validation_report(response.data)
    

def test_validate_with_unsupported_content_type(client, valid_turtle_data):
    """Test the validate endpoint with an unsupported content type."""
    data = valid_turtle_data
    response = client.post('/validate', data=data, content_type='application/json')
    assert response.status_code == 415
    assert b'unsupported Content-Type' in response.data


def test_validate_with_malformatted_data(client):
    """Test the validate endpoint with invalid data."""
    data = "Not valid turtle"
    response = client.post('/validate', data=data, content_type='text/turtle')
    assert response.status_code == 400
    assert b'Unable to parse and validate the provided data' in response.data
