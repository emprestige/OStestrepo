from ehrql import Dataset, case, when
#from ehrql import Dataset
from ehrql.tables.beta.tpp import ( 
  patients, 
  medications,
  ons_deaths,
  addresses, 
  clinical_events,
  practice_registrations
)
from ehrql import codelist_from_csv

dataset = Dataset()

index_date = "2022-01-01"

#get patients who are registered
registered_patients = practice_registrations.for_patient_on(index_date)

#define population 
dataset.define_population(registered_patients.exists_for_patient())
#get patients ages and age groups

dataset.registered = registered_patients.exists_for_patient()
dataset.sex = patients.sex
dataset.age = patients.age_on(index_date)

last_ons_death = ons_deaths.sort_by(ons_deaths.date).first_for_patient() #get death records for patients
dataset.death_date = last_ons_death.date #date of death

#import ethnicity codelist
ethnicity_codelist = codelist_from_csv(
     "codelists/opensafely-ethnicity-snomed-0removed.csv",
     column="snomedcode",
     category_column="Ethnicity",
)

#define latest ethnicity code for patient
dataset.latest_ethnicity_code = (
    clinical_events.where(clinical_events.snomedct_code.is_in(ethnicity_codelist))
    .where(clinical_events.date.is_on_or_before(index_date))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .snomedct_code
)

# #assign this code to a category
# dataset.latest_ethnicity_group = dataset.latest_ethnicity_code.to_category(
#     ethnicity_codelist
# )

#get patients IMD rank
dataset.imd_rounded = addresses.for_patient_on(index_date).imd_rounded


#get rural/urban classification
dataset.rural_urban_classification = addresses.for_patient_on(index_date).rural_urban_classification

# #get patietns practice's pseudonymised identifier
# dataset.practice = practice_registrations.for_patient_on(index_date).practice_pseudo_id

dataset.region = registered_patients.practice_nuts1_region_name
dataset.stp = registered_patients.practice_stp
