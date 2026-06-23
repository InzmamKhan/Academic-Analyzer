import os
import pandas as pd

def load_and_sanitize_csv(file_path: str, required_columns: list) -> pd.DataFrame:
    """
    Loads a student grades CSV file, validates its existence and columns,
    and sanitizes the data for the analytics engine.
    """
    # 1. Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The gradebook file was not found at '{file_path}'")
    
    # 2. Ingest CSV file
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error: Failed to parse the CSV file. Details: {e}")
    
    # Clean column names (strip whitespace)
    df.columns = df.columns.str.strip()
    
    # 3. Validate presence of required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise KeyError(
            f"Error: Missing required columns in CSV: {missing_cols}. "
            f"Found columns: {list(df.columns)}"
        )
    
    # 4. Data Sanitization
    # Clean core identifier strings
    df['Student_ID'] = df['Student_ID'].astype(str).str.strip()
    df['Student_Name'] = df['Student_Name'].astype(str).str.strip()
    
    # Ensure numeric columns are strictly numeric, filling missing values (NaN) with 0
    # (Real gradebooks often leave empty fields for missed tests)
    for col in required_columns:
        if col not in ['Student_ID', 'Student_Name']:
            # coerce turns non-numeric junk strings into NaN, then fillna(0) makes them zeroes
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            
    return df