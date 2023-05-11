import helpers as helpers
import chat as chatHelp

import os
TOKENIZERS_PARALLELISM=False


if __name__ == '__main__':
    prompt = "Was ist die im Kontext beschriebene Amtshandlung?"
    
    # "Q: Create a JSON file in English about the law announcement above that has the fields:\
    # {'Specific dates': {'date','explanation'},\
    # 'Signatory of the document':{'signatory', 'details'}, \
    # 'Number of announcement',\
    # 'Institution enforcing announcement',\
    # 'Content': Here, give a summary of the document in English,\
    # 'Official action'}"

    # tokenizer = tiktoken.get_encoding("cl100k_base")


    # # Get the number of tokens for each sentence
    # n_tokens = len(tokenizer.encode(prompt)) #76
    # print("Length of prompt", n_tokens)

    text = helpers.processText("../documents/481b.docx")
    response = chatHelp.answer_question(text,prompt,debug=True)
    print(response)
    

    # except Exception as e:
    #     print(e)
    #     return ""

    """Experimentation: Chunk length: 200, chatCompletion
            Signatories:Wer sind die Unterzeichner des Dokuments? Geben Sie Einzelheiten über sie an.
                        The orders are signed by the Chairman of the Board. No further details about the signatory are available in the text

            Announcement number: Geben Sie mir nur die Nummer der Ankündigung - gave 481 for document 481b.docx, works
            Institution: Die Oberste Preisbehörde. -- document 481b, works 
            Summary: Geben Sie mir eine Zusammenfassung des Kontextes auf Deutsch, die mindestens 100 Wörter lang ist
                    Result: Der vorliegende Kontext beinhaltet mehrere Kundmachungen und Verordnungen, 
                        die im Jahr 1943 in Brünn veröffentlicht wurden. Die ersten beiden Abschnitte 
                        beschäftigen sich mit der Preisbildung von getrockneten Pilzen heimischer
                        Herkunft und informieren über die verschiedenen Pilzarten, die in diese Kategorie fallen. 
                        Es werden auch Richtlinien für die Durchführung von Arbeiten bezüglich der Absperrung von 
                        Bränden und Brühungen gegeben. Der dritte Abschnitt behandelt das Verhalten bei einem 
                        Grubenbrand und informiert darüber, dass Schlagwetterexplosionen berücksichtigt werden 
                        müssen. Die letzte Passage legt fest, wie die Preise für getrocknete Pilze berechnet 
                        werden und verweist auf andere Verordnungen zur Preisbildung im Verkehr mit Frischwaren 
                        und Trockenfrüchten. Insgesamt handelt es sich um eine Zusammenstellung von gesetzlichen 
                        Vorgaben und Anweisungen, die sich mit verschiedenen Aspekten des Handels und der Sicherheit
                        befassen. --Good
            Official action: Es gibt keine spezifische Amtshandlung im Kontext. Der Text beschäftigt sich mit verschiedenen Verordnungen, Regelungen und Kundmachungen zu Themen wie Preisbildung bei getrockneten Pilzen, dem Abdämmen von Grubenbränden und der Anleitung zur Durchführung von Arbeiten im Zusammenhang mit Absperrungen von Bränden und Brühungen.
            
            
    """