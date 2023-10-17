import openai
import pandas as pd
import re
import spacy

nlp = spacy.load('en_core_web_sm')

# Set up your OpenAI API key
openai.api_key = 'enter_your_key'

# Define A dictionary for storing information 
information={"name":"","email":"","phone":""}

# Define your chat agents and their roles
agents = {
    "agent1": "Convince to give details",
    "agent2": "Extract and Verify user information",
    "agent3": "Format the extracted information"
}

# Define regular expressions for extracting  Email, and Phone number

email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
phone_pattern = re.compile(r'\b[6-9]\d{9}\b')

def extract_information(response_text):
    # Extract Name, Email, and Phone Number from the response text
  
    email_match = email_pattern.search(response_text)
    phone_match = phone_pattern.search(response_text)


    phone_match = re.findall(phone_pattern, response_text)
    email_match=re.findall(email_pattern,response_text)
    doc = nlp(response_text)

    names = [entity for entity in doc.ents if entity.label_ == 'PERSON']    
    name=None
    phone =None
    email=None
    
    if(len(phone_match)!=0):
        phone=phone_match[0]
    
    if(len(email_match)!=0):
        email=email_match[0]

    if(len(names)!=0):
        name=names[0]

    # Returning the relevant info
    return name, email, phone

def send_message(message):
    conversation_history.append({"role": "system", "content": "You are a chatbot.",})
    conversation_history.append({"role": "user", "content": message,})

def get_openai_response(messages):
    response = openai.Completion.create(
        model="text-davinci-003",  # Wechoose a different model
        prompt=messages,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Initialize conversation history
conversation_history = []
send_message("Hi How are you?. You are a chatbot. Your job is to majorly extract 3 things from the user. 1)His/Her name 2)His/her mobile Number 3) His/her email id. If he/she isnt ready to give it readily, ask the user manipulative questions in such a way that he/she gives you the required details. Start the chat by asking their name. Do not directly say that you want to extract it. Do it in a diplomatic way. But for sure ask these 3 pieces of information from the user")
print("Agent: Hi human! How may I help you ?")
print("Prompt 'stop' to terminate this conversation")
prompt = input("User: ")



while prompt.lower() != "stop":

    # Update conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Construct the conversation string
    conversation = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history])

    # Get response from GPT-3
    response_text = get_openai_response(conversation)

    # Print and update conversation history with the agent's response
    print(f"Agent: {response_text}")
    conversation_history.append({"role": "agent", "content": response_text})
    prompt = input("User: ")
    
    # Extract information from the response

    name, email, phone = extract_information(prompt)

    if(name!=None):
        information["name"]=name
    if(phone!=None):
        information["phone"]=phone
    if(email!=None):
        information["email"]=email

    
df = pd.DataFrame(list(information.items()), columns=['Key', 'Value'])

# Display the DataFrame
df.to_csv("output.csv",index=False)

print(information)