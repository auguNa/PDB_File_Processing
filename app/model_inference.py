import torch
from transformers import AutoModel, AutoTokenizer


def load_model(model_name="facebook/esm2_t6_8M_UR50D"):
    """Loads the protein embedding model."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return model, tokenizer


def infer_sequence(model, tokenizer, sequence):
    """Generates embeddings for a given protein sequence."""
    inputs = tokenizer(sequence, return_tensors="pt", add_special_tokens=True)
    with torch.no_grad():
        outputs = model(**inputs)

    return outputs.last_hidden_state.tolist()  # Convert tensor to list for JSON
