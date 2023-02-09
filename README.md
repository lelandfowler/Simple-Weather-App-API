# Simple-Weather-App-API
<p>I've built an API that serves temperature and humidity to the client based on a date and location provided.</p>

## Table of Contents:
- Section 1: Overview
- Section 2: Planning
- Section 3: Mac Deployment
- Section 4: UX Discussion

## Section 1: Overview
This API is built utilizing FastAPI as the API framework and Uvicorn as the ASGI server.</p>
By default the API is hosted locally and can be reached by at the following address after starting up the application using Uvicorn.</p>
Local Host Address: http://127.0.0.1:8000.

API documentation is provided at the following link when the API is hosted locally: http://127.0.0.1:8000/docs.

Poetry is employed for dependency management.

Testing is performed through the Pytest library.

Recommended Python Version: 3.7.16

### Inputs:
1. Date
2. Location
<br>

### Outputs
1. Temperature
2. Humidity

<br>

### Resources:
- API: [Fast API](https://fastapi.tiangolo.com)<br>
- Utilizing GraphQL: [Strawberry](https://strawberry.rocks)<br>
<br>

### Other Links
- Weather Data Source: [Open Weather Map](https://home.openweathermap.org/api_keys)<br>
- Requirements: [CZero Technical Assessment](https://czerotoday.notion.site/Technical-Assessment-cc5f624c821249d7917a81f112f1e043)<br>



## Section 2: Planning

### To do list:
  1. Find a weather API provider to retrieve the weather data.
     1. [Open Meteo](https://open-meteo.com) <br>
     or
     2. [Open Weather Map](https://openweathermap.org/api) < Currently preferred
  2. Use the FastAPI framework to build the API
  3. Use Strawberry for graphql to handle the GraphQL queries and mutations.
  4. Implement a GraphQL query for weather information by city and date, including data on temperature and humidity by time. Consider carefully the data type for the output.
  5. Implement a GraphQL mutation for saving favorite locations.
  6. Implement a GraphQL query for retrieving the weather from favorite locations.
  7. Use MongoDB (using ODMantic) as the datastore.
  8. Test the API using tools like Insomnia to make GraphQL calls.
  9. Share the demo in a GitHub repository and be ready to demonstrate it in a technical interview.

## Section 3: Mac Deployment
<p>To run this repository locally follow the steps below in your terminal (Note that these steps are valid for macOS details some installation steps may be different for Linux distros and Windows OS).</p>



__Set up and Launch Steps:__
1. Get an API key by signing up for an account at the [Open Weather Map Website](https://home.openweathermap.org/api_keys). 
2. Create a folder to hold : ```$ mkdir {name of new folder}```<br>
3. Clone the Repo: ```$ git clone git@github.com:lelandfowler/Simple-Weather-App-API.git```
4. It is suggested that a version management tool such as pyenv is installed to manage python versions.  Here I show how to do so with Brew: ```$ brew install pyenv```
5. Install python version 3.7.16: ```$ pyenv install 3.7.16```
6. It is suggested that a virtual environment is deployed, pyenv virtual ```$ brew install pyenv-virtualenv```
7. Create a virtual environment: ```$ pyenv virutalenv {name of virtual env}```
8. Activate the virtual env (this can also be automated using a ".python-version" file): ```$ source activate {name of virtual env```
9. Assign your API key from the Open Weather Map Website to the "API_KEY" environment variable in your shell (Note I use zsh and therefore alter the zshrc file, depending on your default shell you may need to alter a different file): ```$ echo 'export API_Key={YOUR API KEY}' >> ~/.zshenv```
10. Reload the ".zshrc" file's content into your shell: ```$ source ~/.zshrc```
11. Navigate to the repo folder that contains the "poetry.lock" file and install: ```$ poetry install```
12. Now the API can be started using Uvicorn: ```$ uvicorn app.main:app --reload```
13. Details of the Uvicorn autoload behavior can be found here: https://www.uvicorn.org/settings/
14. If Uvicorn successfully starts then the "Application startup complete." message will appear in the terminal a link to the api landing page will be shown above it (defaulting to:  http://127.0.0.1:8000)

__Testing__: Testing can be performed by utilizing Pytest, as described in the [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/usage.html).

## Section 4: UX Discussion
