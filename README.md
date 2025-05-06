# Split Python API

This API wrapper is designed to work with [Split](https://www.split.io), the platform for controlled rollouts, serving features to your users via the Split feature flag to manage your complete customer experience.

For specific instructions on how to use Split Admin REST API refer to our [official API documentation](https://docs.split.io/reference).

Full documentation on this Python wrapper is available in [this link](https://help.split.io/hc/en-us/articles/4412331052685-Python-PyPi-library-for-Split-REST-Admin-API).

## Using in Harness Mode

Starting with version 3.5.0, the Split API client supports operating in "harness mode" to interact with both Split and Harness Feature Flags APIs. This is required for usage in environments that have been migrated to Harness and want to use the new features. Existing API keys will continue to work with the non-deprecated endpoints after migration, but new Harness Tokens will be required for Harness mode.

For detailed information about Harness API endpoints, please refer to the [official Harness API documentation](https://apidocs.harness.io/).

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

Non-deprecated endpoints will continue to function as they did before the migration.

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
    'description': 'Service account for test',
    'tags': {'test': 'test tag'}
}
        
new_sa = client.service_account.create(sa_data, account_id)
```

```python
# Add a user to a group
client.harness_user.add_user_to_groups(user.id, [group.id], account_id)
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

## Quick Setup

Install the splitapiclient:
```
pip install splitapiclient
```

Import the client object and initialize connection using an Admin API Key:

```python
from splitapiclient.main import get_client
client = get_client({'apikey': 'ADMIN API KEY'})
```

Enable optional logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Standard Split API Usage

### Workspaces

Fetch all workspaces:

```python
for ws in client.workspaces.list():
    print("\nWorkspace:" + ws.name + ", Id: " + ws.id)
```

Find a specific workspace:

```python
ws = client.workspaces.find("Defaults")
print("\nWorkspace:" + ws.name + ", Id: " + ws.id)
```

### Environments

Fetch all Environments:

```python
ws = client.workspaces.find("Defaults")
for env in client.environments.list(ws.id):
    print("\nEnvironment: " + env.name + ", Id: " + env.id)
```

Add new environment:

```python
ws = client.workspaces.find("Defaults")
env = ws.add_environment({'name': 'new_environment', 'production': False})
```

### Splits
Fetch all Splits:

```python
ws = client.workspaces.find("Defaults")
for split in client.splits.list(ws.id):
    print("\nSplit: " + split.name + ", " + split._workspace_id)
```

Add new Split:

```python
split = ws.add_split({'name': 'split_name', 'description': 'new UI feature'}, "user")
print(split.name)
```

Add tags:

```python
split.associate_tags(['my_new_tag', 'another_new_tag'])
```

Add Split to environment:

```python
ws = client.workspaces.find("Defaults")
split = client.splits.find("new_feature", ws.id) 
env = client.environments.find("Production", ws.id)
tr1 = treatment.Treatment({"name":"on","configurations":""})
tr2 = treatment.Treatment({"name":"off","configurations":""})
bk1 = bucket.Bucket({"treatment":"on","size":50})
bk2 = bucket.Bucket({"treatment":"off","size":50})
match = matcher.Matcher({"attribute":"group","type":"IN_LIST_STRING","strings":["employees"]})
cond = condition.Condition({'matchers':[match.export_dict()]})
rl = rule.Rule({'condition':cond.export_dict(), 'buckets':[bk1.export_dict(), bk2.export_dict()]})
defrl = default_rule.DefaultRule({"treatment":"off","size":100}) 
data={"treatments":[tr1.export_dict() ,tr2.export_dict()],"defaultTreatment":"off", "baselineTreatment": "off","rules":[rl.export_dict()],"defaultRule":[defrl.export_dict()], "comment": "adding split to production"}
splitdef = split.add_to_environment(env.id, data)
```

Kill Split:

```python
ws = client.workspaces.find("Defaults")
env = client.environments.find("Production", ws.id)
splitDef = client.split_definitions.find("new_feature", env.id, ws.id)
splitDef.kill()
```

Restore Split:

```python
splitDef.restore()
```

Fetch all Splits in an Environment:

```python
ws = client.workspaces.find("Defaults")
env = client.environments.find("Production", ws.id)
for spDef in client.split_definitions.list(env.id, ws.id):
    print(spDef.name + str(spDef._default_rule))
```

Submit a Change request to update a Split definition:

```python
splitDef = client.split_definitions.find("new_feature", env.id, ws.id)
definition= {"treatments":[ {"name":"on"},{"name":"off"}],
    "defaultTreatment":"off", "baselineTreatment": "off",
    "rules": [],
    "defaultRule":[{"treatment":"off","size":100}],"comment": "updating default rule"
}
splitDef.submit_change_request(definition, 'UPDATE', 'updating default rule', 'comment', ['user@email.com'], '')
```

List all change requests:

```python
for cr in client.change_requests.list():
    if cr._split is not None:
        print(cr._id + ", " + cr._split['name'] + ", " + cr._title + ", " + str(cr._split['environment']['id'])) 
    if cr._segment is not None:
        print(cr._id + ", " + cr._segment['name'] + ", " + cr._title)
```

Approve specific change request:

```python
for cr in client.change_requests.list():
    if cr._split['name'] == 'new_feature':
        cr.update_status("APPROVED", "done")
```

### Users and Groups

Fetch all Active users:

```python
for user in client.users.list('ACTIVE'):
    print(user.email + ", " + user._id) 
```

Invite new user:

```python
group = client.groups.find('Administrators')
userData = {'email': 'user@email.com', 'groups': [{'id': '', 'type': 'group'}]}
userData['groups'][0]['id'] = group._id
client.users.invite_user(userData)
```

Delete a pending invite:

```python
for user in client.users.list('PENDING'):
    print(user.email + ", " + user._id + ", " + user._status)
    if user.email == 'user@email.com': 
        client.users.delete(user._id)
```

Update user info:

```python
data = {'name': 'new_name', 'email': 'user@email.com', '2fa': False, 'status': 'ACTIVE'}
user = client.users.find('user@email.com')
user.update_user(user._id, data)
```

Fetch all Groups:

```python
for group in client.groups.list():
    print(group._id + ", " + group._name)
```

Create Group:

```python
client.groups.create_group({'name': 'new_group', 'description': ''})
```

Delete Group:

```python
group = client.groups.find('new_group')
client.groups.delete_group(group._id)
```

Replace existing user group:

```python
user = client.users.find('user@email.com')
group = client.groups.find('Administrators')
data = [{'op': 'replace', 'path': '/groups/0', 'value': {'id': '<groupId>', 'type': 'group'}}]
data[0]['value']['id'] = group._id
user.update_user_group(data)
```

Add user to new group

```python
user = client.users.find('user@email.com')
group = client.groups.find('Administrators')
data = [{'op': 'add', 'path': '/groups/-', 'value': {'id': '<groupId>', 'type': 'group'}}]
data[0]['value']['id'] = group._id
user.update_user_group(data)
```

## About Split

### Commitment to Quality:

Split's APIs are in active development and are constantly tested for quality. Unit tests are developed for each wrapper based on the unique needs of that language, and integration tests, load and performance tests, and behavior consistency tests are running 24/7 via automated bots. In addition, monitoring instrumentation ensures that these wrappers behave under the expected parameters of memory, CPU, and I/O.

### About Split:

Split is the leading platform for intelligent software delivery, helping businesses of all sizes deliver exceptional user experiences, and mitigate risk, by providing an easy, secure way to target features to customers. Companies like WePay, LendingTree and thredUP rely on Split to safely launch and test new features and derive insights on their use. Founded in 2015, Split's team comes from some of the most innovative enterprises in Silicon Valley, including Google, LinkedIn, Salesforce and Splunk. Split is based in Redwood City, California and backed by Accel Partners and Lightspeed Venture Partners. To learn more about Split, contact hello@split.io, or start a 14-day free trial at www.split.io/trial.

**Try Split for Free:**

Split is available as a 14-day free trial. To create an account, visit [split.io/trial](https://www.split.io/trial).

**Learn more about Split:** 

Visit [split.io/product](https://www.split.io/product) for an overview of Split, or visit our documentation at [docs.split.io](http://docs.split.io) for more detailed information.

**System Status:**

We use a status page to monitor the availability of Split's various services. You can check the current status at [status.split.io](http://status.split.io).