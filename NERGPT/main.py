import helpers as helpers
import chat as chatHelp
import json
import os
TOKENIZERS_PARALLELISM=False

import openai

if __name__ == '__main__':
        """Testing for first page"""
        filename_test = "../documents/13-x-final.pdf"
        page_test = helpers.get_first_page(filename_test)
     
        test_Q = f"{page_test} \n\n---\n Create a Python list where the first index is the number of the document, the second the page number and the third the year it was published. REMEMBER that the page number comes before the number of the document"
        filepath = "../ddocuments/test.pdf"
        page = helpers.get_first_page(filepath)
        print(page)
        
        Q =  f"{page} \n\n---\n Create a Python list where the first index is the number of the document, the second the page number and the third the year it was published. REMEMBER that the page number comes before the number of the document"
        response = openai.ChatCompletion.create(
                messages =[
                {"role":"user", "content":f"{test_Q}"},
                {"role":"assistant", "content": "[22, 13, 1941]"},
                {"role":"user", "content":f"{Q}"},

                ],
                temperature=0,
                model="gpt-3.5-turbo",
        )
        print(response)


"""
Test: test.pdf 
Prompt:  Create a Python list where the first index is the number of the document, the second the page number and the third the year it was published.
 REMEMBER that the page number comes before the number of the document

Result : {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "[22, 14, 1941]",
        "role": "assistant"
      }
    }
  ],
  "created": 1684857035,
  "id": "chatcmpl-7JOZPSI9XRIlAJOGKRKlDMj8Wpa6y",
  "model": "gpt-3.5-turbo-0301",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 10,
    "prompt_tokens": 2108,
    "total_tokens": 2118
  }
} 

expected result = [22, 13, 1941]
"""


















#481-X

PROMPTS = {"Dates": "Geben Sie im Format {Datum: Erläuterung} die genauen Daten im Text im Format Jahr-Monat-Tag ein und geben Sie an, was an den einzelnen Tagen passiert ist. Geben Sie die Antwort in einem Python-Wörterbuch an",
           "Signatories": "Wer sind die Unterzeichner des Dokuments? Geben Sie Einzelheiten über sie an.",
           "Announcement number": "Wie lautet die Nummer der Bekanntmachung? Nur die Nummer angeben",
           "Institution":"Geben Sie mir einfach die Institution, die die Ankündigung durchsetzt",
           "Content":"Geben Sie mir eine Zusammenfassung des Kontextes auf Deutsch, die mindestens 100 Wörter lang ist",
           "Official action":"Was ist die im Kontext beschriebene Amtshandlung?"}
if __name__ == '__main__':

    # prompt = "Wie lautet die Nummer der Bekanntmachung? Nur die Nummer angeben"
    
    # "Q: Create a JSON file in English about the law announcement above that has the fields:\
    # {'Specific dates': {'date','explanation'},\
    # 'Signatory of the document':{'signatory', 'details'}, \
    # 'Number of announcement',\
    # 'Institution enforcing announcement',\
    # 'Content': Here, give a summary of the document in English,\
    # 'Official action'}"
    # directory = "../documents"
    # results_file = open("../results.json",'a')
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     dic = {"Document":filename, "Values":{}}
    #     text = helpers.processText(f)
    #     for id,question in PROMPTS.items():
    #         response = chatHelp.answer_question(text,question)
    #         dic["Values"][id] = response
    #     json_format = json.dumps(dic)
    #     results_file.write(json_format)
    # results_file.close()


    """Testing for paragraphs
    filename = "../documents/13-x-final.pdf"
    paragraphs = helpers.get_paragraphs(filename)
    print(paragraphs)"""

   




    # text = helpers.processText("../documents/481b.docx")
    # response = chatHelp.answer_question(text,prompt,debug=True)
    # print(response)
    

    # except Exception as e:
    #     print(e)
    #     return ""

    """Experimentation: Chunk length: 200, chatCompletion
            Dates: Nennen Sie mir die genauen Daten im Text im Format Jahr-Monat-Tag und geben Sie an, was an den einzelnen Tagen passiert ist.
                    Response: - 7. Juli 1942: Der Böhmisch-Mährische Verband für die Garten- 
                                    und Weinbauwirtschaft gibt eine Kundmachung bezüglich der 
                                    Erfassung und des Absatzes von Waldfrüchten und Pilzen heraus
                                    (Kundmachung Nr. 64), in der Pilzarten in Preisgruppen I-IV 
                                    eingeteilt werden. 
                             - 27. Juli 1942: Die Oberste Preisbehörde gibt einen Bescheid für 
                             Höchstpreise, Handelsspannen und Sätze im Handel mit getrockneten
                             Pilzen heraus. 
                            - 1. September 1942: Der Böhmisch-Mährische Verband für die Garten-
                            und Weinbauwirtschaft ergänzt die Kundmachung Nr. 64 
                            (Kundmachung Nr. 64a), die ebenfalls getrocknete Pilze betrifft. 
                            - 23. Juli 1942: Der Vorsitzende der Obersten Preisbehörde gibt 
                            eine Verordnung über die Preisbildung im Verkehr mit Frischwaren
                            und Trockenfrüchten heraus (Slg. Nr. 264). 
                            - 25. Juni 1943: Die Berghauptmannschaft in Brünn gibt eine
                            Verordnung im Kontext von Arbeiten zur Absperrung von Bränden heraus. 
                            - 7. Juli 1943: Die Oberste Preisbehörde gibt eine 
                            Kundmachung bezüglich der Preisbildung bei getrockneten
                            Pilzen heimischer Herkunft heraus (Kundmachung X), 
                            die mit ihrer Veröffentlichung im Amtsblatt in Kraft tritt.

            Signatories:Wer sind die Unterzeichner des Dokuments? Geben Sie Einzelheiten über sie an.
                        The orders are signed by the Chairman of the Board. No further details about the signatory are available in the text

            Announcement number: i - gave 481 for document 481b.docx, works
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
            Official action: Was ist die im Kontext beschriebene Amtshandlung?
                            Answer: Es gibt keine spezifische Amtshandlung im Kontext. Der Text beschäftigt sich mit verschiedenen Verordnungen, Regelungen und Kundmachungen zu Themen wie Preisbildung bei getrockneten Pilzen, dem Abdämmen von Grubenbränden und der Anleitung zur Durchführung von Arbeiten im Zusammenhang mit Absperrungen von Bränden und Brühungen.
            
                            
            Dates: Better: Geben Sie im Format {Datum: Erklärung} die genauen Daten im Text im Format Jahr-Monat-Tag an und geben Sie an, was an jedem Tag passiert ist.
            1943-07-07: Kundmachung X der Obersten Preisbehörde über die Preisbildung bei getrockneten Pilzen heimischer Herkunft wird veröffentlicht.
            1943-07-08: Die Kundmachung tritt mit dem Tag der Veröffentlichung im Amtsblatt in Kraft. Der Verordnung der Berghauptmannschaft in Brünn wird herausgegeben, die im Sinne des 64 der Verordnung vom 2. Mai 1932 die Anleitung zur Durchführung der mit der Absperrung von Brühungen und Bränden verbundenen Arbeiten regelt.
            1942-07-07: In der Beilage B und C der Kundmachung Nr. 64 des Böhmisch-Mährischen Verbandes für die Garten- und Weinbauwirtschaft betreffend die Regelung der Erfassung und des Absatzes von Waldfrüchten und Pilzen werden bestimmte getrocknete Pilzarten zu verstehen gegeben. 
            1942-07-23: Die Verordnung des Vorsitzenden der Obersten Preisbehörde über die Preisbildung im Verkehr mit Frischwaren und Trockenfrüchten wird herausgegeben.
            1942-07-27: Der Bescheid der OPB an den Böhmisch-Mährischen Verband für die Garten- und Weinbauwirtschaft, der die Höchstpreise, Handelsspannen und Sätze im Handel mit getrockneten Pilzen geregelt hat, wird herausgegeben.
            1942-09-01: Die Kundmachung Nr. 64a des Böhmisch-Mährischen Verbandes für die Garten- und Weinbauwirtschaft wird veröffentlicht.
            1943-06-25: Die Verordnung der Berghauptmannschaft in Brünn wird herausgegeben.
            Ich weiß es nicht, welche Tage wichtige Ereignisse im Zusammenhang mit dem Abdämmen von Grubenbränden auftraten.

            Dates: Best: Geben Sie im Format {Datum: Erläuterung} die genauen Daten im Text im Format Jahr-Monat-Tag ein und geben Sie an, was an den einzelnen Tagen passiert ist. Geben Sie die Antwort in einem Python-Wörterbuch an

            
    """