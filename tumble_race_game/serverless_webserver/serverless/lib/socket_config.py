
# Incoming message keys:
MESSAGE_TYPE_KEY = 'MessageType'
MESSAGE_KEY = 'Message'

# Connection table
DB_AUTH_TABLE = 'authentication'
DB_TOKEN_ID_KEY = 'token_id'
DB_CONNECTION_TABLE = 'connections'
DB_CONNECTION_ID_KEY = 'connection_id'
DB_STAGE_KEY = 'stage'
DB_DOMAIN_KEY = 'domain_name'
DB_FILTER_EXP_KEY = 'filter_expression'
DB_FILTER_FIELD_KEY = 'filter_field'
DB_SUBSCRIPTION_KEY = 'subscriptions'
DB_EVENT_TYPE = 'event_type'

# URL parameters
URL_FILTER_EXP_KEY = 'filterexpr'
URL_FILTER_FIELD_KEY = 'field'
URL_TOKEN_KEY = 'token'
URL_EVENT_TYPE_KEY = 'eventType'

TTL_KEY = 'ttl'
TOKEN_LIFETIME = 60 * 60 * 4


# Constants
class Constants:
    class Action:
        CONNECT = "CONNECT"
        DISCONNECT = "DISCONNECT"
