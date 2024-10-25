import streamlit as st
from llm_init import chat_model
from router import router
from ms_creator import meeting_creator
from csv_interactor import InteractWithCSV

#user_input = "Make a meeting Checking service with hiro.nguyen@techvify.com.vn from 12:00 to 15:00 on October 27th 2024"

def InteractiveChat(user_input):
    
    Pointer = router.invoke(user_input)

    if Pointer.normal:
        print("Normal Chat")
        reply = chat_model.invoke(user_input)
        #print(reply.content)
        return reply.content
    elif Pointer.csv_information:
        print("Infomation from CSV")
        reply = InteractWithCSV(user_input)
        #print(reply)
        return reply
    elif Pointer.ms_create:
        
        response = meeting_creator(user_input)
        
        if response.status_code == 201:
            meeting_data = response.json()
            meeting_id = meeting_data["id"]
            #print("Meeting created successfully please check your mail and calendar. Meeting ID:", meeting_id)
            return f"Meeting created successfully please check your mail and calendar.\n Meeting ID: {meeting_id}"
        else:
            #print("Failed to create meeting. Status code:", response.status_code)
            return f"Failed to create meeting.\n Status code: {response.status_code}"

#InteractiveChat(user_input)