from llm_init import chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
prompt = ChatPromptTemplate.from_template("""
You are an intelligent assistant tasked with classifying user input into one of three categories:
1. Normal interaction: This occurs when the user is not asking for CSV interaction and is not discussing meeting creation.
2. CSV Interaction: This occurs when the user is asking questions or suggesstion questions related or interacting with a CSV file.
3. Meeting Creation: This occurs when the user is discussing or attempting to create a meeting.

Based on the user's input, return a response indicating which category the interaction belongs to, looking at the csv file first and remember all its information:
- If the input is general or specifically about CSV file information, mark it as csv_information.
- If the input is a normal conversation (neither CSV interaction nor meeting creation), mark it as normal.
- If the input is related to creating or managing a meeting, mark it as ms_create.

Your task is to classify the following input:

{topic}

Return your classification as a dictionary with keys 'normal', 'csv_information', and 'ms_create' where one of the values is True and the other two are False.
""")

class Pointing(BaseModel):
    normal: bool = Field(
        description="Indicates whether the interaction is a general or normal conversation that does not involve CSV file interaction or meeting creation."
    )
    csv_information: bool = Field(
        description="True if the interaction generally or specifically involves questions or actions or suggesstion questions related to a CSV file, otherwise False."
    )
    ms_create: bool = Field(
        description="True if the interaction involves creating, managing, or discussing a meeting, otherwise False."
    )

router = prompt | chat_model.with_structured_output(Pointing)