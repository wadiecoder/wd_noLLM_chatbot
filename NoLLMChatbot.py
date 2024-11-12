import customtkinter as ctk
from difflib import SequenceMatcher
import re
import json
from PIL import Image

''' WD: This function loads the predefined question-answer pairs from a JSON file.
    It opens the 'data.json' file and reads its contents into the qa_pairs list. 
    Each item in this list contains a question and its corresponding answer. '''
with open('data.json', encoding='utf-8') as f:
    qa_pairs = json.load(f)

''' WD: This function is used to clean and preprocess the user input by removing 
    all non-alphanumeric characters and converting the text to lowercase.
    This makes text comparison more accurate by ensuring consistency. '''
def clean_text(text):
    return re.sub(r'[^\w\s]', '', text).lower()

''' This function computes a similarity score between two strings (s1 and s2) 
    using the SequenceMatcher from difflib. It returns a value between 0 and 1, 
    where 1 indicates identical strings and lower values indicate less similarity. '''
def similarity_score(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

''' This function takes user input, cleans it, and then compares it to all the predefined questions in the qa_pairs list.
    It calculates a similarity score for each question and returns the answer to the most similar question.
    If no match is found with a high enough score, a default response is returned. '''
def chatbot_response(user_input):
    user_input_clean = clean_text(user_input)
    best_match = None
    highest_score = 0.0
    ''' For each question-answer pair in the qa_pairs list, we clean the question 
        and calculate the similarity score between the cleaned question and the user input. '''
    for qa in qa_pairs:
        question_clean = clean_text(qa['question'])
        score = similarity_score(user_input_clean, question_clean)

        if score > highest_score:
            highest_score = score
            best_match = qa
    ''' If the highest similarity score is greater than 0.6, we return the answer associated with the best match.
        Otherwise, we return a default message indicating the chatbot doesn't have a response. '''
    if highest_score > 0.6:
        return best_match['answer']
    else:
        return "Je suis désolé, je n'ai pas de réponse à cette question. Essayez de poser des questions sur le génie électrique ou mécanique."

''' This function is triggered when the user presses the "Demander" button.
    It retrieves the user's input from the text entry field, passes it to the chatbot_response function, 
    and then updates the response label with the chatbot's answer. '''
def on_ask():
    user_question = question_entry.get()
    response = chatbot_response(user_question)
    response_text.set(f"Chatbot: {response}")
    question_entry.delete(0, 'end')

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("WD NoLLM Chatbot - Made by Wadie Coder")
window.geometry("600x450")
window.resizable(False, False)

window.configure(bg="#1a1a1a")

image = Image.open("./assets/logo.png")
logo = ctk.CTkImage(dark_image=image, size=(100, 100))
logo_label = ctk.CTkLabel(window, image=logo, text="")
logo_label.pack(pady=(10, 20))

welcome_label = ctk.CTkLabel(window, text="Bienvenue dans le chatbot WD NoLLM",
                             fg_color="#007ACC", text_color="white", 
                             font=("Helvetica", 18, "bold"), corner_radius=8)
welcome_label.pack(pady=(20, 10), padx=20, fill="x")

question_frame = ctk.CTkFrame(window, fg_color="#333333", corner_radius=8)
question_frame.pack(pady=10, padx=20, fill="x")

question_label = ctk.CTkLabel(question_frame, text="Posez votre question :", 
                              font=("Arial", 12), text_color="#D1D1D1")
question_label.pack(pady=(10, 5))

question_entry = ctk.CTkEntry(question_frame, width=500, font=("Arial", 12), 
                              placeholder_text="Entrez votre question ici...")
question_entry.pack(pady=5, padx=20, fill="x")

# Ask button
ask_button = ctk.CTkButton(window, text="Demander", command=on_ask, 
                           fg_color="#007ACC", text_color="white", 
                           font=("Arial", 13, "bold"), corner_radius=8)
ask_button.pack(pady=10)

response_frame = ctk.CTkFrame(window, fg_color="#333333", corner_radius=8)
response_frame.pack(pady=10, padx=20, fill="both", expand=True)

response_text = ctk.StringVar()
response_label = ctk.CTkLabel(response_frame, textvariable=response_text, 
                              wraplength=500, justify="left", 
                              font=("Arial", 12), text_color="white")
response_label.pack(pady=20, padx=20)

window.mainloop()
