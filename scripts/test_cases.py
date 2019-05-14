TEST_CASES_BY_PATH = {
    '/apiv4/cohorts': {
        'post': {
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
        'patch': {
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
    '/apiv4/samples/': {
        'get': {
            'TCGA-single-sample': 'TCGA-DX-A23U-10A',
            'CCLE-single-sample': 'CCLE-253J',
            'TARGET-single-sample': 'TARGET-52-PAREWI-01A'
        },
        'post': {
            'TCGA-multi-sample': {
                'barcodes': ['TCGA-DX-A23U-10A', 'TCGA-WK-A8XQ-10A']
            },
            'CCLE-multi-sample': {
                'barcodes': ['CCLE-8-MG-BA', 'CCLE-253J', 'CCLE-A3/KAW']
            },
            'TARGET-multi-sample': {
                'barcodes': ['TARGET-52-PAREWI-01A', 'TARGET-52-PATBLF-10A', 'TARGET-52-PATDVL-01A']
            }
        }
    },
    '/apiv4/cases/': {
        'get': {
            'TCGA-single-sample': 'TCGA-DX-A23U',
            'CCLE-single-sample': 'A-204',
            'TARGET-single-sample': 'TARGET-52-PAREWI'
        },
        'post': {
            'TCGA-multi-sample': {
                'barcodes': ['TCGA-DX-A23U', 'TCGA-WK-A8XQ']
            },
            'CCLE-multi-sample': {
                'barcodes': ['A-204', '769-P', 'A3/KAW']
            },
            'TARGET-multi-sample': {
                'barcodes': ['TARGET-52-PAREWI', 'TARGET-52-PATBLF', 'TARGET-52-PATDVL']
            }
        }
    },
    '/apiv4/cohorts/{cohort_id}/file_manifest': {
        'post': {
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
    }
}