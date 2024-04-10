""" Extract tables from PDF file and save them as CSV files. """
import tabula
import sys
import os
import pandas as pd

OUTPUT_PATH = "data/table.csv"

if not os.getenv('JAVA_HOME', ''):
    print("Please set JAVA_HOME environment variable.", file=sys.stderr)
    sys.exit(1)

# get file name from arguments
if len(sys.argv) > 1:  # if there is an argument
    file = sys.argv[1]
else:
    file = "data/src.pdf"


print(f"Extracting tables from: {file}")
try:
    # Read PDF file
    tables = tabula.read_pdf(file, pages="all", multiple_tables=True, lattice=True)
except FileNotFoundError:
    print(f"The file: {file}, does not exist.", file=sys.stderr)
    sys.exit(1)

if not tables:
    print("No tables found.", file=sys.stderr)
    sys.exit(1)

# Convert extracted tables into CSV file
for i, table in enumerate(tables):
    # Set the second row as the header
    # table.columns = table.iloc[0]
    table.to_csv(f"data/table_{i}.csv", index=False)

# Combine all the tables into one
with open("data/table_0.csv", "r", encoding='utf-8') as f:
    lines = f.readlines()[1:]

for i in range(1, len(tables)):
    with open(f"data/table_{i}.csv", "r", encoding='utf-8') as f:
        lines += f.readlines()[2:]

lines = [line.replace(",,,", "") for line in lines]

with open(OUTPUT_PATH, "w+", encoding='utf-8') as f:
    f.write("מורה,חדר,שעות,יום,סמס,בהמתנה,בפעל,מכסה,שש,נז,שם שעור,של,קוד שעור\n")
    f.writelines(lines)

# Delete the rest of the files
for i in range(len(tables)):
    os.remove(f"data/table_{i}.csv")

print("Finished extracting tables.")

# Clean the data
df = pd.read_csv(OUTPUT_PATH, encoding="utf-8")
df = df.replace('\r\n', ' ', regex=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

print("Finished cleaning data.")

print(f"\n ~ the output file is: {OUTPUT_PATH} ~")
