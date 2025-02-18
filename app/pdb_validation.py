def validate_pdb(file_path: str):
    required_atoms = {"C", "CA", "O", "N"}  # Required atom types
    found_atoms = set()

    with open(file_path, 'r') as pdb_file:
        for line in pdb_file:
            # Only consider lines that start with "ATOM"
            if line.startswith("ATOM"):
                atom_type = line[12:16].strip()  # Extract atom type from the column
                if atom_type in required_atoms:
                    found_atoms.add(atom_type)

    # Check if all required atom types were found
    missing_atoms = required_atoms - found_atoms
    if missing_atoms:
        raise ValueError(f"PDB validation failed: Missing required atom types: {', '.join(missing_atoms)}")
