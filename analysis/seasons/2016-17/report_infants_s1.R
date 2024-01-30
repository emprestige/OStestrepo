library("tidyverse")
library("here")
library("arrow")
library("ggplot2")
library("data.table")

df_input <- read_feather(
    here::here("output", "seasons", "2016-17", "input_manipulated_infants_s1.arrow"))

plot_age <- ggplot(data = df_input, aes(age, frequency(age))) + geom_col(width = 0.9) +
  xlab("Age (Months)") + ylab("Frequency")

ggsave(
    plot = plot_age,
    filename = "descriptive_infants_s1.png", path = here::here("output", "seasons", "2016-17"),
)
