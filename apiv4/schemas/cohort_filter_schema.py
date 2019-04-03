COHORT_FILTER_SCHEMA = {
        'type': 'object',
        'properties': {
            'filters': {
                'type': 'object',
                'properties': {
                    'TCGA': {
                        'type': 'object',
                        'properties': {
                            'avg_percent_lymphocyte_infiltration': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_monocyte_infiltration': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_necrosis': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_neutrophil_infiltration': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_normal_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_stromal_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_nuclei': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'batch_number': {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'bcr': {
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
                            'days_to_collection': {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'days_to_sample_procurement': {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'disease_code': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'max_percent_lymphocyte_infiltration': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_monocyte_infiltration': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_necrosis': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_neutrophil_infiltration': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_normal_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_stromal_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_nuclei': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'metadata_biospecimen_id': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_lymphocyte_infiltration': {
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_monocyte_infiltration': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_necrosis': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_neutrophil_infiltration': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_normal_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_stromal_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_cells': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_nuclei': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'num_portions': {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'num_slides': {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'pathology_report_uuid': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'preservation_method': {
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
                            'sample_type': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
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
        ],
        "additionalProperties": False
    }
