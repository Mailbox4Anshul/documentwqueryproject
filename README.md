# documentwqueryproject
Project for ChatBot from multiple PDFs using LLM

**About the project -** 
  The project aims to create a chatbot that uses PDF documents as a knowledge base and a user can chat based on the information inside the pdf documents.
  The foundational model used is the gpt-3.5-turbo model
  Therefore, using the LangChain and Vector database (Deeplake), the model is further finetuned for the contextual knowledge from the uploaded PDFs.

Frontend is kept simple and built using HTML, styling is done using CSS. 
The backend is based on Python. 

**User flow -**

The user uploads multiple PDF files in a zip folder and clicks on the upload button -> As the files are getting uploaded, embeddings are created through the Ada model and then stored in deeplake vector database. -> After files are uploaded successfully, then 
