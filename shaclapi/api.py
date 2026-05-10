from flask import Flask, Response, request

from shaclapi.validator import HealtDCATShaclValidator

app = Flask(__name__)


@app.route("/")
def index():
    """
    A simple interface to send text to the validation API.
    It uses HTMX to display the validation result in the same page below the input text field.
    """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SHACL Validator</title>
        <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js" integrity="sha384-H5SrcfygHmAuTDZphMHqBJLc3FhssKjG7w/CeCpFReSfwBWDTKpkzPP8c+cLsK+V" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/htmx-ext-response-targets@2.0.4" integrity="sha384-T41oglUPvXLGBVyRdZsVRxNWnOOqCynaPubjUVjxhsjFTKrFJGEMm3/0KGmNQ+Pg" crossorigin="anonymous"></script>
    </head>
    <body hx-ext="response-targets">
        <h1>SHACL Validator</h1>
        <form hx-post="/validate" hx-target="#result" hx-target-4*="#result" hx-swap="innerHTML">
            <label for="rdf_data">Enter RDF Data (Turtle format):</label><br>
            <textarea id="rdf_data" name="rdf_data" rows="10" cols="50"></textarea><br>
            <input type="submit" value="Validate">
        </form>

        <div id="result" style="white-space: pre; font-family: monospace;"></div>
    </body>
    </html>
    """


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

    # Return the serialized graph as a response
    return Response(
        graph.serialize(format="turtle"),
        mimetype="text/turtle"
    )
