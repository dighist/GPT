from transformers import AutoTokenizer, AutoModelForSequenceClassification

import torch
from PyPDF2 import PdfReader, PdfFileWriter
import re

TOKENIZERS_PARALLELISM = False


tokenizer = AutoTokenizer.from_pretrained(
    "ivanlau/language-detection-fine-tuned-on-xlm-roberta-base")

model = AutoModelForSequenceClassification.from_pretrained(
    "ivanlau/language-detection-fine-tuned-on-xlm-roberta-base")


def remove_special_characters(text: str):
    text = text.replace('\t', " ")
    # text = text.replace('/', "")
    # text = text.replace('\n', '')
    text = text.replace("§", " ")
    return text


def get_pages(filepath: str, num_pages: int, file_type="pdf") -> list[str]:
    """
    params
        - filepath: The path of the document
        - pages: the number of pages of document desired
        - file_type: pdf or txt, 
    returns:
        - a list of strings, each string representing the raw output from each page. The list has length pages-1
        Returns the whole document if it's of type txt
    """
    strings: list[str] = []
    if file_type == "pdf":
        reader = PdfReader(filepath)
        pages = reader.pages
        for i in range(num_pages):
            page = pages[i]
            strings.append(page.extract_text())
    elif file_type == "txt":
        with open(filepath) as file:
            text = "\n".join(file.readlines())
            strings.append(text)
    return strings


def clean_document(document: list[str], single_language=False):
    """
    params:
        - document: A list, every string representing the pages of the document
        - single_language: a boolean indicating if we are trying to get only one language of the document
    Returns a list of cleaned strings representing the document
    """
    clean = []
    for string in document:
        if single_language:
            clean.append(get_single_language(
                remove_special_characters(string)))
        else:
            clean.append(remove_special_characters(string))
    return clean


def get_single_language(text: str, language: str = "Czech"):
    """
    Cleans up a text possibly in two languages, and returns the part of the text only in the desired language
    """
    clean = ""
    # Check language for every 4 words
    words = text.split()
    i = 0
    while i < len(words):
        seq = " ".join(words[i:i+4])
        match = re.search(r'[1-9]+', seq)
        if not match:
            # Now chech the language
            inputs = tokenizer(seq, return_tensors="pt")
            with torch.no_grad():
                logits = model(**inputs).logits
                predicted_class_id = logits.argmax().item()
                logits = torch.softmax(logits, dim=1)
                predicted_class_value = logits[0][predicted_class_id].item()
                label = model.config.id2label[predicted_class_id]
            if label == language and predicted_class_value >= 0.95:
                clean += " " + seq
        else:
            clean += " " + seq
        i += 4

    return clean
