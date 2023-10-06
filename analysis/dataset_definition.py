from ehrql import create_dataset, case, when
from ehrql.tables.beta.tpp import ( 
  patients, 
  medications,
  ons_deaths,
  addresses, 
  clinical_events,
  practice_registrations
)
from ehrql import codelist_from_csv

dataset = create_dataset()

#deine population size
dataset.configure_dummy_data(population_size=1000)

#define population 
dataset.define_population(patients.date_of_birth.is_on_or_before("1999-12-31")) #get patients after certain date

#get patients ages and age groups
dataset.age = patients.age_on("2019-09-01") #get patients age on defined date
dataset.age_band = case(
        when(dataset.age < 20).then("0-19"),
        when(dataset.age < 40).then("20-39"),
        when(dataset.age < 60).then("40-59"),
        when(dataset.age < 80).then("60-79"),
        when(dataset.age >= 80).then("80+"),
        default="missing",
)

last_ons_death = ons_deaths.sort_by(ons_deaths.date).last_for_patient() #get death records for patients
dataset.date_of_death = last_ons_death.date #date of death
dataset.place_of_death = last_ons_death.place #place of death
dataset.cause_of_death = last_ons_death.cause_of_death_01 #cause of death

#import ethnicity codelist
ethnicity_codelist = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column="snomedcode",
    category_column="Grouping_6",
)

#define latest ethnicity code for patient
dataset.latest_ethnicity_code = ( 
    clinical_events.where(clinical_events.snomedct_code.is_in(ethnicity_codelist))
    .where(clinical_events.date.is_on_or_before("2023-01-01"))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .snomedct_code
)
#assign this code to a category
dataset.latest_ethnicity_group = dataset.latest_ethnicity_code.to_category( 
    ethnicity_codelist
)

#get patients IMD rank 
dataset.imd = addresses.for_patient_on("2023-01-01").imd_rounded

#calculate IMD quintile
dataset.imd_quintile = case(
    when((dataset.imd >=0) & (dataset.imd < int(32844 * 1 / 5))).then("1 (most deprived)"),
    when(dataset.imd < int(32844 * 2 / 5)).then("2"),
    when(dataset.imd < int(32844 * 3 / 5)).then("3"),
    when(dataset.imd < int(32844 * 4 / 5)).then("4"),
    when(dataset.imd < int(32844 * 5 / 5)).then("5 (least deprived)"),
    default="unknown"
)

#get rural/urban classification 
dataset.rural_urban = addresses.for_patient_on("2023-01-01").rural_urban_classification

#get patietns practice's pseudonymised identifier
dataset.practice = practice_registrations.for_patient_on("2023-01-01").practice_pseudo_id
