import os
import fitz  # PyMuPDF
import docx
import extract_msg

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_msg(file_path):
    msg = extract_msg.Message(file_path)
    return msg.body

def chunk_text(text, max_chars=6000):
    chunks = []
    while len(text) > max_chars:
        split_point = text.rfind('\n', 0, max_chars)
        if split_point == -1:
            split_point = max_chars
        chunks.append(text[:split_point].strip())
        text = text[split_point:].strip()
    if text:
        chunks.append(text)
    return chunks

def extract_and_chunk(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        raw_text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        raw_text = extract_text_from_txt(file_path)
    elif ext == ".msg":
        raw_text = extract_text_from_msg(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return chunk_text(raw_text)

# 🔽 Example usage
if __name__ == "__main__":
    file = input("Enter the file path: ")
    chunks = extract_and_chunk(file)
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n")
        print(chunk)# Print the first 500 characters for preview
