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

### Harness Mode

Split has been acquired by Harness. This client now supports a 'harness_mode' which uses a different authentication mechanism and provides access to Harness-specific resources.

#### Authentication

In harness mode, authentication can be configured in two ways:
- Use `harness_token` for Harness endpoints and `apikey` for Split endpoints
- If `harness_token` is not provided, `apikey` will be used for all operations

Harness endpoints use the 'x-api-key' header instead of the standard Split authentication.

#### Base URLs and Endpoints

- Existing, non-deprecated Split endpoints continue to use the Split base URLs
- New Harness-specific endpoints use the Harness base URL (https://app.harness.io/)
- There is no v3 version for the Harness API

#### Deprecated Endpoints

The following endpoints are deprecated and cannot be used in harness mode:
- `/workspaces`: POST, PATCH, DELETE, PUT verbs are deprecated
- `/apiKeys`: POST verb for apiKeyType == 'admin' is deprecated
- `/users`: all verbs are deprecated
- `/groups`: all verbs are deprecated
- `/restrictions`: all verbs are deprecated

#### Basic Usage

To use the client in harness mode:

```python
from splitapiclient.main import get_client

# Option 1: Use harness_token for Harness endpoints and apikey for Split endpoints
client = get_client({
    'harness_mode': True,
    'harness_token': 'YOUR_HARNESS_TOKEN',  # Used for Harness-specific endpoints
    'apikey': 'YOUR_SPLIT_API_KEY'         # Used for existing Split endpoints
})

# Option 2: Use apikey for all operations (if harness_token is not provided)
client = get_client({
    'harness_mode': True,
    'apikey': 'YOUR_API_KEY'  # Used for both Split and Harness endpoints
})
```

#### Working with Split Resources in Harness Mode

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

# List splits in a workspace
for split in client.splits.list(ws.id):
    print(f"Split: {split.name}")
```

#### Working with Harness-specific Resources

Harness mode provides access to several Harness-specific resources:

```python
# Account identifier is required for Harness operations
account_id = 'YOUR_ACCOUNT_IDENTIFIER'

# List tokens
for token in client.token.list(account_id):
    print(f"Token: {token.name}, ID: {token.id}")

# Get a specific token
token = client.token.get('TOKEN_ID', account_id)

# List Harness API keys
for api_key in client.harness_apikey.list(api_key_type="STANDARD", account_identifier=account_id):
    print(f"API Key: {api_key.name}, ID: {api_key.id}")

# List service accounts
for sa in client.service_account.list(account_id):
    print(f"Service Account: {sa.name}, ID: {sa.id}")

# List Harness users
for user in client.harness_user.list(account_id):
    print(f"User: {user.name}, Email: {user.email}")

# List Harness groups
for group in client.harness_group.list(account_id):
    print(f"Group: {group.name}, ID: {group.id}")

# List roles
for role in client.role.list(account_id):
    print(f"Role: {role.name}, ID: {role.id}")

# List resource groups
for rg in client.resource_group.list(account_id):
    print(f"Resource Group: {rg.name}, ID: {rg.id}")

# List role assignments
for ra in client.role_assignment.list(account_id):
    print(f"Role Assignment: {ra.id}, Role: {ra.role_identifier}")

# List Harness projects
for project in client.harness_project.list(account_identifier=account_id):
    print(f"Project: {project.name}, ID: {project.identifier}")

# Get a specific project
project = client.harness_project.get('PROJECT_ID', account_identifier=account_id)
```

#### Account Identifier

The `account_identifier` is a required parameter for all Harness operations. You have two options for providing it:

1. Specify it during client initialization (recommended):

```python
from splitapiclient.main import get_client

# Specify account_identifier during initialization
client = get_client({
    'harness_mode': True,
    'harness_token': 'YOUR_HARNESS_TOKEN', 
    'apikey': 'YOUR_SPLIT_API_KEY',
    'account_identifier': 'YOUR_ACCOUNT_ID'  # Will be used for all Harness operations
})

# Now you can make calls without specifying account_identifier in each request
tokens = client.token.list()  # account_identifier is automatically included
projects = client.harness_project.list()  # account_identifier is automatically included
```

2. Provide it with each API call:

```python
from splitapiclient.main import get_client

# Initialize without account_identifier
client = get_client({
    'harness_mode': True,
    'harness_token': 'YOUR_HARNESS_TOKEN',
    'apikey': 'YOUR_SPLIT_API_KEY'
})

# Must specify account_identifier with each API call
tokens = client.token.list(account_identifier='YOUR_ACCOUNT_ID')
projects = client.harness_project.list(account_identifier='YOUR_ACCOUNT_ID')
```

If you don't provide the account_identifier either during initialization or with each API call, the client will raise a ValueError when you try to access Harness resources.

You can still override the account_identifier for specific calls even if you provided it during initialization:

```python
# Override the default account_identifier for a specific call
other_account_projects = client.harness_project.list(account_identifier='DIFFERENT_ACCOUNT_ID')
```

The account identifier can be found in your Harness account settings or through the Harness UI. It is typically in the format of a unique string identifying your organization in the Harness platform.

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
