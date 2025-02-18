import os


def extract_chains(pdb_file: str):
    """
    Extracts the H (Heavy) and L (Light) chains from a PDB file.

    Args:
        pdb_file (str): Path to the PDB file.

    Returns:
        dict: Dictionary with 'H' and 'L' chains containing their amino acid sequences.
    """
    if not os.path.exists(pdb_file):
        raise FileNotFoundError(f"PDB file not found: {pdb_file}")

    chains = {"H": [], "L": []}  # Store extracted residues per chain

    try:
        with open(pdb_file, "r") as f:
            for line in f:
                # Look for ATOM records
                if line.startswith("ATOM"):
                    chain_id = line[21]  # Column 5 in the PDB file
                    residue_name = line[17:20].strip()  # Column 4 (3-letter amino acid code)

                    # Store in corresponding chain (H or L)
                    if chain_id in chains:
                        chains[chain_id].append(residue_name)

        # Remove duplicates while keeping order
        for chain in chains:
            chains[chain] = list(dict.fromkeys(chains[chain]))

        return chains

    except Exception as e:
        raise RuntimeError(f"Error extracting chains: {e}")
