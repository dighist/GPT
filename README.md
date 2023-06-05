# Using GPT for digital History

The goal of this repository is to support the digital history project aiming at digitalizing some documents from the Kladno archive in the Czech Republic. The repository contains code that allows historical documents to be analyzed using OpenAI gpt-3.5-turbo model. The code works as follows.

1. helpers.py contains different functions aimed at extracting text from documents (either in txt or pdf format)
2. chat.py allows to make the API request to the OpenAI API. 
3. main.py contains glue code, that can be run to analyze all the **documents** folder. 
4. The results of all analysis will be saved in the **results.json** file. If a file has already been analyzed and has info in the json, running main.py will not analyze it

# Requirements

You will need to create a top-level file called **keys.json**. In this file, create an JSON file containing your OpenAI api key as follows:

<pre><code>
{
    "API_KEY": "dummyAPIKey"
}
</code></pre>

