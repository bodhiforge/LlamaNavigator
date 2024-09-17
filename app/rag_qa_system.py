import openai
import gradio as gr
from elasticsearch import Elasticsearch
import os

# Initialize Elasticsearch using the environment variable for the host
es_host = os.getenv("ES_HOST", "http://localhost:9200")
es = Elasticsearch(es_host)

# Set OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dummy data for Elasticsearch index
documents = [
    {"title": "Document 1", "content": "This is the content of document 1."},
    {"title": "Document 2", "content": "This is the content of document 2."},
]

# Index the documents in Elasticsearch (one-time process)
for i, doc in enumerate(documents):
    es.index(index="documents", id=i, body=doc)

# Function to retrieve relevant documents using Elasticsearch
def retrieve_documents(query):
    res = es.search(index="documents", query={"match": {"content": query}})
    hits = res['hits']['hits']
    return [hit["_source"]["content"] for hit in hits]

# Function to generate answer using OpenAI
def generate_answer(question):
    # Step 1: Retrieve relevant documents
    retrieved_docs = retrieve_documents(question)
    context = "\n".join(retrieved_docs)
    
    # Step 2: Generate answer using OpenAI GPT
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)
    answer = response.choices[0].text.strip()
    
    return answer

# Define Gradio interface
def qa_system(question):
    answer = generate_answer(question)
    return answer

# Launch Gradio app
iface = gr.Interface(fn=qa_system, inputs="text", outputs="text", title="RAG QA System")
iface.launch(server_name="0.0.0.0", server_port=7860)
