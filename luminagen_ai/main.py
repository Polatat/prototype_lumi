# luminagen_ai/main.py
from luminagen_ai import llm
from luminagen_ai.analysis import variant_interpreter
from luminagen_ai.reporting import report_generator

def main():
    """Main function to run the complete LuminaGen AI workflow."""
    print("--- Starting LuminaGen AI ---")

    # --- 1. CONFIGURATION ---
    # IMPORTANT: Make sure this path is correct!
    MODEL_PATH = "models/nous-hermes-2-solar-10.7b.Q4_K_M.gguf" 

    # Patient data for this run
    PATIENT_GENE = "PCSK9"
    PATIENT_VARIANT = "c.-73A>G" # Example variant for alpha-thalassemia

    # File paths
    REPORT_TEMPLATE = "report_test.html"
    OUTPUT_REPORT = "final_patient_report.html"

    # --- 2. LOAD THE AI MODEL ---
    # This will only load the model once. Your Mac's GPU will be used.
    llm.load_model(MODEL_PATH)

    # --- 3. RUN AI ANALYSIS ---
    # Use the AI to generate the text content for our report
    summary_text = variant_interpreter.generate_summary(PATIENT_GENE)
    genetic_info_text = variant_interpreter.generate_interpretation(PATIENT_GENE, PATIENT_VARIANT)

    # --- 4. PREPARE DATA FOR REPORT ---
    # This dictionary's keys must match the placeholders in the HTML template
    report_data = {
        "result_summary": summary_text,
        "genetic_information": genetic_info_text
        # We can add more data like patient details, risk scores, etc. here later
    }

    # --- 5. GENERATE THE FINAL HTML REPORT ---
    report_generator.create_html_report(
        template_name=REPORT_TEMPLATE,
        output_path=OUTPUT_REPORT,
        data=report_data
    )

    print(f"--- LuminaGen AI Finished. Open '{OUTPUT_REPORT}' in your browser to see the result. ---")

if __name__ == "__main__":
    main()
