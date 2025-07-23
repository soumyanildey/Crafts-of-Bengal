from transformers import AutoTokenizer, AutoModel
from datasets import load_dataset
import torch
import faiss
from optimum.intel.openvino import OVModelForCausalLM
import os
from transformers import pipeline
import re

# Relative to the current script's location
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "ov_model_llama_3.2")


# Load tokenizer from the same folder
llm_tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load the OpenVINO optimized model
llm_model = OVModelForCausalLM.from_pretrained(model_path)


# Load tokenizer and model once
tokenizer = AutoTokenizer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def encode(texts):
    tokens = tokenizer(texts, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**tokens)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings / embeddings.norm(p=2, dim=1, keepdim=True)


# Load dataset and build FAISS index
faq = load_dataset("Andyrasika/Ecommerce_FAQ")
answers = list(faq['train']['answer'])
embeddings = encode(answers)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings.numpy())

qa_pipeline = pipeline("text-generation", model=llm_model, tokenizer=llm_tokenizer)

def generate_response(context, query):
    # Gemma-style formatted prompt (single-turn enforced)
    formatted = (
        "<|start_header_id|>system<|end_header_id|>\n\n"
        "You are a polite assistant answering only from the given context. "
        "Answer ecommerce customer query service related only. "
        "If someone greets or is rude, respond politely. If context is missing, reply intelligently and precisely to the point or direct them to Customer Support.\n\n"
        "<|eot_id|>\n"
        "<|start_header_id|>user<|end_header_id|>\n\n"
        f"Context:\n{context}\n\nUser Input:\n{query}\n\n"
        "<|eot_id|>\n"
        "<|start_header_id|>assistant<|end_header_id|>\n\n"
    )

    outputs = qa_pipeline(
        formatted,
        return_full_text=False,
        max_new_tokens=100,
        eos_token_id=llm_tokenizer.eos_token_id,
    )

    generated_text = outputs[0]["generated_text"]

    # Only keep text until the next tag or special token
    for stop_token in ["<|eot_id|>", "<|start_header_id|>", "<|end_header_id|>"]:
        if stop_token in generated_text:
            generated_text = generated_text.split(stop_token)[0]

    return generated_text.strip()



def get_bot_response(query, top_k=5):
    # Normalize query
    query_clean = query.strip().lower()

    # Embed and retrieve from FAISS
    query_embedding = encode([query_clean]).numpy()
    D, I = index.search(query_embedding, k=top_k)

    # Extract relevant contexts
    contexts = [answers[i] for i in I[0] if D[0][list(I[0]).index(i)] >= 0.5]
    context = "\n".join(contexts)

    # Generate response from model
    answer = generate_response(context, query)
    return answer
