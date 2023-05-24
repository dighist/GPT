import os
import openai
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
import requests
import tiktoken
from helpers import get_german_sentences
from helpers import readDocument
import json

#Initializing API keys
KEY = ""
with open("../keys.json", 'r') as keys:
    json_data = json.load(keys)
    KEY = json_data['API_KEY']
openai.api_key = KEY
TOKENIZERS_PARALLELISM = False

# Helper functions, not used for now


# Function to split the text into chunks of a maximum number of tokens
def split_into_many(text, max_tokens=200):
    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence))
                for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    # Add the last chunk to the list of chunks
    if chunk:
        chunks.append(". ".join(chunk) + ".")

    return chunks


def createEmbedding(text):
    embedding = openai.Embedding().create(
        input=text, engine='text-embedding-ada-002')['data'][0]['embedding']
    return embedding


def create_context(
    question, text, max_len=1800, size="ada"
):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Create chunks for which creating embedding would be easier
    chunks = split_into_many(text)

    # Creating holder for chunks and embeddings
    dic = {}
    i = 0
    for chunk in chunks:
        dic[i] = {}
        dic[i]['text'] = chunk
        i += 1

    # Get the embeddings for the question
    q_embeddings = createEmbedding(question)
    distances = {}
    for index, holder in dic.items():
        chunk_text = holder['text']
        embedding = createEmbedding(chunk_text)
        holder['embedding'] = embedding
        distances[index] = distances_from_embeddings(
            q_embeddings, [embedding], distance_metric='cosine')[0]

    # Get the distances from the embeddings
    returns = []
    cur_len = 0
    distances = dict(sorted(distances.items(), key=lambda x: x[1]))
    # print("DISTANCES SORTED", distances)
    # Sort by distance and add the text to the context until the context is too long
    for i, distance in distances.items():

        # Add the length of the text to the current length
        tokenizer = tiktoken.get_encoding("cl100k_base")
        # Get the number of tokens for each sentence
        n_tokens = len(tokenizer.encode(dic[i]['text']))

        cur_len += n_tokens + 4

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(dic[i]['text'])
    # print("CONTEXT LENGTH", cur_len)
    # Return the context
    return "\n\n###\n\n".join(returns)


def answer_question(
    text,
    question,
    model="text-davinci-003",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        text,
        max_len=max_len,
        size=size,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the questin and context
        # response = openai.Completion.create(
        #     prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
        #     temperature=0.5,
        #     # top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        #     stop=stop_sequence,
        #     model=model,
        # )
        # return response["choices"][0]["text"].strip()

        # English question: Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:
        response = openai.ChatCompletion.create(
            messages=[
                {"role": "user", "content": f"Beantworten Sie die Frage anhand des nachstehenden Kontextes, und wenn die Frage anhand des Kontextes nicht beantwortet werden kann, sagen Sie \"Ich weiß es nicht\"\n\nKontext: {context}\n\n---\n\nFrage: {question}\nAntwort:"}
            ],
            # prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            # temperature=0,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            # stop=stop_sequence,
            model="gpt-3.5-turbo",
        )
        print(response)
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(e)
        return ""
