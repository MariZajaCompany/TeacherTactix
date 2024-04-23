import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Step 1: Open the file and read the lines
with open('data.txt', 'r') as file:
    lines = file.readlines()

data = []

# Step 2: For each line, split the line by commas to get the individual entries
for line in lines:
    entries = line.strip().split(',')
    day_data = []
    # Step 3: For each entry, split by space to separate the keys and the value
    for entry in entries:
        day_data.append(entry)
    data.append(day_data)

# Step 5: Convert the dictionary to a pandas DataFrame for display
df = pd.DataFrame(data)
print(df)

df_str = df.to_string()

# Step 4: Use matplotlib's `table` function to create a table from the string
fig, ax = plt.subplots(figsize=(12, 4)) # set size frame
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, cellLoc = 'center', loc='center')

# Step 5: Save the figure as a PDF
pp = PdfPages("output.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()