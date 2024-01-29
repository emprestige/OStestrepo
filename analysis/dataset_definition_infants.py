import json
from pathlib import Path 

from datetime import date, datetime
from ehrql import Dataset, case, when
from ehrql.tables.tpp import ( 
  patients, 
  medications,
  ons_deaths,
  addresses, 
  clinical_events,
  practice_registrations,
  household_memberships_2020,
  vaccinations,
  apcs
)
import codelists

dataset = Dataset()

#######################################################################################
# Import study dates defined in "./analysis/design/study-dates.R" script and then exported
# to JSON
#######################################################################################
study_dates = json.loads(
    Path("analysis/design/study-dates.json").read_text(),
)

# Change these in ./analysis/design/study-dates.R if necessary
studystart_date = study_dates["studystart_date"]
studyend_date = study_dates["studyend_date"]
#followupend_date = study_dates["followupend_date"]
index_date = studystart_date

age_months = (index_date - patients.date_of_birth).months
age_at_start = (studystart_date - patients.date_of_birth).months

#get patients who are registered, have sex, age, and imd info
registered_patients = (practice_registrations.for_patient_on(index_date)).exists_for_patient()
is_female_or_male = patients.sex.is_in(["female", "male"])
is_appropriate_age = (age_at_start <= 23)
has_imd = (addresses.for_patient_on(index_date).imd_rounded.is_not_null())

#define population
dataset.define_population(
  registered_patients
  & is_female_or_male
  & is_appropriate_age
  & has_imd
)

#registration, sex and age 
dataset.registered = registered_patients
dataset.sex = patients.sex
dataset.age = age_months

#define entrance and exit to study
dataset.patientstart_date = practice_registrations.start_date
dataset.patientend_date = practice_registrations.end_date


#last_ons_death = ons_deaths.sort_by(ons_deaths.date).first_for_patient() #get death records for patients
dataset.death_date = ons_deaths.date #date of death

#define latest ethnicity code for patient
dataset.latest_ethnicity_code = (
  clinical_events.where(clinical_events.snomedct_code.is_in(codelists.ethnicity_codes))
  .where(clinical_events.date.is_on_or_before(index_date))
  .sort_by(clinical_events.date)
  .last_for_patient()
  .snomedct_code
)

#get patients IMD rank
dataset.imd_rounded = addresses.for_patient_on(index_date).imd_rounded

#get rural/urban classification
dataset.rural_urban_classification = addresses.for_patient_on(index_date).rural_urban_classification

#get patients household info
dataset.household_pseudo_id = household_memberships_2020.household_pseudo_id
dataset.household_size = household_memberships_2020.household_size

#get patietns practice's pseudonymised identifier
dataset.practice_pseudo_id = practice_registrations.for_patient_on(index_date).practice_pseudo_id

#practice and patient information
dataset.region = (practice_registrations.for_patient_on(index_date)).practice_nuts1_region_name
dataset.stp = (practice_registrations.for_patient_on(index_date)).practice_stp

##outcomes

#rsv primary
dataset.rsv_primary = (
  clinical_events.where(clinical_events.ctv3_code
  .is_in(codelists.covid_primary_codelist)) #change codelist when available
  .exists_for_patient()
)

#rsv secondary
dataset.rsv_secondary = (
  apcs.where(apcs.primary_diagnosis
  .is_in(codelists.covid_secondary_codelist)) #change codelist when available
  .exists_for_patient()
  |apcs.where(apcs.secondary_diagnosis
  .is_in(codelists.covid_secondary_codelist)) #change codelist when available
  .exists_for_patient()
)

#covid primary 
dataset.covid_primary = (
  clinical_events.where(clinical_events.ctv3_code
  .is_in(codelists.covid_primary_codelist))
  .exists_for_patient()
)

#covid secondary
dataset.covid_secondary = (
  apcs.where(apcs.primary_diagnosis
  .is_in(codelists.covid_secondary_codelist))
  .exists_for_patient()
  |apcs.where(apcs.secondary_diagnosis
  .is_in(codelists.covid_secondary_codelist))
  .exists_for_patient()
)

#flu primary 
dataset.flu_primary = (
  clinical_events.where(clinical_events.ctv3_code
  .is_in(codelists.covid_primary_codelist)) #change codelist when available
  .exists_for_patient()
)

#flu secondary
dataset.flu_secondary = (
  apcs.where(apcs.primary_diagnosis
  .is_in(codelists.covid_secondary_codelist)) #change codelist when available
  .exists_for_patient()
  |apcs.where(apcs.secondary_diagnosis
  .is_in(codelists.covid_secondary_codelist)) #change codelist when available
  .exists_for_patient()
)
