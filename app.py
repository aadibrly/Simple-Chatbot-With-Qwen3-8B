import os 
from dotenv import load_dotenv

load_dotenv()



os.environ['HF_TOKEN'] = os.getenv("HUGGINGFACE_API_KEY")

#langsmith tracking 
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANG_CHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["USER_AGENT"] = "Mozilla/5.0"


from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 
import streamlit as st



llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-8B",
    max_new_tokens=1024,
    temperature=0.7,
    
)

llm = ChatHuggingFace(llm=llm)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are Sunday an ai companion with same style as friday from ironman, greet the user or respond using 'Sir' , respond to the question asked"),
        ("user","Question:{question}")
    ]
)

parser = StrOutputParser()


#streamlit setup 





parser = StrOutputParser()



# Create chain
chain = prompt | llm | parser



# Streamlit Title
st.title("Say Hi to Sunday")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Message
if not st.session_state.messages:
    st.chat_message("assistant").write(
        "Hey! I'm Sunday. How can I help you today?"
    )

# Previoutmesage
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# user INput
question = st.chat_input("Ask Sunday something...")

# Run chain
if question:

    # Show user message
    with st.chat_message("user"):
        st.write(question)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Run existing LangChain chain
    response = chain.invoke({
        "question": question
    })

    # Show assistant response
    with st.chat_message("assistant"):
        st.write(response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })