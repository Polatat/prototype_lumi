# luminagen_ai/main.py
import base64
from pathlib import Path
import typer  # Import the Typer library

from luminagen_ai import llm
from luminagen_ai.analysis import variant_interpreter
from luminagen_ai.reporting import report_generator
from luminagen_ai.data_processing import wgs_handler

# Create a Typer application instance
app = typer.Typer()

def image_to_base64(file_path: str) -> str:
    """Reads an image file and converts it to a Base64 encoded data URI."""
    try:
        with Path(file_path).open("rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        print(f"WARNING: Logo file not found at {file_path}. Logo will be missing in the report.")
        return ""

# This decorator tells Typer that this function is a command
@app.command()
def run(
    input_vcf: Path = typer.Argument(..., help="Path to the input VCF file for the patient."),
    output_report: Path = typer.Option("patient_report.html", "--output", "-o", help="Path to save the final HTML report.")
):
    """
    Runs the complete LuminaGen AI workflow on a single VCF file.
    """
    print("--- Starting LuminaGen AI ---")
    
    # --- 1. CONFIGURATION ---
    MODEL_PATH = "models/nous-hermes-2-solar-10.7b.Q4_K_M.gguf"
    REPORT_TEMPLATE = "report/report_test02.html"
    LOGO_PATH = "assets/Redix_logo_02.png"
    
    # --- 2. LOAD THE AI MODEL ---
    llm.load_model(MODEL_PATH)
    
    # --- 3. PARSE THE VCF FILE ---
    if not input_vcf.exists():
        print(f"ERROR: Input VCF file not found at '{input_vcf}'")
        raise typer.Exit(code=1)
        
    variants_from_vcf = wgs_handler.parse_vcf(str(input_vcf))
    
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
    logo_data_uri = image_to_base64(LOGO_PATH)

    report_data = {}
    if all_variant_results:
        report_data = {
            "variants_found": True,
            "all_results": all_variant_results,
            "logo_data_uri": logo_data_uri
        }
        print("\nINFO: Pathogenic variants found. Generating detailed report.")
    else:
        report_data = {
            "variants_found": False,
            "result_summary": "No pathogenic mutations were found.",
            "genetic_information": "Based on the provided data, no reportable genetic variants associated with the tested conditions were detected.",
            "logo_data_uri": logo_data_uri
        }
        print("\nINFO: No pathogenic variants found. Generating summary report.")

    report_generator.create_html_report(
        template_name=REPORT_TEMPLATE,
        output_path=str(output_report),
        data=report_data
    )

    print(f"\n--- LuminaGen AI Finished. Check for the generated report file: '{output_report}' ---")

if __name__ == "__main__":
    app()
