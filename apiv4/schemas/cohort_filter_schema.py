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
                            'age_at_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'age_at_diagnosis_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
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
                            'disease_code': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'tumor_code': {
								'type': ['array', 'string'],
                                'items': { 'type': 'string' }
                            },
                            'days_to_birth_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_birth_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_birth_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_death_lte': {
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
                            'days_to_last_followup_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'days_to_last_known_alive_gte': {
                                'type': ['array', 'string', 'integer'],
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
                            'ethnicity': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'gender': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'year_of_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_diagnosis_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_followup_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_followup_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_followup': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'year_of_last_followup_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'wbc_at_diagnosis_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'wbc_at_diagnosis_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'wbc_at_diagnosis': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'wbc_at_diagnosis_btw': {
                                'type': 'array',
                                'items': {'type': ['string', 'integer']}
                            },
                            'vital_status': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'race': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
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
                            'protocol': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'first_event': {
                                'type': ['array', 'string'],
                                'items': {'type': 'string'}
                            },
                            'event_free_survival': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'event_free_survival_gte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'event_free_survival_lte': {
                                'type': ['array', 'string', 'integer'],
                                'items': {'type': ['string', 'integer']}
                            },
                            'event_free_survival_btw': {
                                'type': 'array',
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
            }
        },
        'required': [
            'filters'
        ],
        "additionalProperties": False
    }
