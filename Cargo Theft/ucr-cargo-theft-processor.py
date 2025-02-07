import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
import csv

@dataclass
class BatchHeader:
    record_type: str
    state_code: str
    ori: str
    city_name: str
    population_group: str
    country_division: str
    country_region: str
    agency_indicator: str
    core_city: str
    covered_by_ori: str
    fbi_field_office: str
    judicial_district: str
    current_population_1: int
    ucr_county_code_1: str
    msa_code_1: str
    last_population_1: int
    current_population_2: int
    ucr_county_code_2: str
    msa_code_2: str
    last_population_2: int
    current_population_3: int
    ucr_county_code_3: str
    msa_code_3: str
    last_population_3: int
    master_file_year: str
    monthly_activity: str
    agency_name: str

@dataclass
class IncidentReport:
    record_type: str
    ori: str
    agency_name: str
    incident_number: str
    incident_date: str
    data_source: str
    report_date_indicator: str
    incident_hour: str
    cleared_exceptionally: str
    cargo_theft_offense_code: str
    location_code: str
    stolen_property_description_code: str
    stolen_value: float
    recovered_date: str
    recovered_value: float
    unknown_offender: str
    offender_count: str
    arrestee_count: str

def parse_batch_header(line: str) -> BatchHeader:
    return BatchHeader(
        record_type=line[0:2].strip(),
        state_code=line[2:4].strip(),
        ori=line[4:13].strip(),
        city_name=line[13:37].strip(),
        population_group=line[37:39].strip(),
        country_division=line[39:40].strip(),
        country_region=line[40:41].strip(),
        agency_indicator=line[41:42].strip(),
        core_city=line[42:43].strip(),
        covered_by_ori=line[43:52].strip(),
        fbi_field_office=line[52:56].strip(),
        judicial_district=line[56:60].strip(),
        current_population_1=int(line[60:69].strip() or '0'),
        ucr_county_code_1=line[69:72].strip(),
        msa_code_1=line[72:75].strip(),
        last_population_1=int(line[75:84].strip() or '0'),
        current_population_2=int(line[84:93].strip() or '0'),
        ucr_county_code_2=line[93:96].strip(),
        msa_code_2=line[96:99].strip(),
        last_population_2=int(line[99:108].strip() or '0'),
        current_population_3=int(line[108:117].strip() or '0'),
        ucr_county_code_3=line[117:120].strip(),
        msa_code_3=line[120:123].strip(),
        last_population_3=int(line[123:132].strip() or '0'),
        master_file_year=line[132:136].strip(),
        monthly_activity=line[136:148].strip(),
        agency_name=line[148:172].strip()
    )

def parse_incident_report(line: str) -> IncidentReport:
    return IncidentReport(
        record_type=line[0:2].strip(),
        ori=line[2:11].strip(),
        agency_name=line[11:35].strip(),
        incident_number=line[35:47].strip(),
        incident_date=line[47:55].strip(),
        data_source=line[55:56].strip(),
        report_date_indicator=line[56:57].strip(),
        incident_hour=line[57:59].strip(),
        cleared_exceptionally=line[59:60].strip(),
        cargo_theft_offense_code=line[60:63].strip(),
        location_code=line[63:65].strip(),
        stolen_property_description_code=line[128:130].strip(),
        stolen_value=float(line[130:139].strip() or '0'),
        recovered_date=line[139:147].strip(),
        recovered_value=float(line[147:156].strip() or '0'),
        unknown_offender=line[408:410].strip(),
        offender_count=line[410:412].strip(),
        arrestee_count=line[437:439].strip()
    )

def process_file(input_file: str) -> None:
    """
    Function to process a Cargo Theft Master File
    
    Args:
        filepath (str): Path to the input file
    
    Returns:
        None
    """
    # Create output filename
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_processed.csv"
    
    batch_headers: List[BatchHeader] = []
    incident_reports: List[IncidentReport] = []
    
    # Read input file
    with open(input_file, 'r') as f:
        for line in f:
            record_type = line[0:2]
            if record_type == 'BH':
                batch_headers.append(parse_batch_header(line))
            elif record_type == 'IR':
                incident_reports.append(parse_incident_report(line))
    
    # Write batch headers to CSV
    if batch_headers:
        bh_output = f"{base_name}_batch_headers.csv"
        with open(bh_output, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(BatchHeader.__annotations__.keys())
            # Write data
            for bh in batch_headers:
                writer.writerow([getattr(bh, field) for field in BatchHeader.__annotations__.keys()])
        print(f"Batch headers written to: {bh_output}")
    
    # Write incident reports to CSV
    if incident_reports:
        ir_output = f"{base_name}_incident_reports.csv"
        with open(ir_output, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(IncidentReport.__annotations__.keys())
            # Write data
            for ir in incident_reports:
                writer.writerow([getattr(ir, field) for field in IncidentReport.__annotations__.keys()])
        print(f"Incident reports written to: {ir_output}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_filepath>")
        sys.exit(1)
    
    input_filepath = sys.argv[1]
    if not os.path.exists(input_filepath):
        print(f"Error: File '{input_filepath}' not found.")
        sys.exit(1)
    
    try:
        #input_filepath = 'FBI raw data/2020_CT_NATIONAL_MASTER_FILE.txt'
        process_file(input_filepath)
        print("Processing completed successfully.")
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)
