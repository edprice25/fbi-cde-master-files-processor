import pandas as pd
import numpy as np
import os

def parse_human_trafficking_file(filepath):
    """
    Parse FBI Human Trafficking Master File
    
    Args:
        filepath (str): Path to the text file
    
    Returns:
        pandas.DataFrame: Parsed and processed data
    """
    # Define column specifications based on the master file layout
    column_specs = [
        # Header Information
        ('file_identifier', 0, 1, str),
        ('state_code', 1, 3, str),
        ('ori_code', 3, 10, str),
        ('population_group', 10, 12, str),
        ('division', 12, 13, str),
        ('year', 13, 15, str),
        ('sequence_number', 15, 20, str),
        ('core_city_indication', 20, 21, str),
        ('covered_by', 21, 28, str),
        ('covered_by_group', 28, 29, str),
        ('field_office', 29, 33, str),
        ('months_reported', 33, 35, str),
        ('agency_count', 35, 36, str),
        ('population', 36, 45, str),
        ('agency_name', 45, 69, str),
        ('agency_state', 69, 75, str),
    ]
    
    # Monthly report code columns
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    
    # Add report code columns
    for month in months:
        column_specs.append((f'{month}_report_code', len(column_specs), len(column_specs)+1, str))
    
    # Monthly data columns for all 12 months
    for month in months:
        month_offset = 87 + (months.index(month) * 75)  # Calculate offset for each month
        monthly_columns = [
            (f'{month}_offenses_commercial_sex_acts', month_offset, month_offset+5, str),
            (f'{month}_offenses_involuntary_servitude', month_offset+5, month_offset+10, str),
            (f'{month}_offenses_grand_total', month_offset+10, month_offset+15, str),
            (f'{month}_unfounded_commercial_sex_acts', month_offset+15, month_offset+20, str),
            (f'{month}_unfounded_involuntary_servitude', month_offset+20, month_offset+25, str),
            (f'{month}_unfounded_grand_total', month_offset+25, month_offset+30, str),
            (f'{month}_actual_offenses_commercial_sex_acts', month_offset+30, month_offset+35, str),
            (f'{month}_actual_offenses_involuntary_servitude', month_offset+35, month_offset+40, str),
            (f'{month}_actual_offenses_grand_total', month_offset+40, month_offset+45, str),
            (f'{month}_cleared_offenses_commercial_sex_acts', month_offset+45, month_offset+50, str),
            (f'{month}_cleared_offenses_involuntary_servitude', month_offset+50, month_offset+55, str),
            (f'{month}_cleared_offenses_grand_total', month_offset+55, month_offset+60, str),
            (f'{month}_clearances_under_18_commercial_sex_acts', month_offset+60, month_offset+65, str),
            (f'{month}_clearances_under_18_involuntary_servitude', month_offset+65, month_offset+70, str),
            (f'{month}_clearances_under_18_grand_total', month_offset+70, month_offset+75, str)
        ]
        column_specs.extend(monthly_columns)
    
    # Prepare column names and types
    column_names = [spec[0] for spec in column_specs]
    column_types = {spec[0]: spec[3] for spec in column_specs}
    
    # Read fixed-width file
    df = pd.read_fwf(
        filepath, 
        widths=[spec[2]-spec[1] for spec in column_specs],
        names=column_names,
        dtype=column_types,
        header=None
    )
    
    return df

def process_file(filepath):
    """
    Function to process a Human Trafficking Master File
    
    Args:
        filepath (str): Path to the input file
    
    Returns:
        pandas.DataFrame: Processed data
    """
    # Parse the file
    df = parse_human_trafficking_file(filepath)
    
    # Basic cleaning and preprocessing
    #df['state_name'] = df['agency_state'].str.strip()
    df['agency_name'] = df['agency_name'].str.strip()
    
    # Convert year to full year
    #df['full_year'] = '20' + df['year']
    
    # Generate output filename
    input_dir = os.path.dirname(filepath)
    input_filename = os.path.basename(filepath)
    output_filename = f"{os.path.splitext(input_filename)[0]}_processed.csv"
    output_filepath = os.path.join(input_dir, output_filename)
    
    # Save to CSV
    df.to_csv(output_filepath, index=False)
    print(f"Processed file saved to: {output_filepath}")
    
    return df

# Example usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_filepath>")
        sys.exit(1)
    
    input_filepath = sys.argv[1]
    if not os.path.exists(input_filepath):
        print(f"Error: File '{input_filepath}' not found.")
        sys.exit(1)

    #input_filepath = 'FBI raw data/2020_HT_NATIONAL_MASTER_FILE.txt'
    processed_data = process_file(input_filepath)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(processed_data.head())
