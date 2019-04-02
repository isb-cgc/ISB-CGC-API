COHORT_FILTER_SCHEMA = {
        'type': 'object',
        'properties': {
            'filters': {
                'type': 'object',
                'properties': {
                    'TCGA': {
                        'type': 'object',
                        'properties': {
                            'disease_code': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            }
                        }
                    },
                    'TARGET': {
                        'type': 'object',
                        'properties': {
                            'disease_code': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            }
                        }
                    },
                    'CCLE': {
                        'type': 'object',
                        'properties': {
                            'disease_code': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            }
                        }
                    },
                },
                "additionalProperties": False
            }
        },
        'required': [
            'filters'
        ]
    }
