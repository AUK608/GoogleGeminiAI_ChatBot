import gradio as gr   ###for UI
import google.generativeai as genai   ###for genai bot api
from dotenv import load_dotenv, find_dotenv   ###to get key, value pair of environment
import os

###to find each env key,value pair
load_dotenv(find_dotenv())

###configure the keys
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

###create the genai-pro model
genaimodel = genai.GenerativeModel()

###function for getting user msg
def get_user_input(inmsg, chatbotlist):
    print(inmsg, chatbotlist)
    chatbotlist += [[inmsg, None]]

    return '', chatbotlist

###function to store the chat history b/w user and geminiai
def generate_chatbot_history(chatbot: list[list[str, str]]) -> list[list[str, str]]:
    chatbot_history = []
    
    if len(chatbot) == 0:
        return chatbot_history

    ###loop through chats of user and gemini ai
    for cb in chatbot:
        chatbot_history.append(
            {
                "role" : "user",
                "parts" : [cb[0]]
            }
        )
        chatbot_history.append(
            {
                "role" : "model",
                "parts" : [cb[1]]
            }
        )

    return chatbot_history

###function for getting reply from chatbot
def get_geminiai_response(chatbot):
    ###reply from gemini ai and chat history to be stored and sent to UI
    #chatbot[-1][1] = "Reply from the Bot..."
    genai_msg = chatbot[-1][0]
    chatbot_history = generate_chatbot_history(chatbot[:-1])
    chat_hist = genaimodel.start_chat(history=chatbot_history)
    genai_response = chat_hist.send_message(genai_msg)
    chatbot[-1][1] = genai_response.text

    return chatbot

###gradio app different blocks
with gr.Blocks() as GeminiAPI_ChatBot:
    ###chats display area
    chatbot = gr.Chatbot(
        label = "Chat with GEMINI AI",
        bubble_full_width = False,
    )

    ###user textbox to enter msg
    msg = gr.Textbox()

    ###clear button
    clear = gr.ClearButton([msg, chatbot])

    ###hitting enter submits the user inputs
    msg.submit(
        get_user_input, [msg, chatbot], [msg, chatbot]
        ).then(
            get_geminiai_response,
            [chatbot],
            [chatbot]
        )

if __name__ == "__main__":
    GeminiAPI_ChatBot.queue()   ###queue all the requests
    GeminiAPI_ChatBot.launch()   ###launch the gradio app
