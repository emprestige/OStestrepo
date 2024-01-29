# # # # # # # # # # # # # # # # # # # # #
# Purpose: Define the study dates that are used throughout the rest of the project
# Notes:
# This script is separate from the design.R script as the dates are used by the study definition as well as analysis R scripts.
# # # # # # # # # # # # # # # # # # # # #

## create output directories ----
fs::dir_create(here::here("lib", "design"))

# define key dates ----

study_dates <- tibble::lst(
  studystart_date = "2016-03-01", # first possible study entry date (when HES data is first available)
  studyend_date = "2024-01-28", # last study entry dates
  #followupend_date = "2023-10-19", # end of follow-up 
)

jsonlite::write_json(study_dates, path = here("lib", "design", "study-dates.json"), auto_unbox=TRUE, pretty =TRUE)
jsonlite::write_json(study_dates, path = here("analysis", "design", "study-dates.json"), auto_unbox=TRUE, pretty =TRUE)
