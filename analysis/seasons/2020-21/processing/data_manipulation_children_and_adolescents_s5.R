library("tidyverse")
library("here")
library("arrow")
library("ggplot2")
library("data.table")

df_input <- read_feather(
  here::here("output", "seasons", "2020-21", "input_children_and_adolescents_s5.arrow"))

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
    df_input$age >= 2 & df_input$age <= 5 ~ "2-5",
    df_input$age >= 6 & df_input$age <= 9 ~ "6-9",
    df_input$age >= 10 & df_input$age <= 13 ~ "10-13",
    df_input$age >= 14 & df_input$age <= 17 ~ "14-17",
    TRUE ~ NA_character_
  ))

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
write_feather(df_input, here::here("output", "seasons", "2020-21", "input_manipulated_children_and_adolescents_s5.arrow"))
