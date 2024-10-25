import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from operator import itemgetter
from langchain_core.messages import ToolMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from llm_init import chat_model

def InteractWithCSV(input_text):
    df = pd.read_csv("Superstore.csv",encoding='windows-1254')
    tool = PythonAstREPLTool(locals={"df": df})
    llm_with_tools = chat_model.bind_tools([tool], tool_choice=tool.name)
    parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)

    system = f"""You have access to a pandas dataframe `df`. \
    Here is the output of `df.head().to_markdown()`:

    \`\`\`
    {df.head().to_markdown()}
    \`\`\`

    Given a user question, write the Python code to answer it. \
    Don't assume you have access to any libraries other than built-in Python ones and pandas.
    Respond directly to the question once you have enough information to answer it."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system,
            ),
            ("human", "{question}"),
            # This MessagesPlaceholder allows us to optionally append an arbitrary number of messages
            # at the end of the prompt using the 'chat_history' arg.
            MessagesPlaceholder("chat_history", optional=True),
        ]
    )


    def _get_chat_history(x: dict) -> list:
        """Parse the chain output up to this point into a list of chat history messages to insert in the prompt."""
        ai_msg = x["ai_msg"]
        tool_call_id = x["ai_msg"].additional_kwargs["tool_calls"][0]["id"]
        tool_msg = ToolMessage(tool_call_id=tool_call_id, content=str(x["tool_output"]))
        return [ai_msg, tool_msg]


    chain = (
        RunnablePassthrough.assign(ai_msg=prompt | llm_with_tools)
        .assign(tool_output=itemgetter("ai_msg") | parser | tool)
        .assign(chat_history=_get_chat_history)
        .assign(response=prompt | chat_model | StrOutputParser())
        .pick(["tool_output", "response"])
    )

    results = chain.invoke({"question": f"{input_text}"})

    return results['response']