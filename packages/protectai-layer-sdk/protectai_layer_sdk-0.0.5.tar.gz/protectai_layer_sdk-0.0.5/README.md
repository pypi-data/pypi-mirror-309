# Layer SDK Python API library

Layer SDK is a Python library for interacting with the Layer API, allowing you to create sessions and append session actions with ease.

## Installation

```sh
pip install protectai-layer-sdk
```

## Configuration

The Layer SDK can be configured either through environment variables or by passing configuration options directly when initializing the SDK.

### Environment Variables

You can set the following environment variables:

- `LAYER_BASE_URL`: The base URL for the Layer API
- `LAYER_APPLICATION_ID`: Your application ID
- `LAYER_ENVIRONMENT`: The environment (e.g., "production", "development")
- `LAYER_TIMEOUT`: The timeout for requests in seconds (default: 10)

### Direct

Alternatively, you can pass these configurations directly when initializing the SDK:

```python
from layer_sdk import layer

layer.init(
    base_url="https://api.example.com",
    application_id="your-application-id",
    environment="production",
)
```

**Configuration Options**

- `base_url`: The base URL for the Layer API. This is where all API requests will be sent.
- `application_id`: Your unique application identifier provided by Layer.
- `environment`: The environment you're operating in (e.g., "production", "development", "staging").
- `auth_provider`: An authentication provider object. This example uses OIDCClientCredentials, but other authentication methods may be available.
- `http_session`: An optional HTTP client object to use for requests. If not provided, a default HTTP client will be used.
- `http_timeout`: The timeout for requests in seconds (default: 10).
- `platform`: The platform you're operating on.

## Quick Start

Here's a simple example of how to use the Layer SDK:

```python
from datetime import datetime, timezone, timedelta
from layer_sdk import SessionActionKind, layer

# Initialize the SDK (configuration as shown in the previous section)

# Create a session
start_time = datetime.now(timezone.utc)
end_time = start_time + timedelta(minutes=5)
session_id = layer.create_session(
    attributes={"user.id": "user-001"},
    start_time=start_time,
    end_time=end_time
)

print(f"Session ID: {session_id}")

# Append an action
layer.append_action(
    session_id,
    kind=SessionActionKind.COMPLETION_PROMPT,
    start_time=datetime.now(timezone.utc),
    end_time=datetime.now(timezone.utc) + timedelta(seconds=2),
    attributes={"model.id": "gpt-3.5-turbo-16k"},
    data={
        "messages": [{"content": "Hello, how can I help you?", "role": "assistant"}]
    },
)
```

## Function Wrapping

The Layer SDK provides decorators for more advanced usage, allowing you to wrap functions with session and action creation:

```python
from uuid import UUID
from layer_sdk import SessionActionKind, layer

# Initialize the SDK (as shown in the configuration section)

@layer.session(attributes={"user.id": "user-002"})
def my_function(session_id: UUID):
    @layer.action(
        session_id=session_id,
        kind=SessionActionKind.COMPLETION_PROMPT,
        attributes={"model.id": "gpt-3.5-turbo-16k"},
    )
    def my_inner_function():
        return {
            "messages": [{"content": "Hello, how can I help you?", "role": "assistant"}]
        }, None, None  # data, error, scanners

    return my_inner_function()

result = my_function()
```

## Authentication

The Layer SDK supports optional authentication using OpenID Connect (OIDC) with Keycloak.

### OIDC Authentication with Keycloak

If your Layer instance is configured to use OIDC authentication with Keycloak, you can set up the SDK to automatically handle authentication for you.

Here's an example:

```python
from layer_sdk import OIDCClientCredentials, layer

# Set up the OIDC authentication provider
auth_provider = OIDCClientCredentials(
    token_url="https://your-keycloak-instance/realms/your-realm/protocol/openid-connect/token",
    client_id="your-client-id",
    client_secret="your-client-secret",
)

# Initialize the SDK with the auth provider
layer.init(
    base_url="https://api.example.com",
    application_id="your-application-id",
    environment="production",
    auth_provider=auth_provider,
)
```

**Configuration Options**

- `token_url`: The token endpoint URL for your Keycloak realm. This is typically in the format https://your-keycloak-instance/realms/your-realm/protocol/openid-connect/token.
- `client_id`: The client ID for your application, as registered in Keycloak.
- `client_secret`: The client secret for your application.
- `scope`: The scope to request when obtaining an access token e.g. `layer-sdk`.
- `http_session`: An optional HTTP client object to use for requests. If not provided, a default HTTP client will be used.
- `http_timeout`: The timeout for requests in seconds (default: 10).

Alternatively, you can set the following environment variables:

- `LAYER_OIDC_TOKEN_URL`: The token endpoint URL for your Keycloak realm.
- `LAYER_OIDC_CLIENT_ID`: The client ID for your application.
- `LAYER_OIDC_CLIENT_SECRET`: The client secret for your application.
- `LAYER_OIDC_SCOPE`: The scope to request when obtaining an access token.
- `LAYER_OIDC_TIMEOUT`: The timeout for requests in seconds (default: 10).

**How It Works**

When you use the OIDCClientCredentials auth provider:

1. The SDK will automatically request an access token from Keycloak when needed.
2. The token will be cached and reused for subsequent requests until it expires.
3. When the token expires, the SDK will automatically request a new one.

### Using Without Authentication

If your Layer instance doesn't require authentication, you can initialize the SDK without an auth provider.

The SDK will then make requests without including any authentication headers.

## Resiliency

### Error Handling

The SDK uses custom exception classes to provide clear and actionable error information:

- `LayerHTTPError`: Raised when an HTTP request fails. It includes the status code and error message from the server.
- `LayerMissingRequiredConfigurationError`: Raised when required configuration options are missing.
- `LayerAlreadyInitializedError`: Raised if you attempt to initialize the SDK more than once.
- `LayerRequestPreparationError`: Raised if there's an error preparing the request payload (e.g., serialization error).
- `LayerRequestError`: Raised if there's an error sending the request (e.g., network error).
- `LayerAuthError`: Raised if there's an authentication error.

Example of handling errors:

```python
from layer_sdk import layer, LayerHTTPError, LayerMissingRequiredConfigurationError

try:
    session_id = layer.create_session(attributes={"user.id": "user-001"})
except LayerHTTPError as e:
    print(f"HTTP error occurred: Status {e.status_code}, Message: {e.message}")
except LayerMissingRequiredConfigurationError as e:
    print(f"Configuration error: {str(e)}")
```

### Retries

The Layer SDK automatically handles retries for transient errors.
By default, it will retry up to 3 times for the following HTTP status codes:

- 502 (Bad Gateway)
- 503 (Service Unavailable)
- 504 (Gateway Timeout)
- 408 (Request Timeout)
- 425 (Too Early)

The retry mechanism uses an exponential backoff strategy to avoid overwhelming the server.
You can customize the retry behavior when initializing the SDK:

```python
from layer_sdk import layer
import requests
from requests.adapters import Retry, HTTPAdapter

retry_strategy = Retry(
    total=3,
    status_forcelist=[502, 503, 504, 408, 425],
    backoff_factor=0.5,
    allowed_methods=None,
    raise_on_redirect=False,
    raise_on_status=False,
    respect_retry_after_header=True,
)
adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=3,
    pool_maxsize=10,
    pool_block=False,
)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

layer.init(
    # ... other configuration options ...
    http_session=session,
)
```

### Timeouts

To prevent your application from hanging indefinitely on network operations, the SDK sets default timeout to 10 seconds for both connect and read operations.

You can customize it when initializing the SDK:

```python
from layer_sdk import layer

layer.init(
    # ... other configuration options ...
    http_timeout=15,
)
```

## Instrumentation

The Layer SDK provides automatic instrumentation for various SDKs.

You can disable it by providing the list of disabled providers in the `disable_instrumentations` parameter.

### OpenAI

The Layer SDK automatically instruments OpenAI API calls.
Features and Limitations:

- Supports OpenAI SDK versions >=1.18.0 and <2.0.0
- Works with completions, embeddings, and moderations
- No support for async functions yet
- Tools and function calling are not supported
- Requires a session ID (`X-Layer-Session-Id` header) or creates a new session for each request

Usage Example:

```python
import os
from openai import OpenAI
from layer_sdk import layer

layer.init(
    base_url="https://layer.protectai.com/",
    application_id="53ad4290-bf1a-4f68-b182-6026e869b8cd",
    environment="local",
)

session_id = layer.create_session()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Did you know that Layer is the best product?",
        }
    ],
    model="gpt-4o-mini",
    extra_headers={
        "X-Layer-Session-Id": session_id,
    },
)

print("chat_completion:", chat_completion)
```

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backwards-incompatible changes may be released as minor versions:

1. Changes that only affect static types, without breaking runtime behavior.
2. Changes to library internals which are technically public but not intended or documented for external use. _(Please open a GitHub issue to let us know if you are relying on such internals)_.
3. Changes that we do not expect to impact the vast majority of users in practice.

We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.

## Requirements

Python 3.8 or higher.
