# API Endpoints

This section describes the main REST API endpoints available for each application (Enviro-CUBE or Indoor-CUBE).

Each application has its own credentials and set of devices.

All endpoints must include the required headers (`X-AppID`, `X-TenantID`, `X-Secret`) as described in [Authentication](authentication.md).

---

## 1. Get Device Configuration

**Endpoint**  
`GET /api/org/integrations/configs/`

**Description**  
Returns the list of devices and available environmental measures for your application.

**Response Example**
```json
{
  "vss":
  [
    {
      "uuid": "d4e2411281147rwh",
      "name": "GAS SCD41",
      "coords": null,
      "devices": [
        {
          "serial": "D4EB2246",
          "guid": "D4EB2246",
          "product": "SPL.009"
        }
      ],
      "measureKeys": [
        {
          "measureKey": "bt",
          "name": "Batt",
          "precision": 1,
          "unit": "V"
        },
        {
          "measureKey": "VOC_1",
          "name": "VOC",
          "precision": 0,
          "unit": "ppb"
        },
        {
          "measureKey": "GM_2",
          "name": "MisGen1",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "CO2_3",
          "name": "CO2",
          "precision": 0,
          "unit": "ppm"
        },
        {
          "measureKey": "GM_4",
          "name": "MisGen2",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "GM_5",
          "name": "MisGen3",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "GM_6",
          "name": "MisGen4",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "GM_7",
          "name": "MisGen5",
          "precision": 2,
          "unit": "n.d."
        }
      ]
    },
    {
      "uuid": "dc324112811481oo",
      "name": "GAS EE895",
      "coords": null,
      "devices": [
        {
          "serial": "DC32EB99",
          "guid": "DC32EB99",
          "product": "SPL.009FAKE"
        }
      ],
      "measureKeys": [
        {
          "measureKey": "bt",
          "name": "Batt",
          "precision": 1,
          "unit": "V"
        },
        {
          "measureKey": "VOC_1",
          "name": "VOC",
          "precision": 0,
          "unit": "ppb"
        },
        {
          "measureKey": "GM_2",
          "name": "MisGen1",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "CO2_3",
          "name": "CO2",
          "precision": 0,
          "unit": "ppm"
        },
        {
          "measureKey": "GM_4",
          "name": "MisGen2",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "GM_5",
          "name": "MisGen3",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "GM_6",
          "name": "MisGen4",
          "precision": 2,
          "unit": "n.d."
        },
        {
          "measureKey": "GM_7",
          "name": "MisGen5",
          "precision": 2,
          "unit": "n.d."
        }
      ]
    }
  ]
}
```

### 📄 Response Format for `/api/org/integrations/configs/`

The response contains a list of Virtual Stations (`vss`), each representing a group of one or more physical devices with their available environmental measurements.

#### Response Schema
```json
{
  "vss": [
    {
      "uuid": "string",        // Unique identifier of the sensor system
      "name": "string",        // Display name
      "coords": null,          // Geographic coordinates (currently null)
      "devices": [
        {
          "serial": "string",  // Device serial number
          "guid": "string",    // Global unique ID
          "product": "string"  // Product code
        }
      ],
      "measureKeys": [
        {
          "measureKey": "string", // Internal ID for use in data queries
          "name": "string",       // Human-readable label
          "precision": int,       // Number of decimal digits
          "unit": "string"        // Unit of measure (e.g. °C, ppm, V)
        }
      ]
    }
  ]
}
```

---

## 2. Download Time-Series Data

**Endpoint**  
`POST /api/tms/integrations/data/`

**Content-Type**  
`application/json`

**Description**  
Fetches time-series data for selected devices and measures in a given time window (max 31 days).

**Request Payload**
```json
{
  "start": "2025-04-24T07:40:00",
  "stop": "2025-04-24T07:42:00",
  "vss": [
    {
      "uuid": "x4e2412031559eqz",
      "measureKeys": [
        "ta",
        "RH_1"
      ]
    }
  ]
}
```
### 📤 Request Format for `/api/tms/integrations/data/`

This endpoint accepts a POST request with a JSON body that defines the time range and the set of virtual sensor systems (`vss`) and their specific measurements to retrieve.

#### Request Schema
```json
{
  "start": "ISO-8601 string",  // Start datetime (inclusive), UTC
  "stop": "ISO-8601 string",   // Stop datetime (exclusive), UTC
  "vss": [
    {
      "uuid": "string",        // UUID of the virtual sensor system
      "measureKeys": [         // List of measureKeys to retrieve
        "string"
      ]
    }
  ]
}
```

**Response Example**

```json
{
  "vss": [
    {
      "uuid": "x4e2412031559eqz",
      "items": [
        {
          "measureKey": "ta",
          "data": [
            [
              1745480455814,
              20.2
            ],
            [
              1745480485810,
              null
            ],
            [
              1745480515806,
              20.2
            ],
            [
              1745480520000,
              null
            ]
          ]
        },
        {
          "measureKey": "RH_1",
          "data": [
            [
              1745480455814,
              62.0
            ],
            [
              1745480485810,
              null
            ],
            [
              1745480515806,
              62.0
            ],
            [
              1745480520000,
              null
            ]
          ]
        }
      ]
    }
  ]
}
```

### 📥 Response Format for `/api/tms/integrations/data/`

The response contains the requested time series data for each measure of the specified Virtual Sensor Systems (VSS).

#### Response Schema
```json
{
  "vss": [
    {
      "uuid": "string",  // VSS UUID as requested
      "items": [
        {
          "measureKey": "string", // The requested measurement key
          "data": [
            [timestamp, value],    // List of [timestamp, value] pairs
            ...
          ]
        }
      ]
    }
  ]
}
```


---

## Notes

- Maximum time range per request: **31 days**
- Time must be in ISO 8601 format with UTC timezone (e.g. `2024-04-01T00:00:00`)
- If no data is found for the requested range or devices, the response will be an empty array `[]`
- Measure IDs are defined per device and can be fetched using the `/configs/` endpoint
