library("tidyverse")
library("here")
library("arrow")
library("ggplot2")
library("data.table")

df_input <- read_feather(
    here::here("output", "seasons", "2022-23", "input_manipulated_children_and_adolescents_s7.arrow"))

# plot_age <- ggplot(data = df_input, aes(age)) + geom_histogram()

# ggsave(
#     plot = plot_age,
#     filename = "descriptive_s7.png", path = here::here("output", "seasons", "2022-23"),
# )
