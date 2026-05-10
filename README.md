# shacl-api
A simple API to validate Turtle RDF against the HealthDCAT-AP shapes.

To run the application in a Docker container:

1. Go to this directory in a terminal: `cd shacl-api`
2. Build the image: `docker build -t shacl-api .`
3. Run the tests inside the container: `docker run --rm -t shacl-api pytest ./tests`
4. Run the validation service in a web app: `docker run --rm -t -p 5000:5000 shacl-api:latest`
5. The API will be available at http://localhost:5000/
6. You submit turtle RDF data in the textbox, and click validate to make a POST call to the validation endpoint.
The result will show up below the textbox:
![App Screenshot](app-screenshot.png)
It is also possible to send POST requests directly to http://localhost:5000/validate
