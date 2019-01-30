# akamai_network_list_manager
Simple (and incomplete) module to manage akamai network lists

This module uses [Akamai network list API v2](https://developer.akamai.com/api/cloud_security/network_lists/v2.html)

It doesn't deal with authentication. You need to authenticate with akamai using the EdgeGridAuth module

*Sample Usage:*
```python
from network_list_manager import NetworkListManager
from akamai.edgegrid import EdgeGridAuth
import requests

network_list_id = '12345_TESTLIST'
akamai_api_url = 'https://akzz-XXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXX.luna.akamaiapis.net'
access_token = 'XXXXXXXX'
client_token = 'XXXXXXXX'
client_secret = 'XXXXXXX'
session = requests.session()
session.auth = EdgeGridAuth(client_token=client_token,
                      client_secret=client_secret,
                      access_token=access_token)
                      
manager = NetworkListManager(session, akamai_api_url)

# Add single IP address to list
manager.append_elements(network_list_id, '127.0.0.1')

# Append list of IPs to list
manager.append_elements(network_list_id, ['127.0.0.1', '127.0.0.2', '127.0.0.3'])

# Update list with a new set of IPs
manager.update_list(network_list_id, ['127.0.0.4', '127.0.0.5', '127.0.0.6'])

# List all network lists
lists = manager.get_lists()
for l in lists['networkLists']:
    print(l['name'])

# Activate a network list
manager.activate_list(network_list_id, 'PRODUCTION', 'comment', 'email@example.com')

# Check activation status of a list
manager.get_activation_status(network_list_id, 'PRODUCTION')

```
