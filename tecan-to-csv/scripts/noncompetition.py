import pandas as pd
import sys

# Ensure the script is called with the correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python script.py <input_csv> <output_csv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read the CSV file
df = pd.read_csv(input_file, header=None)

# Define the block size
block_size = 13

# Split the dataframe into columns of size block_size and reset the index for each split
cols = [df.iloc[:, i:i+block_size].reset_index(drop=True) for i in range(0, df.shape[1], block_size)]

# Rename columns in each split for consistency
for col in cols:
    col.columns = range(col.columns.size)

# Concatenate all the split columns vertically
stacked_df = pd.concat(cols, axis=0, ignore_index=True)

# Drop rows where all elements are NaN
cleaned_df = stacked_df.dropna(how='all')

# Split the cleaned dataframe into blocks of 10 rows each
splits = [cleaned_df.iloc[i:i+10] for i in range(0, len(cleaned_df), 10)]

# Reset index for each split
reset_splits = [split.reset_index(drop=True) for split in splits]

# Initialize an empty dataframe to store the output
output = pd.DataFrame()

# Process each split
for df in reset_splits:
    sample_id = df.iloc[0, 0]
    solvent = df.iloc[0, 3]
    units = df.iloc[1, 0]

    results = []

    for i in range(2, len(df)):
        for j in range(1, len(df.columns)):
            well_name = str(df.iloc[i, 0]) + str(df.columns[j])
            concentration = df.iloc[i, j]
            if pd.notna(concentration):
                result = {
                    "Sample ID": sample_id,
                    "Well Number": well_name,
                    "Concentration": concentration,
                    "Solvent": solvent,
                    "Units": units
                }
                results.append(result)

    temp_df = pd.DataFrame(results)
    output = pd.concat([output, temp_df], ignore_index=True)

# Write the output dataframe to a CSV file
output.to_csv(output_file, index=False)
