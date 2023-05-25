import os
import openai
import tiktoken
import json
import helpers as helpers

# Initializing API keys
KEY = ""
try:
    with open("../keys.json", 'r') as keys:
        json_data = json.load(keys)
        KEY = json_data['API_KEY']
    openai.api_key = KEY
except:
    raise Exception("Add a API key as described in the README.md")


MODEL = "gpt-3.5-turbo"
DOCUMENTS_DIRECTORY = "../test"
RESULTS_FILEPATH = "../results.json"


def limit_text(text:str,token_limit=2500):
    """
    params
        - text: the text to be shortened
    Returns a text that is at most 2000 tokens to be sent to chatGPT
    """
    print("Limiting text")
    final_text = ""
    current_length = 0
    tokenizer = tiktoken.get_encoding("cl100k_base")
    for word in text.split():
        length = len(tokenizer.encode(word)) 
        if current_length + length<token_limit:
            final_text+= " " + word
            current_length += length
    return final_text

def process_document(filepath: str, file_type:str):
    """
    params: 
        - text: The text of the document
        - file_type: pdf or txt, 
    Returns the output from OpenAI. 
    """
    pages = helpers.get_pages(filepath, 3,file_type=file_type)
    full_text = "".join(helpers.clean_document(pages))
    clean_text = limit_text(full_text)
    print(clean_text)

    prompt = "You are a helpful history science assistant. You can extract the relevant entities from historical law documents. Extract the number of the law, the date the law was published (day-month-year), the title of the law in the original language, the page number of the first page if it exists, and summarize what the law is about. The number of the law is a number only."
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": f"{clean_text}\n{prompt} "},
        ],
        temperature=0,
        model= MODEL,
    )
    #return based on current structure of API, may change later
    return response['choices'][0]['message']['content'].strip()

def batch_process():
    """
    Processes all the documents in the folder documents, and adds it to resuls.json if 
    the document was not already processed
    """

    results_file = open(RESULTS_FILEPATH,'r+')
    current_data = json.load(results_file)
    for filename in os.listdir(DOCUMENTS_DIRECTORY):
        extension = filename.split(".")[1]
        try: 
            test = current_data[filename]
            #if there is an error, the filename does not exist in the json
        except:
            f = os.path.join(DOCUMENTS_DIRECTORY, filename)
            text = process_document(f,extension)
            print("results", filename, text )
            current_data[filename] = text
    results_file.seek(0)
    results_file.truncate(0)
    results_file.write(json.dumps(current_data))
   
    results_file.close()
