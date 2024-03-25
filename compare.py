import pandas as pd

def remove_duplicate_rows(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Remove duplicate rows based on the 'CIN' column
    df.drop_duplicates(subset=['CIN'], keep='first', inplace=True)

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Input and output file paths
    input_file_path = "Pratham(5k to 11k).csv"  # Replace with your input CSV file path
    output_file_path = "output.csv"  # Replace with the desired output CSV file path

    # Remove duplicate rows
    remove_duplicate_rows(input_file_path, output_file_path)
