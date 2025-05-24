from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

class TravelResponse(BaseModel):
    destination: str
    activities: list[str]
    days: int 
    budget: int

llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14")
parser = PydanticOutputParser(pydantic_object=TravelResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a travel agent. 
            Your task is to suggest a travel itinerary based on the user's preferences.
            Suggest the activities, ideal number of days, and budget (in Rs.) for the given destination.
            You are only allowed to talk about the travel itinerary.
            Do not include any other information.
            If asked about anything else, say "I am a travel agent. I can only help you with travel itineraries."
            Wrap the output in this format and provide no other text\n{format_instructions}
            """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent(
    llm=llm,
    tools=[],
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=False,
    tools=[]
)

app = Flask(__name__)
CORS(app)

@app.route("/api/itinerary", methods=["POST"])
def get_itinerary():
    data = request.get_json()
    city = data.get("city")

    try:
        raw_response = agent_executor.invoke({"query": city})
        structured_response = parser.parse(raw_response.get("output"))

        return jsonify({
            "destination": structured_response.destination,
            "activities": structured_response.activities,
            "days": structured_response.days,
            "budget": structured_response.budget
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)




# # !-- TO JUST PRINT THE RESPONSE --! 

# city = input("Enter the city you want to visit: ")

# raw_response = agent_executor.invoke({"query": city})

# # print(raw_response)

# try:
#     structured_response = parser.parse(raw_response.get("output"))
#     print("City: ", structured_response.destination)
#     print("Activities: ", *structured_response.activities, sep=', ')
#     print("Ideal Days: ", structured_response.days)
#     print("Budget: ", structured_response.budget)
# except Exception as e:
#     print("Error parsing response:", e)
#     # print("Raw response:", raw_response)