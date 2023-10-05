from ehrql import create_dataset, case, when
from ehrql.tables.beta.tpp import patients, medications, ons_deaths
from ehrql.tables.beta.core import clinical_events
from ehrql import codelist_from_csv

dataset = create_dataset()

dataset.define_population(patients.date_of_birth.is_on_or_before("1999-12-31")) #get patients after certain date

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
    "codelists/ethnicity_codelist_with_categories.csv",
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
latest_ethnicity_group = dataset.latest_ethnicity_code.to_category( 
    ethnicity_codelist
)

asthma_codes = ["39113311000001107", "39113611000001102"]
latest_asthma_med = (
    medications.where(medications.dmd_code.is_in(asthma_codes))
    .sort_by(medications.date)
    .last_for_patient()
)

dataset.asthma_med_date = latest_asthma_med.date
dataset.asthma_med_code = latest_asthma_med.dmd_code
