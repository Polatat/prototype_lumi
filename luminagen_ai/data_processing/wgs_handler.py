# luminagen_ai/data_processing/wgs_handler.py
import pysam

def parse_vcf(file_path):
    """
    Parses a VCF file using pysam and extracts only the pathogenic variants.
    Returns a list of dictionaries, where each dictionary is a pathogenic variant.
    """
    print(f"INFO: Parsing VCF file at {file_path} using pysam...")
    variants = []
    try:
        # Open the VCF file with pysam
        vcf_file = pysam.VariantFile(file_path)
        
        # Iterate over each record in the VCF file
        for record in vcf_file.fetch():
            # Check if the 'GENE' and 'CLNSIG' keys exist in the INFO field
            if 'GENE' in record.info and 'CLNSIG' in record.info:
                
                # --- NEW LOGIC: Check for Clinical Significance ---
                # Get the clinical significance value
                clinical_significance = record.info.get('CLNSIG')

                # FIX: Check if the value is a tuple (for different VCF formats)
                if isinstance(clinical_significance, tuple):
                    clinical_significance = clinical_significance[0]
                
                # Only process the variant if its significance is "Pathogenic"
                if "Pathogenic" in clinical_significance:
                    gene_name = record.info.get('GENE')
                    
                    if isinstance(gene_name, tuple):
                        gene_name = gene_name[0]

                    variant_info = {
                        "gene": gene_name,
                        "chrom": record.chrom,
                        "pos": record.pos,
                        "ref": record.ref,
                        "alt": record.alts[0] # Get the first alternate allele
                    }
                    variants.append(variant_info)
                    
    except Exception as e:
        print(f"ERROR: Failed to parse VCF file. {e}")
        
    print(f"INFO: Found {len(variants)} pathogenic variants with gene information.")
    return variants
