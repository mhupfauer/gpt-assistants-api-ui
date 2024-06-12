from openai import OpenAI
import nltk
from nltk.tokenize import sent_tokenize
from pydub import AudioSegment
import os
import pymupdf4llm

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
# chunks = chunk_text("SOME_TEXT")
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i+1}: {chunk}")
#     
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="alloy",
#         input=chunk
#     )
#     response.stream_to_file(f"speech{i+1}.mp3")


def merge_mp3_files(folder_path, output_filename):
    # Define a one second of silence audio segment
    one_second_silence = AudioSegment.silent(duration=1000)  # Duration is in milliseconds

    # Initialize an empty audio segment for merging
    combined = AudioSegment.empty()

    # List all mp3 files in the specified directory
    mp3_files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]
    mp3_files.sort()  # Sorting to maintain a consistent order

    # Loop over each file and concatenate them with one second of silence in between
    for file in mp3_files:
        current_track = AudioSegment.from_mp3(os.path.join(folder_path, file))
        combined += current_track + one_second_silence

    # Removing the extra second of silence at the end of the last track
    combined = combined[:-1000]

    # Export the combined audio to a new file
    combined.export(os.path.join(folder_path, output_filename), format="mp3")

# Usage
# folder_path = "../data/mp3"
# output_filename = "merged_output.mp3"
# merge_mp3_files(folder_path, output_filename)


def getPdfConts(path):
    return pymupdf4llm.to_markdown("input.pdf")

# Usage
# getPdfConts("./somefile.pdf")