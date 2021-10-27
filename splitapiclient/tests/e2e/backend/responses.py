traffic_types_all = [{
    'id': 1,
    'name': 'tt1',
    'displayAttributeId': 'Traffic Type one'
}, {
    'id': 2,
    'name': 'tt2',
    'displayAttributeId': 'Traffic Type two'
}]


environments_all = [{
                    'id': 'env1',
                    'name': 'Environment 1',
                    }, {
                    'id': 'env2',
                    'name': 'Environment 2'
                    }]

workspaces_all = {'objects': [{
                    'id': 'ws1',
                    'name': 'Workspace 1',
                    }, {
                    'id': 'ws2',
                    'name': 'Workspace 2'
                    }],
                'offset': 1,
                'totalCount': 2,
                'limit': 2
}

traffic_type_attributes = {
    '1': [{
        'id': '1a',
        'trafficTypeId': '1',
        'displayName': 'Attribute 1a',
        'description': 'Description of attribute 1a',
        'dataType': 'string',
        'isSearchable': False,
        }, {
        'id': '1b',
        'trafficTypeId': '1',
        'displayName': 'Attribute 1b',
        'description': 'Description of attribute 1b',
        'dataType': 'string',
        'isSearchable': False,
        }
    ],
    '2': [{
        'id': '2a',
        'trafficTypeId': '2',
        'displayName': 'Attribute 2a',
        'description': 'Description of attribute 2a',
        'dataType': 'string',
        'isSearchable': False,
        }, {
        'id': '2b',
        'trafficTypeId': '2',
        'displayName': 'Attribute 2b',
        'description': 'Description of attribute 2b',
        'dataType': 'string',
        'isSearchable': False,
        }
    ]
}
