# luminagen_ai/main.py
from data_processing import wgs_handler
from analysis import variant_interpreter
from reporting import report_generator

def main():
    """Main function to run the LuminaGen AI workflow."""
    print("--- Starting LuminaGen AI Prototype ---")
    
    # 1. Load Data
    patient_data = wgs_handler.load_data("data/raw/sample_patient_001.wgs")
    
    # 2. Analyze Data
    interpretation = variant_interpreter.analyze_variants(patient_data)
    
    # 3. Generate Report
    report_generator.create_report(interpretation, patient_id="001")
    
    print("--- LuminaGen AI Prototype Finished ---")

if __name__ == "__main__":
    main()

