import psycopg2
from psycopg2.extras import execute_values
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import nltk
nltk.download('punkt')

# PDF text extraction
def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text_content = []
    for page in reader.pages:
        text_content.append(page.extract_text())
    return text_content

# Text processing
def process_text(text_content):
    text_chunks = []
    for text in text_content:
        sentences = nltk.sent_tokenize(text)
        text_chunks.extend(sentences)
    return text_chunks

# Content embedding
def embed_content(processed_content):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(processed_content)
    return embeddings

# Store embeddings in Postgres
def store_embeddings(embeddings, processed_content):
    conn = psycopg2.connect("postgresql://user:user@localhost:5432/postgres")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pdf_embeddings (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384)
    )
    """)

    execute_values(cur, 
        "INSERT INTO pdf_embeddings (content, embedding) VALUES %s",
        [(content, embedding.tolist()) for content, embedding in zip(processed_content, embeddings)]
    )

    conn.commit()
    cur.close()
    conn.close()

# Retrieve relevant content
def retrieve_relevant_content(query, top_k=5):
    query_embedding = SentenceTransformer('all-MiniLM-L6-v2').encode([query])[0]

    conn = psycopg2.connect("your_connection_string")
    cur = conn.cursor()

    cur.execute(f"""
    SELECT content, embedding <-> %s AS distance
    FROM pdf_embeddings
    ORDER BY distance
    LIMIT {top_k}
    """, (query_embedding.tolist(),))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return [result[0] for result in results]

# Query GPT-4-mini
def query_gpt4_mini(query):
    relevant_content = retrieve_relevant_content(query)
    context = "\n".join(relevant_content)

    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")  # Replace with actual GPT-4-mini model
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")  # Replace with actual GPT-4-mini model

    prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=200, num_return_sequences=1)
    
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Main function to process PDF and set up the system
def setup_pdf_qa_system(pdf_path):
    text_content = extract_pdf_text(pdf_path)
    processed_content = process_text(text_content)
    embeddings = embed_content(processed_content)
    store_embeddings(embeddings, processed_content)
    print("PDF processed and embeddings stored in the database.")

# Main function to query the system
def ask_question(query):
    answer = query_gpt4_mini(query)
    return answer

if __name__ == "__main__":
    print("Welcome to the PDF QA System")
    # Example usage
    pdf_path = "your_pdf_file.pdf"
    
    # Set up the system (run this once for each PDF)
    setup_pdf_qa_system(pdf_path)
    
    # Ask questions
    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        answer = ask_question(query)
        print("Answer:", answer)