library("tidyverse")
library("here")
library("arrow")

df_input <- read_feather(
    here::here("output", "input.feather"))

plot_age <- ggplot(data = df_input, aes(df_input$age)) + geom_histogram()

ggsave(
    plot = plot_age,
    filename = "descriptive.png", path = here::here("output"),
)
