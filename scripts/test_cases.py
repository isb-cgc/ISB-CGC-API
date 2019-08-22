from datetime import datetime

TEST_CASES_BY_PATH = {
    '/cohorts': {
        'POST': {
            'TCGA-disease-code': {
                'name': 'Test cohort TCGA-disease-code for {}'.format(datetime.now()),
                'filters': {
                    'TCGA': {'disease_code': ['BRCA']}
                }
            },
            'TARGET-case-barcode': {
                'name': 'Test cohort TARGET-case-barcode for {}'.format(datetime.now()),
                'filters': {
                    'TARGET': {'case_barcode': ['TARGET-52-PAKHTL']}
                }
            },
            'CCLE-sample-barcode': {
                'name': 'Test cohort CCLE-sample-barcode for {}'.format(datetime.now()),
                'filters': {
                    'CCLE': {'sample_barcode': ['CCLE-22Rv1','CCLE-42-MG-BA','CCLE-769-P','CCLE-A-253']}
                }
            },
            'TCGA-bmi-btw': {
                'name': 'Test cohort TCGA-bmi-btw for {}'.format(datetime.now()),
                'filters': {
                    'TCGA': {'bmi_btw': ['15','25']}
                }
            },
            'TARGET-wbc-at-diagnosis-gte': {
                'name': 'Test cohort TARGET-wbc-at-diagnosis-gte for {}'.format(datetime.now()),
                'filters': {
                    'TARGET': {'wbc_at_diagnosis': ['500']}
                }
            }
        },
        'PATCH': {
            'rename': {
                'name': 'Renamed Cohort'
            },
            'filter_expansion': {
                'filters': {
                    'disease_code': ['LUAD']
                }
            }
        },
    },
    '/cohorts/preview': {
        'POST': {
            'multi-program': {
                "filters": {
                    "TCGA": {
                        "bmi_btw": ['15', '25']
                    },
                    "TARGET": {
                        "disease_code": "LAML"
                    },
                    "CCLE": {}
                }
            }
        }  
    },
    '/samples/{sample_barcode}': {
        'GET': {
            'TCGA-single-sample': {'sample_barcode': 'TCGA-DX-A23U-10A'},
            'CCLE-single-sample': {'sample_barcode': 'CCLE-253J'},
            'TARGET-single-sample': {'sample_barcode': 'TARGET-52-PAREWI-01A'}
        },
    },
    '/samples': {
        'POST': {
            'TCGA-multi-sample': {
                'sample_barcodes': ['TCGA-DX-A23U-10A', 'TCGA-WK-A8XQ-10A']
            },
            'CCLE-multi-sample': {
                'sample_barcodes': ['CCLE-8-MG-BA', 'CCLE-253J', 'CCLE-A3/KAW']
            },
            'TARGET-multi-sample': {
                'sample_barcodes': ['TARGET-52-PAREWI-01A', 'TARGET-52-PATBLF-10A', 'TARGET-52-PATDVL-01A']
            }
        }
    },
    '/cases/{case_barcode}': {
        'GET': {
            'TCGA-single-case': {'case_barcode': 'TCGA-DX-A23U'},
            'CCLE-single-case': {'case_barcode': 'A-204'},
            'TARGET-single-case': {'case_barcode': 'TARGET-52-PAREWI'}
        },
    },
    '/cases': {
        'POST': {
            'TCGA-multi-sample': {
                'case_barcodes': ['TCGA-DX-A23U', 'TCGA-WK-A8XQ']
            },
            'CCLE-multi-sample': {
                'case_barcodes': ['A-204', '769-P', 'A3/KAW']
            },
            'TARGET-multi-sample': {
                'case_barcodes': ['TARGET-52-PAREWI', 'TARGET-52-PATBLF', 'TARGET-52-PATDVL']
            }
        }
    },
    '/cohorts/{cohort_id}/file_manifest': {
        'POST': {
            'TCGA-file-size-lte': {
                'filters': {
                    'program_name': ['TCGA'],
                    'file_size_lte': ['5000000']
                }
            },
            'disease-code': {
                'filters': {
                    'disease_code': ['BRCA']
                }
            },
        }
    },
    '/files/paths/{file_uuid}': {
        'GET': {
            'TARGET-file-uuid': {
                'file_uuid': '20f1cdc2-2900-4f48-9bd4-66a406bf7a61'
            },
            'TCGA-file-uuid': {
                'file_uuid': 'f7863ca3-3297-40c5-8690-f1cedb32f577'
            },
            'CCLE-file-uuid': {
                'file_uuid': '3aa3c169-7945-4ff3-9787-48270f776aa2'
            }
        }

    },
    '/files/paths': {
        'POST': {
            'TARGET-file-uuids': {
                'uuids': ['20f1cdc2-2900-4f48-9bd4-66a406bf7a61', '27e8a6c4-2ca7-4b7c-8f41-ec53fb4faa66', 'e3e6154c-ac76-4d0d-bd40-8dc213c35197']
            },
            'TCGA-file-uuids': {
                'uuids': ['f7863ca3-3297-40c5-8690-f1cedb32f577', '3cfdd784-2aae-4e59-9eb6-733736b7ac37', '78b382a4-1d0e-4946-8c22-510d05dccc09']
            },
            'CCLE-file-uuids': {
                'uuids': ['3aa3c169-7945-4ff3-9787-48270f776aa2', '6daaeb4d-d66f-4efa-b1fe-ada91f1236ba', 'e6f3246e-59f7-4c6b-90fb-88e441b48522']
            }
        }

    },
    '/users/gcp/validate/{gcp_id}': {
        'GET': {
            'should-fail': {
                'gcp_id': 'gibberish_nonsense_id_sfgdfgertergdvg34t'
            },
            'should-pass': {
                'gcp_id': 'cgc-05-0016'
            }
        }
    }
}