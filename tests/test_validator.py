from pathlib import Path

import pytest
from rdflib import URIRef, Literal

from shaclapi.validator import HealtDCATShaclValidator

TEST_DATA_DIR = Path(__file__).parent / "data"

TYPE_URI = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
VAL_REPORT_URI = URIRef("http://www.w3.org/ns/shacl#ValidationReport")
CONFORMS_URI = URIRef("http://www.w3.org/ns/shacl#conforms")
RESULT_URI = URIRef("http://www.w3.org/ns/shacl#ValidationResult")
RESULT_MESSAGE_URI = URIRef("http://www.w3.org/ns/shacl#resultMessage")


@pytest.mark.parametrize(
    "data_file", [
        "minimal_good.ttl", 
        "elaborate_good.ttl"
    ]
)
def test_validator_passes(data_file):
    """Test the validator with good samples: conforms is True"""
    data_file_path = TEST_DATA_DIR / data_file

    # Run the validator
    validator = HealtDCATShaclValidator()
    conforms, graph = validator.validate(str(data_file_path))

    # Assert the result matches the expected outcome
    assert conforms is True
    assert (None, TYPE_URI, VAL_REPORT_URI) in graph
    assert (None, CONFORMS_URI, Literal(True)) in graph


@pytest.mark.parametrize(
    "data_file,expected_result_messages",
    [
        ("minimal_bad.ttl", {
            Literal("Value does not have class skos:Concept"),
        }),
        ("elaborate_bad.ttl", {
            Literal("Value does not have class skos:Concept"),
            Literal("Less than 1 values on <http://www.example.com/dataset/ZLOYOJ>->dc:title"),
            Literal("Value does not have class <http://data.europa.eu/eli/ontology#LegalResource>"),
        }),
    ]
)
def test_validator_fails(data_file, expected_result_messages):
    """Test the validator with sample data files."""
    data_file_path = TEST_DATA_DIR / data_file

    # Run the validator
    validator = HealtDCATShaclValidator()
    conforms, graph = validator.validate(str(data_file_path))

    # Assert validator does not conform
    assert conforms is False

    # Assert graph is ValidationReport and does not conform
    assert (None, TYPE_URI, VAL_REPORT_URI) in graph
    assert (None, CONFORMS_URI, Literal(False)) in graph

    # Extract error messages from graph
    messages = set()
    for result_node in graph.subjects(TYPE_URI, RESULT_URI):
        for _, _, message in graph.triples((result_node, RESULT_MESSAGE_URI, None)):
            messages.add(message)

    # Check messages match expected messages
    assert messages == expected_result_messages
    