library("tidyverse")
library("here")
library("arrow")
library("ggplot2")
library("data.table")

df_input <- read_feather(
  here::here("output", "seasons", "2018-19", "input_infants_subgroup_s3.arrow"))

#assign ethnicity group
df_input <- df_input %>%
  mutate(
    latest_ethnicity_group = ifelse(df_input$latest_ethnicity_code == "1", "White",
                             ifelse(df_input$latest_ethnicity_code == "2", "Mixed",
                             ifelse(df_input$latest_ethnicity_code == "3", "Asian or Asian British",
                             ifelse(df_input$latest_ethnicity_code == "4", "Black or Black British",
                             ifelse(df_input$latest_ethnicity_code == "5", "Other Ethnic Groups", "Unknown"))))
  ))

#calculate age bands
df_input <- df_input %>%
  mutate(age_band = case_when(
    df_input$age >= 0 & df_input$age <= 2 ~ "0-2m",
    df_input$age >= 3 & df_input$age <= 5 ~ "3-5m",
    df_input$age >= 6 & df_input$age <= 11 ~ "6-11m",
    df_input$age >= 12 & df_input$age <= 23 ~ "12-23m",
    TRUE ~ NA_character_
  ))

# #calculate gestational age bands
# df_input <- df_input %>%
#   mutate(gestational_age_band = case_when(
#     df_input$gestational_age < 35 ~ "<35w",
#     df_input$gestational_age >= 35 & df_input$gestational_age <= 36 ~ "35-36w",
#     df_input$gestational_age >= 37 & df_input$gestational_age <= 40 ~ "37-40w",
#     df_input$gestational_age >= 41 ~ ">=41w",
#     TRUE ~ NA_character_
#   ))

#calculate IMD quintile
df_input <- df_input %>%
  mutate(imd_quintile = case_when(
    df_input$imd_rounded >= 0 & df_input$imd_rounded < as.integer(32800 * 1 / 5) ~ "1",
    df_input$imd_rounded < as.integer(32800 * 2 / 5) ~ "2",
    df_input$imd_rounded < as.integer(32800 * 3 / 5) ~ "3",
    df_input$imd_rounded < as.integer(32800 * 4 / 5) ~ "4",
    df_input$imd_rounded < as.integer(32800 * 5 / 5) ~ "5 (least deprived)",
    TRUE ~ NA_character_
  ))

#write the new input file
write_feather(df_input, here::here("output", "seasons", "2018-19", "input_manipulated_infants_subgroup_s3.arrow"))
