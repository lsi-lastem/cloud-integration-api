# CUBE Cloud Integration - Overview

Welcome to the LSI Lastem CUBE Cloud Integration API.

This documentation provides technical details for developers who want to access environmental data from LSI Lastem's cloud platform, CUBE, via REST APIs using JSON over HTTPS.

## What is CUBE?

CUBE is the LSI Lastem cloud platform for managing and accessing environmental monitoring data.

Each customer is represented in the platform as an **Organization**, which may own one or more **Applications** used for data collection in different environments.

There are two types of applications:

- **ENVIRO-CUBE**  
  Designed for **outdoor and industrial environments**. It collects data from weather stations, industrial sensors, and other environmental monitoring devices.  
  More info: [ENVIRO-CUBE product page](https://lsi-lastem.com/products/enviro-cube/)

- **INDOOR-CUBE**  
  Designed for **indoor environments**. It collects data from wireless sensor networks for indoor air quality, comfort, and occupancy monitoring.  
  More info: [INDOOR-CUBE product page](https://lsi-lastem.com/products/indoor-cube/)

## Key Concepts

- **Organization**: Your company or entity registered on CUBE.
- **Application**: A logical group of devices, representing a monitoring project (e.g., "Factory Site A", "Office Building").
- **Device**: A physical sensor or station that sends data to the cloud (e.g., weather station, temperature sensor).
- **Measures**: Each device reports one or more environmental variables (e.g., temperature, humidity, CO₂, wind speed).

## API Use Cases

The API allows you to:

- Retrieve the **list of available devices and their associated measures** in your application.
- Download **time-series data** for selected devices, measures, and time ranges (max 31 days per request, max 5 devices per request).

## How it Works

Each application has its own access credentials:

- `Application ID`
- `Application Secret`
- `Tenant ID`

These credentials are provided by LSI Lastem during subscription and must be included in every API request as custom HTTP headers.

There are no login tokens or sessions — access is stateless and header-based.

## Environments

| Environment | Base URL |
|-------------|-----------|
| Production  | `https://lsi-lastem.cloud/` |
| Development / Test | `https://lsicp.it/` |

All endpoints are relative to these base URLs.

## Permissions

To use the API endpoints, the application token must have the permissions:
- `ORG7001` (for configuration access)
- `TMS1901` (for data access)

These permissions must be configured via the cloud UI in the **Application > Access token** section for each app.


## Next Steps

👉 [Read about Authentication & Headers](authentication.md)  
👉 [See Available Endpoints](endpoints.md)  
