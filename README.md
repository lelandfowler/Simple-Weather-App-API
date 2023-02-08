# Simple-Weather-App-API
<p>Utilizing FastAPI and GraphQL (Strawberry) I've built a website that serves temperature and humidity to the client based on a date and location provided.</p>

## Table of Contents:
- Section 1: Overview
- Section 2: Planning
- Section 3: Set-up
- Section 4: UX Discussion

## Section 1: Overview
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
- Utillizing GraphQL: [Strawberry](https://strawberry.rocks)<br>
<br>

### Links
- Weather Data Source: [Open Meteo](https://open-meteo.com)<br>
- Requirements: [CZero Technical Assessment](https://czerotoday.notion.site/Technical-Assessment-cc5f624c821249d7917a81f112f1e043)<br>


<h2>Section 2: Planning

### To do list:
  1. Find a weather API provider to retrieve the weather data.
     1. [Open Meteo](https://open-meteo.com) <br>
     or
     2. [Open Weather Map](https://openweathermap.org/api)
  2. Use the FastAPI framework to build the API
  3. Use Strawberry for graphql to handle the GraphQL queries and mutations.
  4. Implement a GraphQL query for weather information by city and date, including data on temperature and humidity by time. Consider carefully the data type for the output.
  5. Implement a GraphQL mutation for saving favorite locations.
  6. Implement a GraphQL query for retrieving the weather from favorite locations.
  7. Use MongoDB (using ODMantic) as the datastore.
  8. Test the API using tools like Insomnia to make GraphQL calls.
  9. Share the demo in a Github repository and be ready to demonstrate it in a technical interview.

## Section 3: Set-up

## Section 4: UX Discussion
