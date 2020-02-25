COHORT_FILTER_SCHEMA={
  "type": "object",
  "properties": {
    "bioclin_version": {
      "type": "string"
    },
    "imaging_version": {
      "type": "string"
    },
    "attributes": {
      "type": "object",
      "properties": {
        "collection_id": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
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
        "pathlogic_M": {
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
        "tss_code": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "tobacco_smoking_history": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "mononucleotide_and_dinucleotide_marker_panel_analysis_status": {
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
        "is_ffpe": {
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
        "vital_status": {
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
        "age_at_diagnosis": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "tumor_tissue_site": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "histological_site": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "pathological_stage": {
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
        "residual_tumor": {
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
        "days_to_last_known_alive": {
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
        "year_of_diagnosis": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "bmi": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_initial_pathologic_diagnosis": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_birth": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_death": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_initial_pathologic_diagnosis": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_last_followup": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_submitted_specimen_dx": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_examined": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_positive_by_he": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "batch_number": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "age_began_smoking_in_years": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "year_of_tobacco_smoking_onset": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "stopped_smoking_year": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_pack_years_smoked": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "height": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "weight": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "pregnancies": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "hpv_calls": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "gleason_score_combined": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "psa_value": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_collection": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_sample_procurement": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_portions": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_slides": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "avg_percent_lymphocyte_infiltration": {
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
        "avg_percent_necrosis": {
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
        "avg_percent_normal_cells": {
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
        "avg_percent_tumor_cells": {
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
        "max_percent_lymphocyte_infiltration": {
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
        "max_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "max_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "max_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "max_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "max_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_tumor_nuclei": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_lymphocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_monocyte_infiltration": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_necrosis": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_neutrophil_infiltration": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_normal_cells": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_stromal_cells": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "min_percent_tumor_cells": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "bmi_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "year_of_initial_pathologic_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_birth_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_death_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_initial_pathologic_diagnosis_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_last_followup_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_submitted_specimen_dx_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_examined_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_positive_by_he_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "batch_number_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "age_began_smoking_in_years_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "year_of_tobacco_smoking_onset_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "stopped_smoking_year_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_pack_years_smoked_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "height_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "weight_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "pregnancies_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "hpv_calls_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "gleason_score_combined_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "psa_value_lte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_collection_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_sample_procurement_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_portions_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_slides_lte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "avg_percent_lymphocyte_infiltration_lte": {
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
        "avg_percent_necrosis_lte": {
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
        "avg_percent_normal_cells_lte": {
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
        "avg_percent_tumor_cells_lte": {
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
        "max_percent_lymphocyte_infiltration_lte": {
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
        "max_percent_necrosis_lte": {
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
        "max_percent_normal_cells_lte": {
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
        "max_percent_tumor_cells_lte": {
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
        "min_percent_lymphocyte_infiltration_lte": {
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
        "min_percent_necrosis_lte": {
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
        "min_percent_normal_cells_lte": {
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
        "min_percent_tumor_cells_lte": {
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
        "year_of_initial_pathologic_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_birth_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_death_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_initial_pathologic_diagnosis_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_last_followup_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_submitted_specimen_dx_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_examined_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_positive_by_he_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "batch_number_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "age_began_smoking_in_years_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "year_of_tobacco_smoking_onset_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "stopped_smoking_year_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_pack_years_smoked_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "height_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "weight_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "pregnancies_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "hpv_calls_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "gleason_score_combined_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "psa_value_gte": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_collection_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_sample_procurement_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_portions_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_slides_gte": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "avg_percent_lymphocyte_infiltration_gte": {
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
        "avg_percent_necrosis_gte": {
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
        "avg_percent_normal_cells_gte": {
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
        "avg_percent_tumor_cells_gte": {
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
        "max_percent_lymphocyte_infiltration_gte": {
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
        "max_percent_necrosis_gte": {
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
        "max_percent_normal_cells_gte": {
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
        "max_percent_tumor_cells_gte": {
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
        "min_percent_lymphocyte_infiltration_gte": {
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
        "min_percent_necrosis_gte": {
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
        "min_percent_normal_cells_gte": {
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
        "min_percent_tumor_cells_gte": {
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
        "year_of_initial_pathologic_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_birth_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_death_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_initial_pathologic_diagnosis_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_last_followup_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_submitted_specimen_dx_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_examined_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_of_lymphnodes_positive_by_he_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "batch_number_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "age_began_smoking_in_years_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "year_of_tobacco_smoking_onset_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "stopped_smoking_year_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "number_pack_years_smoked_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "height_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "weight_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "pregnancies_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "hpv_calls_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "gleason_score_combined_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "psa_value_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "days_to_collection_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "days_to_sample_procurement_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_portions_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "num_slides_btw": {
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "avg_percent_lymphocyte_infiltration_btw": {
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
        "avg_percent_necrosis_btw": {
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
        "avg_percent_normal_cells_btw": {
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
        "avg_percent_tumor_cells_btw": {
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
        "max_percent_lymphocyte_infiltration_btw": {
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
        "max_percent_necrosis_btw": {
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
        "max_percent_normal_cells_btw": {
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
        "max_percent_tumor_cells_btw": {
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
        "min_percent_lymphocyte_infiltration_btw": {
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
        "min_percent_necrosis_btw": {
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
        "min_percent_normal_cells_btw": {
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
        "min_percent_tumor_cells_btw": {
          "type": "array",
          "items": {
            "type": "number"
          }
        },
        "SOPInstanceUID": {
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
        "StudyInstanceUID": {
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
        "SeriesDescription": {
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
        "SliceThickness": {
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
        "SliceThickness_gte": {
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
        "file_path": {
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
        }
      }
    }
  },
  "$schema": "http://json-schema.org/schema#"
}
