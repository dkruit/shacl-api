# shacl-api
A simple API to validate Turtle RDF against the HealthDCAT-AP model 

To run the application in a Docker container:

1. Go to this directory in a terminal: `cd shacl-api`
2. Build the image: `docker build -t shacl-api .`
3. Run the image, specifying the desired port: `docker run --name shacl-api -p 5000:5000 shacl-api:latest`
4. The API will be available at http://localhost:5000/
5. Run the tests inside the container: `docker exec shacl-api pytest ./tests`
