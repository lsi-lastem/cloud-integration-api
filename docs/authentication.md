# Authentication & Access

The CUBE API uses **header-based authentication**. No session or token handling is required. Every request must include three HTTP headers provided by LSI Lastem when subscribing to the service.

## Required Headers

Each API request must include the following custom headers:

| Header Name   | Description                    |
|---------------|--------------------------------|
| `X-AppID`     | The Application ID             |
| `X-TenantID`  | The Tenant ID (your organization) |
| `X-Secret`    | The Application Secret         |

Example:
```http
X-AppID: 12345678-abcd-90ab-cdef-1234567890ab
X-TenantID: tenant-001
X-Secret: abcdef1234567890abcdef1234567890
```

## Content-Type

For all `POST` API requests, you must specify the request body as JSON:

```
Content-Type: application/json
```

## No Login Required

There is **no need for a login API** or token exchange. Access control is handled entirely via the header keys above.

## Environments

Choose the appropriate base URL depending on your usage:

| Purpose       | Base URL                      |
|---------------|-------------------------------|
| Production    | `https://lsi-lastem.cloud/`   |
| Development/Test | `https://lsicp.it/`        |

All API paths are relative to the selected base URL.

## Security Note

- Keep your Application Secret safe. Never share it publicly.
- Use HTTPS to ensure data and credentials are encrypted in transit.
- You can request new credentials if needed by contacting LSI Lastem support.
