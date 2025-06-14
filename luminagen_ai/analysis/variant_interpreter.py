# luminagen_ai/analysis/variant_interpreter.py
from luminagen_ai import llm  # Import our new llm module

def generate_interpretation(gene_name: str, variant_name: str) -> str:
    """Uses the LLaMA model to generate a clinical interpretation for the report."""
    print(f"INFO: Using AI to generate interpretation for {gene_name}...")

    prompt = f"""
    Q: You are a medical geneticist. Provide a clear, paragraph-long clinical explanation for a report about a pathogenic mutation found in the {gene_name} gene ({variant_name}). Explain what the gene does and the consequences of the mutation.
    A:"""

    interpretation = llm.generate_text(prompt)
    print("INFO: AI interpretation generated.")
    return interpretation

def generate_summary(gene_name: str) -> str:
    """Uses LLaMA to generate a single-sentence result summary for the report header."""
    print(f"INFO: Using AI to generate result summary for {gene_name}...")

    prompt = f"""
    Q: In a single, formal sentence for a medical report's result box, state that a pathogenic mutation was found in the {gene_name} gene.
    A:"""
    summary = llm.generate_text(prompt)
    print("INFO: AI summary generated.")
    return summary