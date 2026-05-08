from abc import ABC
from typing import Tuple

from pyshacl import validate
from rdflib.graph import Graph


class ShaclValidator(ABC):
    """
    Base class for SHACL validation. Child classes need to define a SHACL Graph file.
    """
    shacl_graph = None

    def validate(self, data_graph) -> Tuple[bool, Graph]:
        """Validate the provided data graph, return conforms and the ValidationReport graph"""
        conforms, results_graph, _ = validate(data_graph, shacl_graph=self.shacl_graph)
        return conforms, results_graph


class HealtDCATShaclValidator(ShaclValidator):
    """
    SHACL validator according to version 6 of the HealthDCAT Application Profile.
    """
    shacl_graph = (
        "https://code.europa.eu/healthdataeu/healthdcat-ap/-/raw/main/public/"
        "releases/release-6/shacl/dcat-ap-SHACL.ttl"
    )
