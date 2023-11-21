## summarise dataset

import pandas as pd
import pyarrow as pa

dataframe = pd.read_feather("output/input_children_and_adolescents.arrow")
num_rows = len(dataframe)

with open("output/summary_children_and_adolescents.txt", "w") as f:
    f.write(f"There are {num_rows} patients in the population\n")
