from ehrql import Dataset, case, when
from ehrql.tables.beta.tpp import ( 
  patients, 
  medications,
  ons_deaths,
  addresses, 
  clinical_events,
  practice_registrations,
  household_memberships_2020,
  vaccinations
)
import codelists

dataset = Dataset()

index_date = "2023-10-31"

age_at_start = patients.age_on("2016-03-01")
age_at_end = patients.age_on(index_date)

#get patients who are registered, have sex, age, and imd info
registered_patients = (practice_registrations.for_patient_on(index_date)).exists_for_patient()
is_female_or_male = patients.sex.is_in(["female", "male"])
is_appropriate_age = (age_at_start <= 17) & (age_at_end >= 2)
has_imd = addresses.for_patient_on(index_date).imd_rounded.is_not_null()

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
dataset.age = patients.age_on(index_date)

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

# #get patietns practice's pseudonymised identifier
# dataset.practice = practice_registrations.for_patient_on(index_date).practice_pseudo_id

#practice and patient information
dataset.region = (practice_registrations.for_patient_on(index_date)).practice_nuts1_region_name
dataset.stp = (practice_registrations.for_patient_on(index_date)).practice_stp

#define comorbidity date 
comorbidity_date = "2020-10-01"

#has asthma if there is a recent asthma diagnosis and a medication prescribed 
dataset.has_asthma = (
  clinical_events.where(clinical_events.snomedct_code.is_in(codelists.asthma_codelist))
  .where(clinical_events.date.is_on_or_between(comorbidity_date, index_date))
  .exists_for_patient() & medications.where(medications.dmd_code.
  is_in(codelists.asthma_medications))
  .exists_for_patient()
)

#define reactive airway disease code
reactive_airway_disease = ["266898002"]

#reactive airway disease diagnosis 
dataset.has_reactive_airway = (
  clinical_events.where(clinical_events.snomedct_code.is_in(reactive_airway_disease))
  .where(clinical_events.date.is_on_or_between(comorbidity_date, index_date))
  .exists_for_patient()
)

  
# #diabetes diagnosis
# dataset.has_diabetes = (
#   clinical_events.where(clinical_events.snomedct_code
#   .is_in(codelists.type1_diabetes_codelist))
#   .where(clinical_events.date.is_on_or_between(comorbidity_date, index_date))
#   .exists_for_patient() | clinical_events.where(clinical_events.snomedct_code
#   .is_in(codelists.non_type1_diabetes_codelist))
#   .where(clinical_events.date.is_on_or_between(comorbidity_date, index_date))
#   .exists_for_patient()
# )

#define earliest vaccination date 
vaccination_date = "2022-10-01"

#vaccinations
dataset.flu_vaccination = (
  vaccinations.where(vaccinations.target_disease.is_in(["Influenza"]))
  .sort_by(vaccinations.date)
  .where(vaccinations.date.is_on_or_between(vaccination_date, index_date))
  .exists_for_patient()
)
dataset.covid_vaccination = (
  vaccinations.where(vaccinations.target_disease.is_in(["SARS-COV-2"]))
  .sort_by(vaccinations.date)
  .where(vaccinations.date.is_on_or_before(index_date))
  .exists_for_patient()
)
