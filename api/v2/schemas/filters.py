COHORT_FILTERS_SCHEMA={
  "type": "object",
  "properties": {
    "project_short_name": {
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
    "age_at_diagnosis_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "age_at_diagnosis_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "age_at_diagnosis_btwe": {
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
    "pathologic_stage": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "tumor_tissue_site": {
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
    "histological_type": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
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
    "bmi_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "bmi_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "bmi_btwe": {
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
    "Apparent_Diffusion_Coefficient_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Apparent_Diffusion_Coefficient_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Apparent_Diffusion_Coefficient_btwe": {
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
    },
    "Modality": {
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
    "Volume_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Volume_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Volume_btwe": {
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
    "Diameter_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Diameter_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Diameter_btwe": {
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
    "Surface_area_of_mesh_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Surface_area_of_mesh_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Surface_area_of_mesh_btwe": {
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
    "BodyPartExamined": {
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
    "SliceThickness_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "SliceThickness_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "SliceThickness_btwe": {
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
    "Manufacturer": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "ManufacturerModelName": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "license_short_name": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "analysis_results_id": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "SamplesPerPixel": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "Volume_of_Mesh": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Volume_of_Mesh_lt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Volume_of_Mesh_lte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Volume_of_Mesh_btw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Volume_of_Mesh_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Volume_of_Mesh_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Volume_of_Mesh_btwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Volume_of_Mesh_gte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Volume_of_Mesh_gt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Sphericity_quant": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Sphericity_quant_lt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Sphericity_quant_lte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Sphericity_quant_btw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Sphericity_quant_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Sphericity_quant_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Sphericity_quant_btwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "Sphericity_quant_gte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "Sphericity_quant_gt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "illuminationType": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "primaryAnatomicStructure": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "ObjectiveLensPower": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "min_PixelSpacing": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "min_PixelSpacing_lt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "min_PixelSpacing_lte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "min_PixelSpacing_btw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "min_PixelSpacing_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "min_PixelSpacing_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "min_PixelSpacing_btwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "min_PixelSpacing_gte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "min_PixelSpacing_gt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixColumns": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixColumns_lt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixColumns_lte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixColumns_btw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixColumns_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixColumns_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixColumns_btwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixColumns_gte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixColumns_gt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixRows": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixRows_lt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixRows_lte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixRows_btw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixRows_ebtw": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixRows_ebtwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixRows_btwe": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "max_TotalPixelMatrixRows_gte": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "max_TotalPixelMatrixRows_gt": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "minItems": 1,
      "maxItems": 1
    },
    "CancerType": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  },
  "additionalProperties": False,
  "$schema": "http://json-schema.org/schema#"
}