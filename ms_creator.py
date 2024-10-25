import requests
import json
from llm_init import chat_model
from pydantic import BaseModel, Field

# Credentials
Client_id = '26d2776f-70d1-4f7b-9ceb-73c29869c146'
Client_secret = 'lI28Q~VteYX4hlrYoS68HVN8iXzzuakYXwKxfb.E'
Tenant_id = '4233b65f-404d-4edc-ba46-0265b65ee5d9'

def get_access_token():
    url = f'https://login.microsoftonline.com/{Tenant_id}/oauth2/v2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': Client_id,
        'client_secret': Client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, data=data)
    response_data = response.json()
    access_token = response_data['access_token']
    return access_token

class meeting_info(BaseModel):
    title: str = Field(description="Meeting title")
    start_time: str = Field(description="Meeting start time")
    end_time: str = Field(description="Meeting end time")
    participants: list = Field(description="List of participants")
    location: str = Field(description="Meeting location")

def process_meeting_input(input_text):
    get_info = chat_model.with_structured_output(meeting_info)
    results = get_info.invoke(input_text)
    return results

def create_invite(title, start_time, end_time, participants, location):
    create_meeting_url = f"https://graph.microsoft.com/v1.0/users/kane.nguyen@techvify.com.vn/events"
    access_token = get_access_token()

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    meeting_payload = {
    "subject": title,
    "body": {
        "contentType": "HTML",
        "content": "Meeting with ".join(participants)
    },
    "start": {
        "dateTime": start_time,
        "timeZone": "SE Asia Standard Time"
    },
    "end": {
        "dateTime": end_time,
        "timeZone": "SE Asia Standard Time"
    },
    "location": {
        "displayName": location
    },
    "attendees": [
            {"emailAddress": {"address": participant, "name": participant}, "type": "required"}
            for participant in participants
        ],
    "isOnlineMeeting": True,
    "onlineMeetingProvider": "teamsForBusiness"
}

    response = requests.post(
        create_meeting_url, headers=headers, data=json.dumps(meeting_payload))

    return response
    # if response.status_code == 201:
    #     meeting_data = response.json()
    #     meeting_id = meeting_data["id"]
    #     print("Meeting created successfully please check your mail and calendar. Meeting ID:", meeting_id)
    
    # else:
    #     print("Failed to create meeting. Status code:", response.status_code)

def meeting_creator(input_text):
    # Step 1: Process the meeting input using LLM
    meeting_details = process_meeting_input(input_text)
    #print(f"Processed Meeting Details: {meeting_details}")

    title = meeting_details.title
    start_time = meeting_details.start_time
    end_time = meeting_details.end_time
    participants = meeting_details.participants
    location = meeting_details.location
    #print(title, start_time, end_time, participants, location)
    
    # Step 2: Create the meeting using MS Graph API
    response = create_invite(title, start_time, end_time, participants, location)
    return response