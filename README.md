# RAG System

## **Installing Dependencies**

The modules are added in requirements.txt. To install run,

	pip install -r requirements.txt

## **API Keys**

The following API keys are required:

- Google Gemini API Key (https://makersuite.google.com/app/apikey)
- Sarvam API Key (https://dashboard.sarvam.ai/)

Add these keys in the .env file located in project folder.

	GOOGLE_API_KEY = ADD YOUR GOOGLE GEMINI API KEY  
	SARVAM_API_KEY = ADD YOUR SARVAM API KEY

## **Tools & Technologies**

- Python
- Langchain

## **Models**

- Text Embedding (text-embedding-004) [https://ai.google.dev/gemini-api/docs/models/gemini#text-embedding]

- LLM (gemini-1.5-pro) [https://deepmind.google/technologies/gemini/pro/]

- Text Translation (mayura:v1) [https://docs.sarvam.ai/api-reference-docs/endpoints/translate-text]

- Text to Speech (bulbul:v1) [https://docs.sarvam.ai/api-reference-docs/endpoints/text-to-speech]

## **Checklist**

| Part No.| Descripton                           | Status     |
| --------| -------------------------------------| ---------- |
| Part 1  | Building a RAG system                | Completed  |
| Part 2  | Building Agent with multiple Tools   | Completed  |
| Part 3  | Adding Voice to Agent                | Completed  |


## Running CodeBase and Web App

To start a server run,
	
`python server.py`

Streamlit is used to create UI,  app.py file can be run as:  

   `streamlit run app.py`
   
## **Functionality & Description**

### Part 1 (Building a RAG system )

- Retrieval-Augmented Generation (RAG) system is built using an external data source (pdf file). The pdf document is loaded and split into chunks, then embeddings are generated and stored in a FAISS (Facebook AI Similarity Search) vector store. Chaining is ued which combines the vectors from vector store and LLM is added. It is served using FastAPI `/part1` endpoint.

  - When app.py is run, below show interface will be presented
  <kbd>![](/README_images/PART0.png)</kbd>

  - To run query for this end point, go to Part 1 tab and enter the query, press the enter button, the response to the query will be displayed.

  - Few examples are shown below:
  <kbd>![](/README_images/PART1_1.png)</kbd>
  <kbd>![](/README_images/PART1_2.png)</kbd>
  
 ### Part 2 (Building Agent with multiple Tools)

- An Agent is used to perform multiple actions based on user's query. Agent uses a language model to choose sequence of actions based on user's query. Additionally, along with pdf tool, a calculator tool is added. 

  When the user's query is hello or how are you, The agent will not use vector database (pdf tool) or calculator tool. It will respond using LLM. 
  
  <kbd>![](/README_images/PART2_1.png)</kbd>
  
  When the user's query is based on calculations, the agent will use calculator tool to generate response.
  
  <kbd>![](/README_images/PART2_2.png)</kbd>
  
  When the user's query is based on pdf like "When Heinrich Rudolph Hertz born?", the agent will use pdf tool to generate response.
  
  <kbd>![](/README_images/PART2_3.png)</kbd>
  
  When the user's query involves both tools i.e. pdf and calculator, "When Heinrich Rudolph Hertz born and What would be the year when he is 12 years old?", the agent will use both the tools to generate response.
  
  <kbd>![](/README_images/PART2_4.png)</kbd>

### Part 3 (Adding Voice to Agent)

- Sarvam API is used to first Transalte the output from English to Hindi language, then Text to speech is used to create a .wav file and use it as audio.

  - User's query and agent response is shown below:
  
  <kbd>![](/README_images/PART3.png)</kbd>


## **Demonstration Video**

The video demonstrates user's query and generated reponses.


<video src="https://github.com/user-attachments/assets/aac51fc5-16a6-4784-9e4a-6d8a06224d3c">
</video>


## **References**

1. <https://docs.sarvam.ai/api-reference-docs/introduction/>
2. <https://docs.streamlit.io/>
3. <https://js.langchain.com/docs/introduction/>
4. <https://ai.google.dev/gemini-api/docs/>
