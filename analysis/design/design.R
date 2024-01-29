# # # # # # # # # # # # # # # # # # # # #
# Purpose: creates metadata objects for aspects of the study design
# This script should be sourced (ie `source(".../design.R")`) in the analysis scripts
# # # # # # # # # # # # # # # # # # # # #

# Preliminaries ----

## Import libraries ----
library("tidyverse")
library("here")
library("Epi")

## create output directories ----
fs::dir_create(here("analysis", "design"))


# import globally defined repo variables
study_dates <-
  jsonlite::read_json(path=here("analysis", "design", "study-dates.json")) %>%
  map(as.Date)

#Lexis expansions? 
#Lexis(entry = studystart_date, duration = )
