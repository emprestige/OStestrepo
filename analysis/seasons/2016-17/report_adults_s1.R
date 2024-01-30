library("tidyverse")
library("here")
library("arrow")
library("ggplot2")
library("data.table")

df_input <- read_feather(
    here::here("output", "seasons", "2016-17", "input_manipulated_adults_s1.arrow"))

# plot_age <- ggplot(data = df_input, aes(age)) + geom_histogram()

# ggsave(
#     plot = plot_age,
#     filename = "descriptive_s1.png", path = here::here("output", "seasons", "2016-17"),
# )
