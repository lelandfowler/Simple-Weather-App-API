# Simple-Weather-App-API
<p>A simple API that serves temperature and humidity to the client based on a date and location provided.</p>

## Table of Contents:
- Section 1: Overview
- Section 2: Mac Deployment
- Section 3: Coming Soon

## Section 1: Overview
This API is built utilizing FastAPI as the API framework and Uvicorn as the ASGI server.</p>
By default the API is hosted locally and can be reached by at the following address after starting up the application using Uvicorn.</p>
Local Host Address: http://127.0.0.1:8000.

API documentation is provided at the following link when the API is hosted locally: http://127.0.0.1:8000/docs.

Poetry is employed for dependency management.

Testing is performed through the Pytest library.

Recommended Python Version: 3.7.16

To employ the Strawberry GraphQL query environment navigate to localhost: http://127.0.0.1:8000/graphql

Note: localhost can be used in place of 127.0.0.1

### Inputs:
1. Date
2. Location
<br>

### Outputs
1. Temperature
2. Humidity


### Other functionality:
- Create User
- Add Favorite Cities to User
- Delete City from User Favorite Cities
- Get User and Favorite Cities
- Get City Weather Info by Date
- Get City Weather for all favorites for a specified user
<br>

### Resources:
- API: [Fast API](https://fastapi.tiangolo.com)<br>
- Utilizing GraphQL: [Strawberry](https://strawberry.rocks)<br>
<br>
- MongoDB: 

### Other Links
- Weather Data Source: [Open Weather Map](https://home.openweathermap.org/api_keys)<br>

## Section 2: Mac Deployment
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
15. Navigate to the strawbery graphql environment to query the api: http://127.0.0.1:8000/graphql

Here is a sample graphql query to get a user: 
```
    query GetOneUser {
      user(userId: "user_1") {
        ... on User {
          userId
          favorites
          creationAt
          lastUpdated
        }
        ... on Message {
          message
        }
      }
    }
```

To get all users:
```
    query GetAllUsers {
      users {
        favorites
        userId
      }
    }
```

to create a user:
```
    mutation CreateUser {
      createUser(userId: "user_1") {
        message
      }
    }
```

to add to a users favorites:
```
    mutation AddFavorite{
      addFavorite(userId:"user_1", 
        newFavorite:"Frimp"){
        message
      }
    }
```

and to get the weather data for all of a user's favorites:
```
    query GetFavForcast {
      getFavoriteForcast(userId: "user_1", requestDate: "2023-02-14") {
        ... on Message {
          __typename
          message
        }
        ... on FavoriteLocationData {
          __typename
          data {
            city
            creationAt
            lastUpdated
            timePoints {
              humidity
              temperature
              timePoint
            }
          }
        }
      }
    }
```

__Testing__: Testing can be performed by utilizing Pytest, as described in the [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/usage.html).

## Section 3: Coming Soon
The following items will be addressed to improve this application at a later date:
1. Write Shell Script for installation of DB, Python, GraphQL, Poetry, and all locked dependencies.
2. Add a Cache (Redis) for commonly requested cities
3. Add Deployment instructions for Linux