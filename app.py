from flask import Flask, request, render_template,session, redirect, url_for
import PyPDF2
# from transformers import AutoTokenizer, AutoModelForQuestionAnswering
#enhance the quality of generated responses through retrieved documents.
from langchain.chains import ConversationalRetrievalChain
#Conversational memory is the mechanism that empowers a chatbot to respond 
#coherently to multiple queries, providing a chat-like experience. 
#It ensures continuity in the conversation, allowing the chatbot to consider 
#past interactions and provide contextually relevant responses.
from langchain.memory import ConversationBufferMemory
import logging
logger = logging.getLogger(__name__)
# All utility functions
import utils

from PIL import Image
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'ABCDEF'

# # Step 1: Choose a pre-trained model architecture
# model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"

def create_conversational_chain(llm, vector_store):
    """
    Creating conversational chain using Mistral 7B LLM instance and vector store instance

    Args:
    - llm: Instance of Mistral 7B GGUF
    - vector_store: Instance of FAISS Vector store having all the PDF document chunks 
    """

    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memory = ConversationBufferMemory(
                memory_key="chat_history",
                input_key="question",
            )
    
    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)
    return chain
def conversation_chat(user_input, conversation_chain):
    """
    Returns LLM response after invoking model through conversation_chain

    Args:
    - user_input(str): User input as a text
    - conversation_chain: Instance of ConversationalRetrievalChain 
    """
    # result = conversation_chain.invoke({"question": user_input, "chat_history": session['history']})
    # print(result)
    result={}
    result["answer"]="Yes"
    print(result)
    # session['past'].append(user_input)
    # session['generated'].append(result["answer"])
    return result["answer"]

# # Step 3: Load the pre-trained model
# try:
#     model = AutoModelForQuestionAnswering.from_pretrained(model_name)
# except OSError:
#     print(f"Model not found locally. Downloading {model_name}...")
#     model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# # Step 4: Define a tokenizer
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# Global variable to hold the conversation history
global_history = []
def clean_text(text):
    """
    Removes special characters from the given text
    """
    cleaned_text = ""
    for char in text:
        if char.isalnum() or char.isspace():
            cleaned_text += char
    return cleaned_text

@app.before_request
def setup_session():
    if 'past' not in session:
        session['past'] = []
        session['generated'] = []
        session['history'] = []
        session['file'] = None

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            # Store the extracted text in the session
            session['file_text'] = text
            # No need to store the file object in the session
            # session['file'] = file
            return redirect(url_for('chat'))
    return render_template("question.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    global global_history
    if request.method == "POST":
        question = request.form["question"]
        text = session.get('file_text', '') # Retrieve the stored text from the session
        if text:
            llm = utils.create_llm()
            vector_store = utils.create_vector_store(text)
            if vector_store:
                global_history.append(question)
                session['history']=global_history
                chain = create_conversational_chain(llm, vector_store)
                response = conversation_chat(question, chain)
                
                global_history.append(response)
                # # # Update the session with the new exchange
                # past.append(question)
                # generated.append(response)
                session['history']=global_history
                # session['past'] = past
                # session['generated'] = generated
                # Debugging: Print the number of past and generated messages
                print(f"Number of past messages: {len(session['history'])}")
                # print(f"Number of generated messages: {len(session['generated'])}")
                print(session)
                logger.info(f"Current session data: {session}")
                return render_template("result.html")
        else:
            # Handle case where no text is available in the session
            # ...
            return redirect(url_for('upload'))
    return render_template("result.html")

@app.route("/new_chat", methods=["GET"])
def new_chat():
    global global_history
    # Clear the global history
    global_history = []
    # Clear the session data and redirect to the upload page
    logger.info(f"Current session data: {session}")
    session.clear()
    return redirect(url_for('upload'))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
        

#     #Step 4: Create Vector Store and store uploaded Pdf file to in-mempry Vector Database FAISS
#     # and return instance of vector store
#         vector_store = utils.create_vector_store(text)
#         # cleaned_text = clean_text(text)

#         question = request.form["question"]
#         response = "Yes"
#         if vector_store:
#         #Step 5: If Vector Store created successful with chunks of PDF files
#         # then Create the chain object
#             chain = create_conversational_chain(llm, vector_store)
#             response=conversation_chat(question, chain)



# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         file = request.files["file"]
#         # print(file)
#         # Pass the path of the saved file to the create_vector_store function
#         if file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             text = ''
#             session['file'] = file
#             for page_num in range(len(pdf_reader.pages)):
#                 page = pdf_reader.pages[page_num]
#                 text += page.extract_text()
#             # return text
#         # vector_store = utils.create_vector_store(text)
#         # text = file.read().decode("utf-8")
#         llm = utils.create_llm()

#     #Step 4: Create Vector Store and store uploaded Pdf file to in-mempry Vector Database FAISS
#     # and return instance of vector store
#         vector_store = utils.create_vector_store(text)
#         # cleaned_text = clean_text(text)

#         question = request.form["question"]
#         response = "Yes"
#         if vector_store:
#         #Step 5: If Vector Store created successful with chunks of PDF files
#         # then Create the chain object
#             chain = create_conversational_chain(llm, vector_store)
#             response=conversation_chat(question, chain)

#         # outputs = model(**inputs)
#         # session['past'].append(question)
#         # session['generated'].append(response)

#         # print(response)
#         # return redirect(url_for('index'))
#         # return render_template("result.html", question=question, answer=response)
#         # return render_template("result.html")
#     # else:
#     #     return render_template("result.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)