FILE_FILTER_SCHEMA = {
    'type': 'object',
    'properties': {
        'case_insensitive': {
            'type': 'string'
        },
        'filters': {
            'type': 'object',
            'properties': {
                'access': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'acl': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'case_barcode': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'case_gdc_id': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'data_category': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'data_format': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'data_type': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'experimental_strategy': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'file_gdc_id': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'file_name_key': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'index_file_id': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'index_file_name_key': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'platform': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'program_name': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'project_short_name': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'sample_barcode': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'sample_gdc_id': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'type': {
                    'type': ['array', 'string'],
                    'items': { 'type': 'string' }
                },
                'file_size': {
                    'type': ['array', 'string', 'integer'],
                    'items': { 'type': ['string', 'integer'] }
                },
                'index_file_size': {
                    'type': ['array', 'string', 'integer'],
                    'items': { 'type': ['string', 'integer'] }
                },
                'file_size_lte': {
                    'type': ['array', 'string', 'integer'],
                    'items': { 'type': ['string', 'integer'] }
                },
                'index_file_size_lte': {
                    'type': ['array', 'string', 'integer'],
                    'items': { 'type': ['string', 'integer'] }
                },
                'file_size_gte': {
                    'type': ['array', 'string', 'integer'],
                    'items': { 'type': ['string', 'integer'] }
                },
                'index_file_size_gte': {
                    'type': ['array', 'string', 'integer'],
                    'items': { 'type': ['string', 'integer'] }
                },
                'file_size_btw': {
                    'type': 'array',
                    'items': { 'type': ['string', 'integer'] }
                },
                'index_file_size_btw': {
                    'type': 'array',
                    'items': { 'type': ['string', 'integer'] }
                },
                'fetch_count': {
                    'type': 'integer'
                },
                'offset': {
                    'type': 'integer'
                },
                'genomic_build': {
                    'type': 'string'
                },
            }
        }
    }
}