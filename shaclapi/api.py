from flask import Flask, Response, request

from shaclapi.validator import HealtDCATShaclValidator

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route("/validate", methods=["POST"])
def validate():
    """
    Endpoint to validate RDF data in Turtle format.
    Expects a POST request which presents the input in one of two ways:
        - A application/x-www-form-urlencoded form request body with an attribute named "rdf_data".
        - A text/turtle request body containing the data as utf-8 encoded text.
    Returns the serialized validation graph.
    """

    content_type = request.headers.get("Content-Type", "")

    if "text/turtle" in content_type:
        # Handle case where request body is text
        data = request.data.decode("utf-8")
    elif "application/x-www-form-urlencoded" in content_type:
        # Handle case where request body is a form
        data = request.form.get("rdf_data", "")
    else:
        # Unsupported content type
        return f"Error: unsupported Content-Type: '{content_type}'. Use text/turtle or application/x-www-form-urlencoded.", 415

    # Validate the data
    validator = HealtDCATShaclValidator()
    try:
        conforms, graph = validator.validate(data)
    except Exception:
        return "Error: Unable to parse and validate the provided data.", 400
    
    # Serialize the validation graph
    serialized_graph = graph.serialize(format="turtle")

    # Return the serialized graph as a response
    return Response(
        graph.serialize(format="turtle"),
        mimetype="text/turtle"
    )
