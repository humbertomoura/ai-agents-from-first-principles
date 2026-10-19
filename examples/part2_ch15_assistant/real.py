import json
import os
from openai import OpenAI
from tools import TOOLS

client = OpenAI()  # uses the key in OPENAI_API_KEY
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-astra")

INSTRUCTIONS = (
    "You are the order assistant at Rosa's Bakery. "
    "Check the calendar and prices before answering.")


def tool(name, description, field):
    return {"type": "function", "name": name,
            "description": description, "strict": True,
            "parameters": {
                "type": "object",
                "properties": {field: {"type": "string"}},
                "required": [field],
                "additionalProperties": False}}


TOOL_SPECS = [
    tool("check_calendar",
         "Says how many openings there are on a given day.",
         "day"),
    tool("check_price",
         "Says the price of a bakery product.",
         "product"),
]

question = "Do you have carrot cake for Saturday? How much is it?"
history = [{"role": "user", "content": question}]

for rnd in range(5):
    response = client.responses.create(
        model=MODEL, instructions=INSTRUCTIONS,
        input=history, tools=TOOL_SPECS)
    history.extend(response.output)  # keep everything
    calls = [item for item in response.output
             if item.type == "function_call"]
    if not calls:                   # the model is done
        text = response.output_text
        if response.status != "completed" or not text:
            text = f"No usable answer ({response.status})."
        print(text)
        break
    for call in calls:
        try:
            args = json.loads(call.arguments)
            result = TOOLS[call.name](**args)
        except Exception as err:    # error becomes a notice
            result = {"error": str(err)}
        history.append({
            "type": "function_call_output",
            "call_id": call.call_id,
            "output": json.dumps(result)})
else:
    print("Round limit reached without a final answer.")
