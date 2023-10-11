from flask import Flask, request, jsonify, render_template
import os
from langchain.document_loaders import PyPDFLoader
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from zipfile import ZipFile
import shutil
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
logging.basicConfig(level=logging.DEBUG)
import configparser

# Initialize config parser
config = configparser.ConfigParser()
#config.read('./config/config.ini')  # Relative path to the config file

if os.path.exists('./config/config.ini'):
    config.read('./config/config.ini')
else:
    raise FileNotFoundError("Configuration file 'config.ini' not found")

# Read values
openai_api_key = config['OpenAI']['API_KEY']
my_activeloop_org_id = config['ActiveLoop']['ORG_ID']
active_loop_api_token = config['ActiveLoop']['api_token']

# Explicitly set the OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["ACTIVELOOP_TOKEN"] = active_loop_api_token

# initialize embeddings model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# create Deep Lake dataset
#my_activeloop_org_id = my_activeloop_org_id
my_activeloop_dataset_name = "langchain_pdf_qa3"

dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"
db = DeepLake(dataset_path=dataset_path, embedding=embeddings)

# Initialize the chat model
model = ChatOpenAI(model='gpt-3.5-turbo')

# Initialize the question-answering chain
retriever = db.as_retriever()
qa_chain = RetrievalQA.from_llm(model, retriever=retriever)

# Initialize Flask app and configure upload folder
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize user_sessions dictionary to manage user session state
user_sessions = {}

# function to load pdf files, split files in pages, use splitter to create chunks and embeddings. 
# store embeddings in vectordb
def load_and_add_to_deep_lake(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=10,
        length_function=len,
    )

    docs = text_splitter.split_documents(pages)
    
    logging.info(f'Starting to add documents to Deep Lake dataset. Number of documents: {len(docs)}')
    result = db.add_documents(docs)
    logging.info(f'Successfully added documents to Deep Lake dataset. Result: {result}')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Check if uploaded file is a ZIP file
            if filename.endswith('.zip'):
                print("Before zip file upload")
                # Create a temporary folder to extract the ZIP contents
                temp_folder = os.path.join(app.config['UPLOAD_FOLDER'], "temp_folder")
                if os.path.exists(temp_folder):
                    print("Inside temp folder condition")
                    shutil.rmtree(temp_folder)
                os.makedirs(temp_folder)

                with ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_folder)

                # Dynamically discover the nested folder name
                nested_folder = next(os.walk(temp_folder))[1][0]  # This will get the first folder
                pdf_folder = os.path.join(temp_folder, nested_folder)
                pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
                print(pdf_files)
                
                for pdf_file in pdf_files:
                    print("Before adding file to folder")
                    pdf_path = os.path.join(temp_folder, nested_folder, pdf_file)
                    print(pdf_path)
                    print("After adding file to folder and before vectordb")
                    load_and_add_to_deep_lake(pdf_path)
                    print("After calling function to vectordb")

                # Remove temporary folder
                #shutil.rmtree(temp_folder)
            else:
                load_and_add_to_deep_lake(file_path)
            
            # Optionally remove the temporary file
            #os.remove(file_path)
            print(file_path)
            print(temp_folder)
            print(nested_folder)
            return jsonify({"message": "File(s) successfully processed"}), 200
        else:
            return jsonify({"message": "No file selected"}), 400
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return jsonify({"message": "An error occurred"}), 500

@app.route('/query', methods=['POST'])
def query_text():
    try:
        session_id = request.json.get('session_id', 'default_session')
        query = request.json['query']

        # Retrieve old context if available
        old_context = user_sessions.get(session_id, '')
        
        print("Before qa_chain.run")
        answer = qa_chain.run(query)
        print("After qa_chain.run")

        #Perform the question-answering task
        #answer, new_context = qa_chain.run(query, context=old_context)

        #Store the new context
        #user_sessions[session_id] = new_context

        return jsonify({"response": answer}), 200
    except Exception as e:
        print(f"Error while processing the query: {e}")
        return jsonify({"response": "An error occurred while processing your query."}), 500

if __name__ == '__main__':
    app.run(debug=True)
