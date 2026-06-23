import pandas as pd
import numpy as np

def calculate_grades_and_metrics(df: pd.DataFrame, config: dict) -> dict:
    """
    Normalizes raw grades, computes weighted totals, assigns letter grades,
    and returns a summary dictionary of class metrics and processed data.
    """
    processed_df = df.copy()
    assessments = config["assessments"]
    passing_threshold = config["passing_threshold_pct"]
    
    # 1. Normalize Scores and Calculate Final Weighted Percentage
    processed_df["Final_Weighted_Pct"] = 0.0
    
    for key, settings in assessments.items():
        col_name = settings["csv_column"]
        max_marks = settings["max_marks"]
        weight = settings["weight_pct"]
        
        # Create normalized percentage column for each assessment type
        norm_col = f"{col_name}_Norm_Pct"
        processed_df[norm_col] = (processed_df[col_name] / max_marks) * 100
        
        # Accumulate the weighted contribution to the final grade
        processed_df["Final_Weighted_Pct"] += processed_df[norm_col] * (weight / 100)

    # 2. Assign Letter Grades based on scale mapping
    def map_letter_grade(pct):
        for rule in config["grading_scale"]:
            if pct >= rule["min_pct"]:
                return rule["grade"]
        return "F"

    processed_df["Letter_Grade"] = processed_df["Final_Weighted_Pct"].apply(map_letter_grade)

    # 3. Identify At-Risk Students (Below passing threshold)
    processed_df["At_Risk"] = processed_df["Final_Weighted_Pct"] < passing_threshold
    at_risk_students = processed_df[processed_df["At_Risk"]][["Student_ID", "Student_Name", "Final_Weighted_Pct"]].to_dict(orient="records")

    # 4. Generate Class-Wide Statistical Metrics
    final_grades = processed_df["Final_Weighted_Pct"]
    
    class_metrics = {
        "class_average": round(final_grades.mean(), 2),
        "class_median": round(final_grades.median(), 2),
        "class_std_dev": round(final_grades.std(), 2) if len(final_grades) > 1 else 0.0,
        "pass_rate_pct": round((final_grades >= passing_threshold).sum() / len(final_grades) * 100, 2),
        "total_students": len(processed_df)
    }

    # 5. Extract Category Performance (Raw vs Normalized Averages)
    component_metrics = []
    for key, settings in assessments.items():
        col_name = settings["csv_column"]
        max_marks = settings["max_marks"]
        
        raw_avg = processed_df[col_name].mean()
        norm_avg = processed_df[f"{col_name}_Norm_Pct"].mean()
        
        component_metrics.append({
            "category": key,
            "max_marks": max_marks,
            "weight": settings["weight_pct"],
            "raw_average": round(raw_avg, 2),
            "norm_average": round(norm_avg, 2)
        })

    # Return everything structured neatly for the HTML generator
    return {
        "class_metrics": class_metrics,
        "component_metrics": component_metrics,
        "at_risk_students": at_risk_students,
        "student_data": processed_df.to_dict(orient="records")
    }