from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import os
import time
import json
import torch  # Import torch for the ESM model
from transformers import EsmModel, EsmTokenizer  # Import the ESM model

from app.pdb_validation import validate_pdb
from app.extract_chains import extract_chains
from app.mapping import load_mapping, map_amino_acids
from app.model_inference import load_model, infer_sequence
from app.generate_metadata import generate_metadata

app = FastAPI()

# Ensure uploads and outputs directories exist
UPLOAD_DIR = "./uploads"
OUTPUT_DIR = "./outputs"  # New directory for saving the output files
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/process-pdb/")
async def process_pdb(file: UploadFile = File(...)):
    """Handles PDB file upload, validation, processing, and model inference."""

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Step 1: Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        start_time = time.time()  # Track processing time

        # Step 2: Validate PDB file
        try:
            validate_pdb(file_path)  # This will raise an exception if validation fails
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"PDB validation failed: {str(ve)}")

        # Step 3: Extract H & L Chains
        chains = extract_chains(file_path)
        print(f"Extracted Chains: {chains}")  # Debugging Output

        # Function to load the mapping.json file
        def load_mapping():
            mapping_file = os.path.join(UPLOAD_DIR, "mapping.json")  # Update to use the uploads directory
            try:
                with open(mapping_file, "r") as file:
                    mapping = json.load(file)
                return mapping
            except FileNotFoundError:
                raise ValueError(f"Mapping file not found in {UPLOAD_DIR}")

        # Function to map three-letter codes to one-letter codes
        def map_amino_acids(chains, mapping):
            mapped_chains = {}
            for chain, residues in chains.items():
                try:
                    mapped_chains[chain] = "".join(mapping[residue] for residue in residues)
                except KeyError as e:
                    raise ValueError(f"Unknown residue in PDB file: {e}")
            return mapped_chains

        # Step 4: Map Amino Acids
        mapping = load_mapping()
        mapped_chains = map_amino_acids(chains, mapping)
        print(f"Mapped Chains: {mapped_chains}")  # Debugging Output

        # Step 5: Run Model Inference
        model, tokenizer = load_model()
        embeddings = {
            chain: infer_sequence(model, tokenizer, "".join(seq))
            for chain, seq in mapped_chains.items()
        }

        # Step 6: Generate Metadata
        metadata = generate_metadata(file.filename, chains)
        metadata["processing_time"] = round(time.time() - start_time, 2)
        metadata["embeddings"] = embeddings
        metadata["original_sequences"] = mapped_chains  # Include original sequences
        metadata["predicted_sequence"] = mapped_chains  # If classification is available, replace this

        # Save the output file
        output_file_path = os.path.join(OUTPUT_DIR, f"{file.filename}_metadata.json")

        # Updated output metadata
        output_metadata = {
            "protein_id": file.filename,
            "processing_date": metadata["processing_date"],
            "extracted_chains": {
                "H": len(chains.get("H", [])),
                "L": len(chains.get("L", []))
            },
            "original_sequences": mapped_chains,  # ✅ Add mapped sequences
            "predicted_sequence": mapped_chains,  # ✅ Include predicted sequences
            "processing_time": metadata["processing_time"],
            "embeddings": embeddings
        }

        # Save metadata to JSON file
        with open(output_file_path, "w") as outfile:
            json.dump(output_metadata, outfile, indent=4)

        # Return the response
        return {
            "message": "Processing complete",
            "metadata": output_metadata,
            "output_file": output_file_path
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during processing: {str(e)}")
