import os
import json
from src.parser import load_and_sanitize_csv
from src.analytics import calculate_grades_and_metrics
from src.generator import render_report

def main():
    CONFIG_PATH = os.path.join("config", "grading_schema.json")
    DATA_PATH = os.path.join("data", "sample_grades.csv")
    TEMPLATE_DIR = "templates"
    OUTPUT_PATH = os.path.join("outputs", "gradebook_report.html")

    print("=============================================")
    print("      ACADEMIC PERFORMANCE ANALYZER          ")
    print("=============================================\n")

    # 1. Load Configuration Schema
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Error: Configuration file missing at {CONFIG_PATH}")
        return
        
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    required_cols = ["Student_ID", "Student_Name"] + [
        settings["csv_column"] for settings in config["assessments"].values()
    ]

    print("[1/3] Validating and loading CSV dataset...")
    try:
        cleaned_df = load_and_sanitize_csv(DATA_PATH, required_cols)
        print(f"     ✅ Data loaded successfully. Count: {len(cleaned_df)} records.")
    except Exception as e:
        print(f"\n❌ Ingestion Failed: {e}")
        return

    print("[2/3] Analyzing metrics and compiling grading systems...")
    try:
        analytics_results = calculate_grades_and_metrics(cleaned_df, config)
        print("     ✅ Statistical calculations finished.")
    except Exception as e:
        print(f"\n❌ Analytics Processing Failed: {e}")
        return

    print("[3/3] Compiling minimalist HTML UI layout...")
    try:
        render_report(analytics_results, TEMPLATE_DIR, OUTPUT_PATH)
    except Exception as e:
        print(f"\n❌ UI Document Generation Failed: {e}")
        return

if __name__ == "__main__":
    main()