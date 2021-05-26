COHORT_FILTER_SCHEMA={
  "type": "object",
  "properties": {
    "idc_data_version": {
      "type": "string"
    },
    "filters": {
      "type": "object",
      "properties": {
        "program_name": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "case_barcode": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "case_gdc_id": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "program_dbgap_accession_number": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "project_short_name": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "project_name": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "disease_code": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "gender": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "vital_status": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "race": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "ethnicity": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "age_at_diagnosis": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_at_diagnosis_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_at_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_at_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "age_at_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_at_diagnosis_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_birth": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_birth_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_birth_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_birth_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_birth_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_birth_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_death": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_death_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_death_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_death_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_death_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_death_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_initial_pathologic_diagnosis": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_initial_pathologic_diagnosis_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_initial_pathologic_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_initial_pathologic_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_initial_pathologic_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_initial_pathologic_diagnosis_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_followup": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_followup_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_followup_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_followup_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_last_followup_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_followup_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_known_alive": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_known_alive_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_known_alive_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_known_alive_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_last_known_alive_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_last_known_alive_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_submitted_specimen_dx": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_submitted_specimen_dx_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_submitted_specimen_dx_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_submitted_specimen_dx_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_submitted_specimen_dx_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_submitted_specimen_dx_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "clinical_stage": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "clinical_T": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "clinical_N": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "clinical_M": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "pathologic_stage": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "pathologic_T": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "pathologic_N": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "pathologic_M": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "year_of_initial_pathologic_diagnosis": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_initial_pathologic_diagnosis_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_initial_pathologic_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_initial_pathologic_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "year_of_initial_pathologic_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_initial_pathologic_diagnosis_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tumor_tissue_site": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "primary_neoplasm_melanoma_dx": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "anatomic_neoplasm_subdivision": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "country": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "other_dx": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "other_malignancy_anatomic_site": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "other_malignancy_type": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "other_malignancy_histological_type": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "history_of_neoadjuvant_treatment": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "primary_therapy_outcome_success": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "histological_type": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "neoplasm_histologic_grade": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "icd_10": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "icd_o_3_site": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "icd_o_3_histology": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "person_neoplasm_cancer_status": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "residual_tumor": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "tumor_type": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "new_tumor_event_after_initial_treatment": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "lymphnodes_examined": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "number_of_lymphnodes_examined": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_examined_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_examined_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_examined_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "number_of_lymphnodes_examined_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_examined_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_positive_by_he": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_positive_by_he_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_positive_by_he_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_positive_by_he_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "number_of_lymphnodes_positive_by_he_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_of_lymphnodes_positive_by_he_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "lymphatic_invasion": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "venous_invasion": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "lymphovascular_invasion_present": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "bcr": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "batch_number": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "batch_number_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "batch_number_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "batch_number_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "batch_number_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "batch_number_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tss_code": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "age_began_smoking_in_years": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_began_smoking_in_years_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_began_smoking_in_years_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_began_smoking_in_years_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "age_began_smoking_in_years_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "age_began_smoking_in_years_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_tobacco_smoking_onset": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_tobacco_smoking_onset_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_tobacco_smoking_onset_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_tobacco_smoking_onset_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "year_of_tobacco_smoking_onset_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "year_of_tobacco_smoking_onset_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "stopped_smoking_year": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "stopped_smoking_year_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "stopped_smoking_year_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "stopped_smoking_year_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "stopped_smoking_year_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "stopped_smoking_year_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tobacco_smoking_history": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tobacco_smoking_history_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tobacco_smoking_history_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tobacco_smoking_history_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "tobacco_smoking_history_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tobacco_smoking_history_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_pack_years_smoked": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_pack_years_smoked_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_pack_years_smoked_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_pack_years_smoked_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "number_pack_years_smoked_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "number_pack_years_smoked_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "height": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "height_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "height_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "height_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "height_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "height_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "weight": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "weight_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "weight_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "weight_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "weight_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "weight_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "bmi": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "bmi_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "bmi_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "bmi_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "bmi_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "bmi_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "mononucleotide_and_dinucleotide_marker_panel_analysis_status": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "menopause_status": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "pregnancies": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "hpv_status": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "hpv_calls": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "h_pylori_infection": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "gleason_score_combined": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "gleason_score_combined_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "gleason_score_combined_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "gleason_score_combined_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "gleason_score_combined_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "gleason_score_combined_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "psa_value": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "psa_value_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "psa_value_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "psa_value_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "psa_value_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "psa_value_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "colorectal_cancer": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "history_of_colon_polyps": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "sample_barcode": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "sample_gdc_id": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "sample_type": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "sample_type_name": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "days_to_collection": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_collection_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_collection_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_collection_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_collection_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_collection_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_sample_procurement": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_sample_procurement_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_sample_procurement_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_sample_procurement_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "days_to_sample_procurement_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "days_to_sample_procurement_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "is_ffpe": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "num_portions": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_portions_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_portions_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_portions_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "num_portions_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_portions_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_slides": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_slides_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_slides_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_slides_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "num_slides_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "num_slides_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_lymphocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_lymphocyte_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_lymphocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_lymphocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_lymphocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_lymphocyte_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_monocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_monocyte_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_monocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_monocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_monocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_monocyte_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_necrosis_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_necrosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_necrosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_necrosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_necrosis_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_neutrophil_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_neutrophil_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_neutrophil_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_neutrophil_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_neutrophil_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_normal_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_normal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_normal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_normal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_normal_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_stromal_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_stromal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_stromal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_stromal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_stromal_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_tumor_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_nuclei": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_nuclei_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_nuclei_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_nuclei_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "avg_percent_tumor_nuclei_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "avg_percent_tumor_nuclei_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_lymphocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_lymphocyte_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_lymphocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_lymphocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_lymphocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_lymphocyte_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_monocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_monocyte_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_monocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_monocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_monocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_monocyte_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_necrosis_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_necrosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_necrosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_necrosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_necrosis_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_neutrophil_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_neutrophil_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_neutrophil_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_neutrophil_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_neutrophil_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_normal_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_normal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_normal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_normal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_normal_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_stromal_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_stromal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_stromal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_stromal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_stromal_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_tumor_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_nuclei": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_nuclei_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_nuclei_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_nuclei_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "max_percent_tumor_nuclei_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "max_percent_tumor_nuclei_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_lymphocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_lymphocyte_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_lymphocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_lymphocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_lymphocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_lymphocyte_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_monocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_monocyte_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_monocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_monocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_monocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_monocyte_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_necrosis_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_necrosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_necrosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_necrosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_necrosis_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_neutrophil_infiltration_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_neutrophil_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_neutrophil_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_neutrophil_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_neutrophil_infiltration_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_normal_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_normal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_normal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_normal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_normal_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_stromal_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_stromal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_stromal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_stromal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_stromal_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_cells_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_tumor_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_cells_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_nuclei": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_nuclei_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_nuclei_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_nuclei_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "min_percent_tumor_nuclei_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "min_percent_tumor_nuclei_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Modality": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "BodyPartExamined": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "StudyDescription": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "StudyInstanceUID": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "PatientID": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Program": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SeriesInstanceUID": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SOPInstanceUID": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SeriesDescription": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SliceThickness": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SliceThickness_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SliceThickness_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SliceThickness_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "SliceThickness_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SliceThickness_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SeriesNumber": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "StudyDate": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SOPClassUID": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "collection_id": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "gcs_url": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "source_DOI": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "gcs_bucket": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "crdc_study_uuid": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "crdc_series_uuid": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "crdc_instance_uuid": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "gcs_generation": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "tcia_tumorLocation": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "AnatomicRegionSequence": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SegmentedPropertyCategoryCodeSequence": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SegmentedPropertyTypeCodeSequence": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "FrameOfReferenceUID": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SegmentNumber": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SegmentNumber_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SegmentNumber_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SegmentNumber_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "SegmentNumber_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SegmentNumber_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SegmentAlgorithmType": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "SUVbw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SUVbw_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SUVbw_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SUVbw_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "SUVbw_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "SUVbw_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Volume": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Volume_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Volume_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Volume_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Volume_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Volume_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Diameter": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Diameter_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Diameter_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Diameter_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Diameter_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Diameter_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Surface_area_of_mesh": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Surface_area_of_mesh_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Surface_area_of_mesh_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Surface_area_of_mesh_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Surface_area_of_mesh_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Surface_area_of_mesh_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Total_Lesion_Glycolysis": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Total_Lesion_Glycolysis_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Total_Lesion_Glycolysis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Total_Lesion_Glycolysis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Total_Lesion_Glycolysis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Total_Lesion_Glycolysis_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Standardized_Added_Metabolic_Activity_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_First_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_Background": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_Background_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_Background_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_Background_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Standardized_Added_Metabolic_Activity_Background_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Standardized_Added_Metabolic_Activity_Background_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Internal_structure": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Sphericity": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Calcification": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Lobular_Pattern": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Spiculation": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Margin": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Texture": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Subtlety_score": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Malignancy": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "Apparent_Diffusion_Coefficient": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Apparent_Diffusion_Coefficient_lt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Apparent_Diffusion_Coefficient_lte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Apparent_Diffusion_Coefficient_btw": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "Apparent_Diffusion_Coefficient_gte": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "Apparent_Diffusion_Coefficient_gt": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 1,
          "maxItems": 1
        },
        "tcia_species": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        }
      },
      "additionalProperties": False
    }
  },
  "$schema": "http://json-schema.org/schema#"
}
