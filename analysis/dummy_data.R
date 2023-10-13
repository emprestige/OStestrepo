##create a dummy dataset 

library("tidyverse")
library("arrow")
library("here")
library("glue")

remotes::install_github("https://github.com/wjchulme/dd4d")
library("dd4d")

#define population size for dummy data 
population_size <- 1000

# #get nth largest value from list
# nthmax <- function(x, n=1){
#   dplyr::nth(sort(x, decreasing=TRUE), n)
# }
# 
# nthmin <- function(x, n=1){
#   dplyr::nth(sort(x, decreasing=FALSE), n)
# }

#define index date and study start date 
index_date <- as.Date("2022-01-01")
studystart_date <- as.Date("2016-01-03")

#define index day and study start day
index_day <- 0L
studystart_day <- as.integer(studystart_date - index_date)

#define known variables
known_variables <- c(
  "index_date", "studystart_date",
  "index_day", "studystart_day"
)

#define a list which will contain all of the variables to be simulated
sim_list = lst(
  
  #whether the patient is registered with the practice
  registered = bn_node(
    ~ rbernoulli(n = ..n, p = 0.99),
  ),
  
  #sex of the patient
  sex = bn_node(
    ~ rfactor(n = ..n, levels = c("female", "male", "intersex", "unknown"), 
              p = c(0.51, 0.49, 0, 0)), missing_rate = ~0.001 
  ),
  
  #age of the patient 
  age = bn_node(
    ~ as.integer(rnorm(n = ..n, mean = 60, sd = 14)),
  ),
  
  # #sustainability transformation partnership code (here a pseudocode just represented by a number)
  # stp = bn_node(
  #   ~ factor(as.integer(runif(n = ..n, 1, 36)), levels = 1:36),
  # ),
  
  #whether the participant has diabetes or not 
  diabetes = bn_node(
    ~ rbernoulli(n = ..n, p = plogis(-1 + age*0.02 + I(sex == 'F')*-0.2))*1
  ),
  
  #region the patient lives in 
  region = bn_node(
    variable_formula = ~ rfactor(n = ..n, levels = c(
      "North East",
      "North West",
      "Yorkshire and The Humber",
      "East Midlands",
      "West Midlands",
      "East",
      "London",
      "South East",
      "South West"
    ), p = c(0.2, 0.2, 0.3, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)),
  ),
  
  end_date = bn_node(
    ~ "2023-03-01", keep = FALSE
  ),
  
  #day of death for patient (want most to be alive) 
  death_day = bn_node(
    ~ as.integer(runif(n = ..n, index_day, index_day + 2000)),
    missing_rate = ~ 0.99
  )
)

bn <- bn_create(sim_list, known_variables = known_variables)

bn_plot(bn)
bn_plot(bn, connected_only = TRUE)

set.seed(10)

dummydata <- bn_simulate(bn, pop_size = population_size, keep_all = FALSE, 
                         .id = "patient_id")

dummydata_processed <- dummydata %>%
  #convert logical to integer as study defs output 0/1 not TRUE/FALSE
  #mutate(across(where(is.logical), ~ as.integer(.))) %>%
  #convert integer days to dates since index date and rename vars
  mutate(across(ends_with("_day"), ~ as.Date(as.character(index_date + .)))) %>%
  rename_with(~str_replace(., "_day", "_date"), ends_with("_day"))

fs::dir_create(here("lib", "dummydata"))
write_feather(dummydata_processed, sink = here("lib", "dummydata", "dummyinput.arrow"))
