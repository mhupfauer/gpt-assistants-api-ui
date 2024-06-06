from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

def search_web(query):
    print(f"Function called! With query: {query}")
    results = []
    for r in search(query, lang="en", num_results=10):
        results.append(r)

    urls = {*results}
    content = {}
    for k in results:
        try:
            # Send a GET request to the URL
            response = requests.get(k)
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract and return the plaintext
            text = soup.get_text(separator="\n")

            content[k] = re.sub(r"\n{2,}", "", text)
            content[k] = content[k] if len(content[k]) < 10000 else content[k][:10000]
    
        except requests.exceptions.RequestException as e:
            # Print any error that occurs
            print(f"Error fetching {k}: {e}")

    output =  "\n".join(content.values())
    return output if len(output) < 100000 else output[:100000]


TOOL_MAP = {"search_web": search_web}
