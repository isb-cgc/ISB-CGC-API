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
                            'avg_percent_lymphocyte_infiltration_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_monocyte_infiltration_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_necrosis_lte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_neutrophil_infiltration_lte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_normal_cells_lte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_stromal_cells_lte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_cells_lte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_nuclei_lte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_lymphocyte_infiltration_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_monocyte_infiltration_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_necrosis_gte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_neutrophil_infiltration_gte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_normal_cells_gte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_stromal_cells_gte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_cells_gte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_nuclei_gte': {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_lymphocyte_infiltration_btw': {
                                'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_monocyte_infiltration_btw': {
                                'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_necrosis_btw': {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_neutrophil_infiltration_btw': {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_normal_cells_btw': {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_stromal_cells_btw': {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_cells_btw': {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'avg_percent_tumor_nuclei_btw': {
								'type': 'array',
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
                            'max_percent_lymphocyte_infiltration_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_monocyte_infiltration_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_necrosis_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_neutrophil_infiltration_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_normal_cells_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_stromal_cells_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_cells_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_nuclei_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_lymphocyte_infiltration_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_monocyte_infiltration_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_necrosis_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_neutrophil_infiltration_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_normal_cells_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_stromal_cells_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_cells_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_nuclei_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_lymphocyte_infiltration_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_monocyte_infiltration_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_necrosis_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_neutrophil_infiltration_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_normal_cells_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_stromal_cells_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_cells_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'max_percent_tumor_nuclei_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_lymphocyte_infiltration': {
                                'type': ['array', 'string', 'number'],
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
                            'min_percent_lymphocyte_infiltration_lte':  {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_monocyte_infiltration_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_necrosis_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_neutrophil_infiltration_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_normal_cells_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_stromal_cells_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_cells_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_nuclei_lte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'num_portions_lte':  {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'num_slides_lte':  {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'min_percent_lymphocyte_infiltration_gte':  {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_monocyte_infiltration_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_necrosis_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_neutrophil_infiltration_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_normal_cells_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_stromal_cells_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_cells_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_nuclei_gte':  {
								'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'num_portions_gte':  {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'num_slides_gte':  {
								'type': ['array', 'string', 'integer'],
								'items': { 'type': ['string', 'integer'] }
                            },
                            'min_percent_lymphocyte_infiltration_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_monocyte_infiltration_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_necrosis_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_neutrophil_infiltration_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_normal_cells_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_stromal_cells_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_cells_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'min_percent_tumor_nuclei_btw':  {
								'type': 'array',
                                'items': { 'type': ['string', 'number'] }
                            },
                            'num_portions_btw':  {
								'type': 'array',
								'items': { 'type': ['string', 'integer'] }
                            },
                            'num_slides_btw':  {
								'type': 'array',
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
                            'weight_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_tobacco_smoking_onset_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_began_smoking_in_years_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'anatomic_neoplasm_subdivision_gte': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'batch_number_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'bmi_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'days_to_birth_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_initial_pathologic_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_followup_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_submitted_specimen_dx_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'height_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'psa_value_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'gleason_score_combined_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'weight_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_tobacco_smoking_onset_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_began_smoking_in_years_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'anatomic_neoplasm_subdivision_lte': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'batch_number_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'bmi_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'days_to_birth_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_initial_pathologic_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_followup_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_submitted_specimen_dx_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'height_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'psa_value_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'gleason_score_combined_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'weight_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_tobacco_smoking_onset_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_began_smoking_in_years_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'anatomic_neoplasm_subdivision_btw': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'batch_number_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'bmi_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'days_to_birth_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_initial_pathologic_diagnosis_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_followup_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_submitted_specimen_dx_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'height_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'psa_value_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'gleason_score_combined_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'weight': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'year_of_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'year_of_tobacco_smoking_onset': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'age_at_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'age_began_smoking_in_years': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'anatomic_neoplasm_subdivision': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'batch_number': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'bmi': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'bcr': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'days_to_birth': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'days_to_death': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'days_to_initial_pathologic_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'days_to_last_followup': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'days_to_last_known_alive': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'days_to_submitted_specimen_dx': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'height': {
                                'type': ['array', 'string', 'integer'],
                                'items': { 'type': ['string', 'integer'] }
                            },
                            'psa_value': {
                                'type': ['array', 'string', 'number'],
                                'items': { 'type': ['string', 'number'] }
                            },
                            'gleason_score_combined': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'summary_file_count': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'summary_file_count_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'summary_file_count_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'summary_file_count_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'clinical_M': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'clinical_N': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'clinical_stage': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'clinical_T': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'colorectal_cancer': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'country': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'histological_type': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'history_of_colon_polyps': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'history_of_neoadjuvant_treatment': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'hpv_calls': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'hpv_status': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'h_pylori_infection': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'icd_10': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'icd_o_3_histology': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'icd_o_3_site': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'lymphatic_invasion': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'lymphnodes_examined': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'lymphovascular_invasion_present': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'menopause_status': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'mononucleotide_and_dinucleotide_marker_panel_analysis_status': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'neoplasm_histologic_grade': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'new_tumor_event_after_initial_treatment': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'number_of_lymphnodes_examined': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'number_of_lymphnodes_positive_by_he': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'number_pack_years_smoked': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'other_dx': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'other_malignancy_anatomic_site': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'other_malignancy_histological_type': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'other_malignancy_type': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'pathologic_M': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'pathologic_N': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'pathologic_stage': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'pathologic_T': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'person_neoplasm_cancer_status': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'pregnancies': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'primary_neoplasm_melanoma_dx': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'primary_therapy_outcome_success': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'project_short_name': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'race': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'residual_tumor': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'stopped_smoking_year': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'tobacco_smoking_history': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'tss_code': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'tumor_tissue_site': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'tumor_type': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'venous_invasion': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'vital_status': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'ethnicity': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'gender': {
                                'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                        }
                    },
                    'TARGET': {
                        'type': 'object',
                        'properties': {
                            'sample_barcode': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'sample_gdc_id': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'sample_type': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'disease_code': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'tumor_code': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'case_barcode': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'case_gdc_id': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'program_name': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'program_dbgap_accession_number': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'project_short_name': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'project_name': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'disease_code': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'gender': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'vital_status': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'race': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ethnicity': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'age_at_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_birth': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_birth_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_birth_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_birth_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_followup': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_followup_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_followup_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_followup_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'protocol': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'year_of_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_follow_up': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_follow_up_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_follow_up_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_follow_up_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'event_free_survival_time_in_days': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'event_free_survival_time_in_days_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'event_free_survival_time_in_days_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'event_free_survival_time_in_days_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'first_event': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'WBC_at_diagnosis': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'WBC_at_diagnosis_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'WBC_at_diagnosis_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'WBC_at_diagnosis_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MLL_status': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'CNS_site_of_relapse_or_induction_failure': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'CNS_status_at_diagnosis': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'bone_marrow_site_of_relapse_or_induction_failure': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'other_site_of_relapse_or_induction_failure': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'histology': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'BCR_ABL1_status': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'BMA_blasts_day_8': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_8_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_8_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_8_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_15': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_15_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_15_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_15_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_29': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_29_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_29_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_29_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_43': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_43_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_43_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'BMA_blasts_day_43_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'DNA_index': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'DNA_index_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'DNA_index_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'DNA_index_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'Down_syndrome': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'MRD_at_end_of_course_1': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_1_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_1_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_1_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_1_YN': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'MRD_at_end_of_course_2': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_2_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_2_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_2_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_at_end_of_course_2_YN': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'MRD_day_8': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_8_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_8_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_8_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_29': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_29_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_29_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_29_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_43': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_43_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_43_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_day_43_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_end_consolidation': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_end_consolidation_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_end_consolidation_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'MRD_end_consolidation_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'cell_of_origin': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'testes_site_of_relapse': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'testicular_involvement': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'comment': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'trisomies_4_10_Status': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ETV6_RUNX1_fusion_status': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'karyotype': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'TCF3_PBX1_status': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'COG_risk_group': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ICDO_description': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'INSS_stage': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'MYCN_status': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ICDO': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'diagnostic_category': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ploidy': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'CEBPA_mutation': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'CNS_disease': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'CR_status_at_end_of_course_1': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'CR_status_at_end_of_course_2': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'FLT3_ITD_positive': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'FLT3_PM': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ISCN': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'MKI': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'NPM_mutation': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'WT1_mutation': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'bone_marrow_leukemic_blast_percentage': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'bone_marrow_leukemic_blast_percentage_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'bone_marrow_leukemic_blast_percentage_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'bone_marrow_leukemic_blast_percentage_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'chloroma': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'cytogenetic_complexity': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'del5q': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'del7q': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'del9q': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'grade': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'inv_16': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'minus_X': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'minus_Y': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'monosomy_5': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'monosomy_7': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'peripheral_blasts_pct': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'peripheral_blasts_pct_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'peripheral_blasts_pct_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'peripheral_blasts_pct_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'primary_cytogenetic_code': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'risk_group': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            't_10_11_p11_2_q23': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            't_11_19_q23_p13_1': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            't_3_5_q25_q34': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            't_6_11_q27_q23': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            't_6_9': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            't_8_21': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            't_9_11_p22_q23': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'trisomy_8': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'trisomy_21': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'FAB_category': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'SCT_in_1st_CR': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'percent_tumor': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ICD_O_3_M': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ICD_O_3_T': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'stage': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'discovery_or_validation': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'ALL_mol_subtype': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'chloroma_site_of_relapse_or_induction_failure': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'cytogenetic_site_of_relapse_or_induction_failure': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'percent_necrosis': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'percent_tumor_vs_stroma': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'site_of_relapse': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'alternate_therapy': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'c_Kit_mutation_exon8': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'c_Kit_mutation_exon17': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'cytogenetic_code_other': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'disease_at_diagnosis': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'primary_tumor_site': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'specific_tumor_site': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'time_to_first_event_in_days': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_event_in_days_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_event_in_days_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_event_in_days_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'FLT3_ITD_allelic_ratio': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'FLT3_ITD_allelic_ratio_lte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'FLT3_ITD_allelic_ratio_gte': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'FLT3_ITD_allelic_ratio_btw': {
                                'type': ['array', 'string', 'number'],
                                'items': {'type': ['string', 'number']}
                            },
                            'definitive_surgery': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'histologic_response': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'reason_for_death': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'specific_tumor_region': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'specific_tumor_side': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'time_to_first_relapse_in_days': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_relapse_in_days_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_relapse_in_days_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_relapse_in_days_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'alternate_therapy_other': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'metastasis_site': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'primary_site_progression': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'refractory_timepoint_sent_for_induction_failure_project': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'relapse_percent_necrosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'relapse_percent_necrosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'relapse_percent_necrosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'relapse_percent_necrosis_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'relapse_percent_tumor': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'relapse_type': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'therapy': {
                                'type': ['array', 'string'],
                                'items': {'type': ['string']}
                            },
                            'time_to_first_SMN_in_days': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_SMN_in_days_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_SMN_in_days_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_SMN_in_days_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_enrollment_on_relapse_protocol_in_days': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_enrollment_on_relapse_protocol_in_days_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_enrollment_on_relapse_protocol_in_days_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'time_to_first_enrollment_on_relapse_protocol_in_days_btw': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },

                        }
                    },
                    'CCLE': {
                        'type': 'object',
                        'properties': {
                            'project_short_name': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'sample_barcode': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'sample_gdc_id': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'sample_type': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'case_barcode': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'case_gdc_id': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'summary_file_count': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'summary_file_count_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'summary_file_count_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'summary_file_count_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'gender': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'hist_subtype': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'histology': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'site_primary': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'source': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                        }
                    },
                },
                "additionalProperties": False
            },
            'name': {
                'type': 'string'
            },
            'desc': {
                'type': 'string'
            }
        },
        "additionalProperties": False
    }
