import os
import sys
import csv
import argparse

def union_csv_files(input_files, output_file):
    """
    Unions multiple CSV files with identical headers into a single output CSV file.
    
    Args:
        input_files (list): List of paths to input CSV files
        output_file (str): Path to the output CSV file
    """
    # Validate input files exist
    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"Error: File not found - {file_path}")
            sys.exit(1)
    
    # Read the first file to get headers
    with open(input_files[0], 'r', newline='', encoding='utf-8') as first_file:
        reader = csv.reader(first_file)
        headers = next(reader)
    
    # Open output file and write headers
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        
        # Process each input file
        for file_path in input_files:
            with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                
                # Skip headers for subsequent files
                next(reader)
                
                # Write data rows to output
                for row in reader:
                    writer.writerow(row)
    
    print(f"Successfully combined {len(input_files)} CSV files into {output_file}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Union multiple CSV files with identical headers.')
    parser.add_argument('input_files', nargs='+', help='List of input CSV files to union')
    parser.add_argument('-o', '--output', default='combined.csv', 
                        help='Output CSV file path (default: combined.csv)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call union function
    union_csv_files(args.input_files, args.output)

if __name__ == '__main__':
    main()
