# import ehrql function for importing codelists
from ehrql import (
  codelist_from_csv
)

# ethnicity codes
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column = "snomedcode",
    category_column = "Grouping_6",
)
ethnicity_codes_16 = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column = "snomedcode",
    category_column = "Grouping_16",
)

# smoking
clear_smoking_codes = codelist_from_csv(
    "codelists/opensafely-smoking-clear.csv",
    column = "CTV3Code",
    category_column = "Category",
)

unclear_smoking_codes = codelist_from_csv(
    "codelists/opensafely-smoking-unclear.csv",
    column = "CTV3Code",
    category_column = "Category",
)

# drinking
drinking_codelist = codelist_from_csv(
  "codelists/user-angel-wong-hazardous-drinking.csv",
  column = "code",
)

# illicit substances 
drug_usage_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-illsub_cod.csv",
  column = "code",
)
drug_intervention_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-illsubint_cod.csv",
  column = "code",
)
drug_assessment_declination_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-illsubassdec_cod.csv",
  column = "code",
)

# asthma diagnosis
asthma_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ast_cod.csv",
    column = "code",
)

# asthma medications
asthma_medications = codelist_from_csv(
  "codelists/opensafely-asthma-inhaler-steroid-medication.csv",
  column = "code",
)

# COPD
copd_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-copd_cod.csv",
  column = "code",
)

# pulmonary fibrosis
pulmonary_fibrosis_codelist = codelist_from_csv(
  "codelists/bristol-ild-snomed.csv",
  column = "code",
)

# hypertension
hypertension_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv",
  column = "code",
)

# type 1 diabetes
type1_diabetes_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-dmtype1_cod.csv",
  column = "code",
)

# non-type 1 diabetes
non_type1_diabetes_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-dmnontype1_cod.csv",
  column = "code",
)

# heart failure
heart_failure_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-hf_cod.csv",
  column = "code",
)

# prior MI
prior_mi_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-mi_cod.csv",
  column = "code",
)
