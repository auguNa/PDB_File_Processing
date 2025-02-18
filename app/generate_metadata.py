import datetime

def generate_metadata(file_name, chains):
    """Generates metadata for the processed PDB file."""
    return {
        "protein_id": file_name,
        "processing_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "extracted_chains": {chain: len(seq) for chain, seq in chains.items()}
    }
