
event = {
    'schema': {
        'id': {
            'type': 'string',
            'unique': True
        },
        'from': {
            'type': 'string',
            'required': True
        },
        'type': {
            'type': 'string',
            'allowed': ['message', 'status'],
            'required': True
        },
        'site_id': {
            'type': 'string',
            'required': True
        },
        'data_message': {
            'type': 'string'
        },
        'data_status': {
            'type': 'string',
            'allowed': ['online', 'offline']
        },
        'timestamp': {
            'type': 'integer',
            'required': True
        }
    }
}

site = {
    'schema': {
        'site_id': {
            'type': 'string',
            'unique': True
        },
        'messages': {
            'type': 'integer',
            'default': 0
        },
        'emails': {
            'type': 'integer',
            'default': 0
        },
        'operators': {
            'type': 'integer',
            'default': 0
        },
        'visitors': {
            'type': 'integer',
            'default': 0
        }
    }
}


eve_settings = {
    'MONGO_HOST': 'mongo',
    'MONGO_DBNAME': 'testing',
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'BANDWIDTH_SAVER': False,
    'OPLOG': True,
    'OPLOG_ENDPOINT': 'oplog',
    'OPLOG_AUDIT': True,
    'DOMAIN': {
        'events': event,
        'sites': site,
    },
}
