import os
import openai
import gradio as gr
from pymongo import MongoClient

# Set up OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up MongoDB connection
atlas_mongo_url = os.getenv('ATLAS_MONGODB_URL')
client = MongoClient(atlas_mongo_url)
db = client["chatbot"]
collection = db["conversations"]

# Define the chatbot function
def chatbot(input_text):
    conversation.append(input_text)  # Add user input to conversation history
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt='\n'.join(conversation),
        max_tokens=100,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    conversation.append(answer)  # Add chatbot's answer to conversation history
    # Save question and answer to MongoDB
    conversation_dict = {"question": input_text, "answer": answer}
    collection.insert_one(conversation_dict)
    return answer

# Initialize conversation history
conversation = []

# Create the Gradio interface
input_text = gr.inputs.Textbox(lines=7, label="Input")
output_text = gr.outputs.Textbox(label="Output")

interface = gr.Interface(
    fn=chatbot,
    inputs=input_text,
    outputs=output_text,
    title="Chatbot",
    description="Type your question or statement.",
    examples=[
        ["What is the weather today?"],
        ["Tell me a joke."],
        ["Who won the World Cup in 2018?"],
    ],
)

# Launch the Gradio interface
interface.launch(server_port=7860)