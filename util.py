from openai import OpenAI
import nltk
from nltk.tokenize import sent_tokenize

# Ensure that the required Punkt tokenizer resource is available
nltk.download('punkt')

def chunk_text(text, max_chunk_size=4000):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Initialize variables to store the chunks and the current chunk
    chunks = []
    current_chunk = ""

    # Iterate through each sentence
    for sentence in sentences:
        # Check if adding this sentence would exceed the max chunk size
        if len(current_chunk) + len(sentence) > max_chunk_size:
            # If adding the sentence exceeds the max size, add the current chunk to the list
            chunks.append(current_chunk)
            # Start a new chunk with the current sentence
            current_chunk = sentence
        else:
            # If not, add the sentence to the current chunk
            if current_chunk:
                # Add a space before the sentence if the current chunk is not empty
                current_chunk += " " + sentence
            else:
                # If the current chunk is empty, start with the current sentence
                current_chunk = sentence
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

# Example usage
chunks = chunk_text(courseText)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=chunk
    )

    response.stream_to_file(f"speech{i+1}.mp3")