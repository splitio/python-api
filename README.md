# Split Python API

This API wrapper is designed to work with [Split](https://www.split.io), the platform for controlled rollouts, serving features to your users via the Split feature flag to manage your complete customer experience.

For specific instructions on how to use Split Admin REST API refer to our [official API documentation](https://docs.split.io/reference).

Full documentation on this Python wrapper is available in [this link](https://help.split.io/hc/en-us/articles/4412331052685-Python-PyPi-library-for-Split-REST-Admin-API).

### Quick setup

Install the splitapiclient:
```
pip install splitapiclient
```

Import the client object and initialize connection using an Admin API Key:

```python
from splitapiclient.main import get_client
client = get_client({'apikey': 'ADMIN API KEY'})
```

## Using in Harness Mode

Starting with version 3.5.0, the Split API client supports operating in "harness mode" to interact with both Split and Harness Feature Flags APIs.

For detailed information about Harness Feature Flags API endpoints, please refer to the [official Harness API documentation](https://apidocs.harness.io/).

### Authentication in Harness Mode

The client supports multiple authentication scenarios:

1. Harness-specific endpoints always use the 'x-api-key' header format
2. Split endpoints will use the 'x-api-key' header when using the harness_token
3. Split endpoints will use the normal 'Authorization' header when using the apikey
4. If both harness_token and apikey are provided, the client will use the harness_token for Harness endpoints and the apikey for Split endpoints

### Base URLs and Endpoints

- Existing, non-deprecated Split endpoints continue to use the Split base URLs
- New Harness-specific endpoints use the Harness base URL (https://app.harness.io/)

### Deprecated Endpoints

The following Split endpoints are deprecated and cannot be used in harness mode:
- `/workspaces`: POST, PATCH, DELETE, PUT verbs are deprecated
- `/apiKeys`: POST verb for apiKeyType == 'admin' is deprecated
- `/users`: all verbs are deprecated
- `/groups`: all verbs are deprecated
- `/restrictions`: all verbs are deprecated

### Basic Usage

To use the client in harness mode:

```python
from splitapiclient.main import get_client

# Option 1: Use harness_token for Harness endpoints and apikey for Split endpoints
client = get_client({
    'harness_mode': True,
    'harness_token': 'YOUR_HARNESS_TOKEN',  # Used for Harness-specific endpoints
    'apikey': 'YOUR_SPLIT_API_KEY',         # Used for existing Split endpoints
    'account_identifier': 'YOUR_HARNESS_ACCOUNT_ID'  # Required for Harness operations
})

# Option 2: Use harness_token for all operations (if apikey is not provided)
client = get_client({
    'harness_mode': True,
    'harness_token': 'YOUR_HARNESS_TOKEN',  # Used for both Harness and Split endpoints
    'account_identifier': 'YOUR_HARNESS_ACCOUNT_ID'
})

```

### Working with Split Resources in Harness Mode

You can still access standard Split resources with some restrictions:

```python
# List workspaces (read-only in harness mode)
for ws in client.workspaces.list():
    print(f"Workspace: {ws.name}, Id: {ws.id}")

# Find a specific workspace
ws = client.workspaces.find("Default")

# List environments in a workspace
for env in client.environments.list(ws.id):
    print(f"Environment: {env.name}, Id: {env.id}")
```

### Working with Harness-specific Resources

Harness mode provides access to several Harness-specific resources through dedicated microclients:

- token
- harness_apikey
- service_account
- harness_user
- harness_group
- role
- resource_group
- role_assignment
- harness_project

Basic example:

```python
# Account identifier is required for all Harness operations
account_id = 'YOUR_ACCOUNT_IDENTIFIER'

# List all tokens
tokens = client.token.list(account_id)
for token in tokens:
    print(f"Token: {token.name}, ID: {token.id}")

# List service accounts
service_accounts = client.service_account.list(account_id)
for sa in service_accounts:
    print(f"Service Account: {sa.name}, ID: {sa.id}")
```
For most creation, update, and delete endpoints for harness specific resources, you will need to pass through the JSON body directly. 

Example:
```python
# Create a new service account
        sa_data = {
            'name': sa_name,
            'identifier': sa_identifier,
            'email': "test@harness.io",
            'accountIdentifier': account_id,
            'description': 'Service account for dependency chain test',
            'tags': {'test': 'test tag'}
        }
        
        new_sa = client.service_account.create(sa_data, account_id)
```

For detailed examples and API specifications for each resource, please refer to the [Harness API documentation](https://apidocs.harness.io/).

### Setting Default Account Identifier

To avoid specifying the account identifier with every request:

```python
# Set default account identifier when creating the client
client = get_client({
    'harness_mode': True,
    'harness_token': 'YOUR_HARNESS_TOKEN',
    'account_identifier': 'YOUR_ACCOUNT_IDENTIFIER'
})

# Now you can make calls without specifying account_identifier in each request
tokens = client.token.list()  # account_identifier is automatically included
projects = client.harness_project.list()  # account_identifier is automatically included
```

### Testing API Endpoints

#### Example: Creating and Managing Split Resources

```python
# Initialize client
client = get_client({
    'apikey': 'YOUR_SPLIT_API_KEY'
})

# Create a workspace
workspace_data = {
    'name': 'My New Workspace',
    'requiresTitleAndComments': True
}
workspace = client.workspaces.create(workspace_data)

# Create an environment in the workspace
environment_data = {
    'name': 'Production',
    'production': True
}
environment = client.environments.create(workspace.id, environment_data)

# Create a traffic type
traffic_type_data = {
    'name': 'user',
    'displayAttributeId': 'email'
}
traffic_type = client.traffic_types.create(workspace.id, traffic_type_data)

# Create a split
split_data = {
    'name': 'new_feature',
    'description': 'A new feature flag'
}
split = client.splits.create(workspace.id, traffic_type.name, split_data)

# Add split to environment
split_definition_data = {
    'treatment': 'on',
    'keys': ['user_123', 'user_456'],
    'rules': []
}
client.splits.add_to_environment(split.name, environment.id, workspace.id, split_definition_data)
```

### Commitment to Quality:

Split’s APIs are in active development and are constantly tested for quality. Unit tests are developed for each wrapper based on the unique needs of that language, and integration tests, load and performance tests, and behavior consistency tests are running 24/7 via automated bots. In addition, monitoring instrumentation ensures that these wrappers behave under the expected parameters of memory, CPU, and I/O.

### About Split:

Split is the leading platform for intelligent software delivery, helping businesses of all sizes deliver exceptional user experiences, and mitigate risk, by providing an easy, secure way to target features to customers. Companies like WePay, LendingTree and thredUP rely on Split to safely launch and test new features and derive insights on their use. Founded in 2015, Split’s team comes from some of the most innovative enterprises in Silicon Valley, including Google, LinkedIn, Salesforce and Splunk. Split is based in Redwood City, California and backed by Accel Partners and Lightspeed Venture Partners. To learn more about Split, contact hello@split.io, or start a 14-day free trial at www.split.io/trial.

**Try Split for Free:**

Split is available as a 14-day free trial. To create an account, visit [split.io/trial](https://www.split.io/trial).

**Learn more about Split:** 

Visit [split.io/product](https://www.split.io/product) for an overview of Split, or visit our documentation at [docs.split.io](http://docs.split.io) for more detailed information.

**System Status:**

We use a status page to monitor the availability of Split’s various services. You can check the current status at [status.split.io](http://status.split.io).
