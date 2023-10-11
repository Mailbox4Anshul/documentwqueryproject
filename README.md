# ChatBot Derived from PDF Knowledge using LLM (Language Model)

**About the project -** 
  
The project aims to create a chatbot that uses PDF documents as a knowledge base and a user can chat based on the information inside the PDF documents.
The foundational model used is the gpt-3.5-turbo model
Therefore, using the LangChain and Vector database (Deeplake), the model is further finetuned for the contextual knowledge from the uploaded PDFs.

Frontend is kept simple and built using HTML, styling is done using CSS. 
The backend is based on Python. 

**User flow -**

The user uploads a zip file that contains multiple PDF files and clicks on the upload button -> As the files are getting uploaded, embeddings are created through the Ada model and then stored in the deeplake vector database. -> After files are uploaded successfully, the chat interface is enabled and the user is able to chat the answers given are from the information within the PDF documents uploaded.

**Prerequisites** 
1. You will require an account on OpenAI and should have API key to use the models. https://platform.openai.com/account/api-keys
2. You should have an account in activeloop https://www.activeloop.ai/ and should have a ORD_ID and API_Token

**How to execute the project**
1. Download the project
2. Add the key, org_id, and API-token in the config.ini
3. Install the required Python libraries in cmd
4. Open command prompt on your laptop
5. Navigate to the project path
6. run set FLASK_APP=app.py
7. flask run
  
