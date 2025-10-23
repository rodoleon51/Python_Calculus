import pandas as pd

# Load the CSV file
csv_file = "C:\\Users\\rodol\\Downloads\\007000754141.csv"

# Try using a more tolerant encoding
df = pd.read_csv(csv_file, encoding='latin1')  # or encoding='cp1252' if that fails

# Save it as an Excel file
excel_file = "C:\\Users\\rodol\\Downloads\\007000754141.xlsx"
df.to_excel(excel_file, index=False)

print(f"File saved as {excel_file}")
