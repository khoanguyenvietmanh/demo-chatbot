import openai
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

token_provider = get_bearer_token_provider(
 DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = "2024-02-01"
AZURE_ENDPOINT = "https://tvf-rd-openai-us.openai.azure.com/"
OPENAI_API_KEY = "708eab06a679406199f37dc1bfe4a9d4"
OPENAI_ENGINE = "gpt-4o-mini"
OPENAI_MODEL_NAME = "gpt-4o-mini"


AZURE_OPENAI_EMBEDDING_ENDPOINT = "https://tvf-rd-openai-jp.openai.azure.com/"
OPENAI_EMBEDDING_DEPLOYMENT = "text-embbeding-3-large"

llm_model = AzureOpenAI(
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    azure_ad_token_provider=token_provider,
    azure_deployment=OPENAI_ENGINE,
)


llm_embeddings = AzureOpenAIEmbeddings(
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_EMBEDDING_ENDPOINT,
    azure_deployment=OPENAI_EMBEDDING_DEPLOYMENT,
    azure_ad_token_provider=token_provider,
    chunk_size=256,
)

chat_model = AzureChatOpenAI(
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    azure_deployment=OPENAI_ENGINE,
    model=OPENAI_MODEL_NAME,
    azure_ad_token_provider=token_provider,
    streaming=True,
    temperature=0.0,
)