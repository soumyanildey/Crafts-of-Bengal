from transformers import AutoTokenizer, AutoModel
from datasets import load_dataset
import torch
import faiss

# Load tokenizer and model once
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
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
def get_bot_response(query):
    query_embedding = encode([query]).numpy()
    D, I = index.search(query_embedding, k=1)
    score = D[0][0]
    return answers[I[0][0]] if score >= 0.2 else "I'm not sure about that. Please contact support."
