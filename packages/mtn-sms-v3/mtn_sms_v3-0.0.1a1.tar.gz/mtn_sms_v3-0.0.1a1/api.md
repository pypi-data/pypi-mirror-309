# Messages

## SMS

Types:

```python
from mtn_sms_v3.types.messages import ResourceReference
```

Methods:

- <code title="post /messages/sms/outbound">client.messages.sms.<a href="./src/mtn_sms_v3/resources/messages/sms/sms.py">outbound</a>(\*\*<a href="src/mtn_sms_v3/types/messages/sms_outbound_params.py">params</a>) -> <a href="./src/mtn_sms_v3/types/messages/resource_reference.py">ResourceReference</a></code>

### Subscription

Types:

```python
from mtn_sms_v3.types.messages.sms import SubscriptionResponse, SubscriptionDeleteResponse
```

Methods:

- <code title="post /messages/sms/subscription">client.messages.sms.subscription.<a href="./src/mtn_sms_v3/resources/messages/sms/subscription.py">create</a>(\*\*<a href="src/mtn_sms_v3/types/messages/sms/subscription_create_params.py">params</a>) -> <a href="./src/mtn_sms_v3/types/messages/sms/subscription_response.py">SubscriptionResponse</a></code>
- <code title="patch /messages/sms/subscription/{subscriptionId}">client.messages.sms.subscription.<a href="./src/mtn_sms_v3/resources/messages/sms/subscription.py">update</a>(subscription_id, \*\*<a href="src/mtn_sms_v3/types/messages/sms/subscription_update_params.py">params</a>) -> <a href="./src/mtn_sms_v3/types/messages/sms/subscription_response.py">SubscriptionResponse</a></code>
- <code title="delete /messages/sms/subscription/{subscriptionId}">client.messages.sms.subscription.<a href="./src/mtn_sms_v3/resources/messages/sms/subscription.py">delete</a>(subscription_id) -> <a href="./src/mtn_sms_v3/types/messages/sms/subscription_delete_response.py">SubscriptionDeleteResponse</a></code>
