COHORT_FILTER_SCHEMA={
  "type": "object",
  "properties": {
    "idc_version": {
      "type": "string"
    },
    "filters": {
      "type": "object",
      "properties": {
        "program_name": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "case_barcode": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "case_gdc_id": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "program_dbgap_accession_number": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "project_short_name": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "project_name": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "disease_code": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "gender": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "vital_status": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "race": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "ethnicity": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "age_at_diagnosis": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "age_at_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "age_at_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "age_at_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_birth": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_birth_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_birth_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_birth_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_death": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_death_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_death_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_death_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_initial_pathologic_diagnosis": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_initial_pathologic_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_initial_pathologic_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_initial_pathologic_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_followup": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_followup_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_followup_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_followup_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_known_alive": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_known_alive_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_known_alive_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_last_known_alive_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_submitted_specimen_dx": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_submitted_specimen_dx_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_submitted_specimen_dx_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_submitted_specimen_dx_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "clinical_stage": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "clinical_T": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "clinical_N": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "clinical_M": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "pathologic_stage": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "pathologic_T": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "pathologic_N": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "pathologic_M": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "year_of_initial_pathologic_diagnosis": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_initial_pathologic_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_initial_pathologic_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_initial_pathologic_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "tumor_tissue_site": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "primary_neoplasm_melanoma_dx": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "anatomic_neoplasm_subdivision": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "country": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "other_dx": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "other_malignancy_anatomic_site": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "other_malignancy_type": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "other_malignancy_histological_type": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "history_of_neoadjuvant_treatment": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "primary_therapy_outcome_success": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "histological_type": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "neoplasm_histologic_grade": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "icd_10": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "icd_o_3_site": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "icd_o_3_histology": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "person_neoplasm_cancer_status": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "residual_tumor": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "tumor_type": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "new_tumor_event_after_initial_treatment": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "lymphnodes_examined": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "number_of_lymphnodes_examined": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_of_lymphnodes_examined_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_of_lymphnodes_examined_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_of_lymphnodes_examined_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_of_lymphnodes_positive_by_he": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_of_lymphnodes_positive_by_he_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_of_lymphnodes_positive_by_he_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_of_lymphnodes_positive_by_he_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "lymphatic_invasion": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "venous_invasion": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "lymphovascular_invasion_present": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "bcr": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "batch_number": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "batch_number_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "batch_number_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "batch_number_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "tss_code": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "age_began_smoking_in_years": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "age_began_smoking_in_years_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "age_began_smoking_in_years_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "age_began_smoking_in_years_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_tobacco_smoking_onset": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_tobacco_smoking_onset_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_tobacco_smoking_onset_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_tobacco_smoking_onset_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "stopped_smoking_year": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "stopped_smoking_year_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "stopped_smoking_year_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "stopped_smoking_year_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "tobacco_smoking_history": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "tobacco_smoking_history_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "tobacco_smoking_history_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "tobacco_smoking_history_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_pack_years_smoked": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_pack_years_smoked_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_pack_years_smoked_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "number_pack_years_smoked_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "height": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "height_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "height_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "height_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "weight": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "weight_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "weight_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "weight_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "bmi": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "bmi_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "bmi_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "bmi_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "mononucleotide_and_dinucleotide_marker_panel_analysis_status": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "menopause_status": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "pregnancies": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "hpv_status": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "hpv_calls": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "h_pylori_infection": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "gleason_score_combined": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "gleason_score_combined_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "gleason_score_combined_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "gleason_score_combined_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "psa_value": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "psa_value_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "psa_value_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "psa_value_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "colorectal_cancer": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "history_of_colon_polyps": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "sample_barcode": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "sample_gdc_id": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "sample_type": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "sample_type_name": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "days_to_collection": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_collection_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_collection_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_collection_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_sample_procurement": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_sample_procurement_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_sample_procurement_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_sample_procurement_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "is_ffpe": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "num_portions": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "num_portions_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "num_portions_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "num_portions_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "num_slides": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "num_slides_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "num_slides_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "num_slides_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_lymphocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_lymphocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_lymphocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_lymphocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_monocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_monocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_monocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_monocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_necrosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_necrosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_necrosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_neutrophil_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_neutrophil_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_neutrophil_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_normal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_normal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_normal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_stromal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_stromal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_stromal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_nuclei": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_nuclei_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_nuclei_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "avg_percent_tumor_nuclei_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_lymphocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_lymphocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_lymphocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_lymphocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_monocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_monocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_monocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_monocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_necrosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_necrosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_necrosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_neutrophil_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_neutrophil_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_neutrophil_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_normal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_normal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_normal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_stromal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_stromal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_stromal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_nuclei": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_nuclei_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_nuclei_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "max_percent_tumor_nuclei_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_lymphocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_lymphocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_lymphocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_lymphocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_monocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_monocyte_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_monocyte_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_monocyte_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_necrosis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_necrosis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_necrosis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_neutrophil_infiltration_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_neutrophil_infiltration_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_neutrophil_infiltration_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_normal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_normal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_normal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_stromal_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_stromal_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_stromal_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_cells_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_cells_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_nuclei": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_nuclei_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_nuclei_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "min_percent_tumor_nuclei_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Modality": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "BodyPartExamined": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "StudyDescription": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "StudyInstanceUID": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "PatientID": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SeriesInstanceUID": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SOPInstanceUID": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SeriesDescription": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SliceThickness": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SliceThickness_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SliceThickness_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SliceThickness_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SeriesNumber": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "StudyDate": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SOPClassUID": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "collection_id": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "AnatomicRegionSequence": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SegmentedPropertyCategoryCodeSequence": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SegmentedPropertyTypeCodeSequence": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "FrameOfReferenceUID": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SegmentNumber": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SegmentNumber_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SegmentNumber_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SegmentNumber_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SegmentAlgorithmType": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "SUVbw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SUVbw_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SUVbw_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SUVbw_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Volume": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Volume_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Volume_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Volume_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Diameter": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Diameter_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Diameter_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Diameter_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Surface_area_of_mesh": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Surface_area_of_mesh_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Surface_area_of_mesh_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Surface_area_of_mesh_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Total_Lesion_Glycolysis": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Total_Lesion_Glycolysis_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Total_Lesion_Glycolysis_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Total_Lesion_Glycolysis_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_First_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_First_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Third_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Fourth_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Percent_Within_Second_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity_Background": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity_Background_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity_Background_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Standardized_Added_Metabolic_Activity_Background_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_First_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Third_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Fourth_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Glycolysis_Within_Second_Quarter_of_Intensity_Range_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "Internal_structure": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Sphericity": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Calcification": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Lobular_Pattern": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Spiculation": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Margin": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Texture": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Subtlety_score": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "Malignancy": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    }
  },
  "$schema": "http://json-schema.org/schema#"
}
