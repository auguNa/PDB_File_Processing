import json

def load_mapping(mapping_file="config/mapping.json"):
    """Loads amino acid mapping from 3-letter to 1-letter codes."""
    with open(mapping_file, "r") as file:
        return json.load(file)

def map_amino_acids(chains, mapping):
    """Converts 3-letter amino acid codes to 1-letter codes."""
    mapped_chains = {}

    for chain, amino_acids in chains.items():
        mapped_chains[chain] = [mapping.get(aa, "?") for aa in amino_acids]

    return mapped_chains
