import csv

def remove_column_data(csv_file, column_name):
    # Read the CSV file and store its data
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = [{field: row[field] if field != column_name else '' for field in fieldnames} for row in reader]

    # Write the modified data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Example usage:
csv_file = 'galat.csv'  # Replace 'example.csv' with your CSV file name
column_name = 'EMAIL'      # Specify the column name you want to remove data from
remove_column_data(csv_file, column_name)
print(f"All data for column '{column_name}' has been removed from the CSV file.")


