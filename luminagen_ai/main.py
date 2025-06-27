# luminagen_ai/main.py
import base64 # Import the standard base64 library
from pathlib import Path # A modern way to handle file paths

from luminagen_ai import llm
from luminagen_ai.analysis import variant_interpreter
from luminagen_ai.reporting import report_generator
from luminagen_ai.data_processing import wgs_handler

def image_to_base64(file_path: str) -> str:
    """
    Reads an image file and converts it to a Base64 encoded data URI.
    This allows the image to be embedded directly into the HTML file.
    """
    try:
        # Read the image file in binary mode
        with Path(file_path).open("rb") as f:
            # Encode the binary data to a base64 string
            encoded_string = base64.b64encode(f.read()).decode()
            # Return the complete data URI string for the HTML src attribute
            return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        print(f"WARNING: Logo file not found at {file_path}. Logo will be missing in the report.")
        return ""

def main():
    """Main function to run the complete LuminaGen AI workflow."""
    print("--- Starting LuminaGen AI ---")
    
    # --- 1. CONFIGURATION ---
    MODEL_PATH = "models/nous-hermes-2-solar-10.7b.Q4_K_M.gguf"
    INPUT_VCF = "data/my_test_variants.vcf"
    REPORT_TEMPLATE = "report/report_test02.html"
    OUTPUT_REPORT = "output/patient_report.html"
    LOGO_PATH = "assets/Redix_logo_02.png" # <-- Path to your logo file
    
    # --- 2. LOAD THE AI MODEL ---
    llm.load_model(MODEL_PATH)
    
    # --- 3. PARSE THE VCF FILE ---
    variants_from_vcf = wgs_handler.parse_vcf(INPUT_VCF)
    
    # --- 4. PROCESS ALL VARIANTS AND COLLECT RESULTS ---
    all_variant_results = []
    if variants_from_vcf:
        print(f"\n--- Found {len(variants_from_vcf)} variants. Analyzing all... ---")
        for i, variant in enumerate(variants_from_vcf):
            gene = variant['gene']
            variant_details = f"chr{variant['chrom']}:{variant['pos']}{variant['ref']}>{variant['alt']}"
            print(f"Processing Variant {i+1}: Gene={gene}")
            summary = variant_interpreter.generate_summary(gene)
            interpretation = variant_interpreter.generate_interpretation(gene, variant_details)
            all_variant_results.append({
                "summary": summary,
                "interpretation": interpretation
            })

    # --- 5. PREPARE DATA AND GENERATE A SINGLE REPORT ---
    logo_data_uri = image_to_base64(LOGO_PATH) # <-- Convert your logo to a Base64 string

    report_data = {}
    if all_variant_results:
        report_data = {
            "variants_found": True,
            "all_results": all_variant_results,
            "logo_data_uri": logo_data_uri # <-- Add the logo string to the report data
        }
        print("\nINFO: Pathogenic variants found. Generating detailed report.")
    else:
        report_data = {
            "variants_found": False,
            "result_summary": "No pathogenic mutations were found.",
            "genetic_information": "Based on the provided data, no reportable genetic variants associated with the tested conditions were detected.",
            "logo_data_uri": logo_data_uri # <-- Add the logo string here as well
        }
        print("\nINFO: No pathogenic variants found. Generating summary report.")

    report_generator.create_html_report(
        template_name=REPORT_TEMPLATE,
        output_path=OUTPUT_REPORT,
        data=report_data
    )

    print(f"\n--- LuminaGen AI Finished. Check for the generated report file: '{OUTPUT_REPORT}' ---")

if __name__ == "__main__":
    main()
