library("tidyverse")
library("here")
library("arrow")
library("ggplot2")
library("data.table")

df_input <- read_feather(
    here::here("output", "input.arrow"))

# df2 <- rlang::duplicate(df_input)
# df2 <- as.data.table(df2)
# df2 <- df2[is.na(date_of_death) == F, ]
# 
# summary(lm(age ~ latest_ethnicity_group + imd + rural_urban, data = df2))

# plot_age <- ggplot(data = df_input, aes(age)) + geom_histogram()

# ggsave(
#     plot = plot_age,
#     filename = "descriptive.png", path = here::here("output"),
# )
