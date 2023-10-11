# ChatBot Derived from PDF Knowledge using LLM (Language Model)

## About the Project
The project is designed to establish a chatbot that leverages the content of PDF documents as its knowledge base. Users can pose questions, and the chatbot will respond based on the context of the uploaded PDFs. The foundational model backing this system is the [gpt-3.5-turbo model](https://platform.openai.com/). By integrating LangChain and Vector database (Deeplake), the model is fine-tuned to provide contextual knowledge from the uploaded PDFs. 

The frontend interface is constructed with simplicity in mind, built on HTML and styled with CSS, while the backend functionality is powered by Python.

## User Flow
1. The user uploads a zip file containing multiple PDF documents and initiates the upload.
2. As files upload, embeddings are constructed via the Ada model, and subsequently stored in the Deeplake vector database.
3. Upon successful upload, a chat interface activates, allowing users to converse with the bot. Responses are sourced directly from the PDF content.

## Prerequisites
1. An [OpenAI account](https://platform.openai.com/account/api-keys) to access the API key.
2. An account with [Activeloop](https://www.activeloop.ai/) to secure the `ORG_ID` and `API_Token`.

## Setup and Execution
1. Clone or download the project repository.
2. Populate `config.ini` with the necessary `key`, `org_id`, and `API-token`.
3. Install the required Python libraries.
4. Open your command terminal.
5. Navigate to the project directory.
6. Execute the command `set FLASK_APP=app.py`.
7. Run the application with `flask run`.

###  Libraries and Dependencies
Flask: For web application backend.
langchain: For document loading, embeddings, chat models, etc.
werkzeug: For secure file operations.
zipfile: For working with zip files.
shutil: For high-level file operations.
logging: For application logging.
configparser: For parsing configuration files.

For a full list of dependencies and their versions, see requirements.txt.

## Contributions
Feel free to raise issues or provide pull requests!

## License
NA

## Acknowledgements
Thank you to OpenAI and Activeloop for their platforms and APIs.
