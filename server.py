import os
from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from bot import FaqBot  # Your FaqBot class defined earlier
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Bot Adapter Settings
bot_settings = BotFrameworkAdapterSettings(
    app_id=os.getenv("MICROSOFT_APP_ID"),
    app_password=os.getenv("MICROSOFT_APP_PASSWORD")
)

# Bot Adapter
adapter = BotFrameworkAdapter(bot_settings)

# FaqBot instance
faq_bot = FaqBot()

# Error handler
async def on_error(context: TurnContext, error: Exception):
    print(f"An error occurred: {error}")
    await context.send_activity("Sorry, it looks like something went wrong.")

adapter.on_turn_error = on_error

# Flask route to handle messages
@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        json_message = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(json_message)

    async def aux_func(turn_context):
        await faq_bot.on_turn(turn_context)

    # Process the activity through Bot Framework Adapter
    task = adapter.process_activity(activity, "", aux_func)
    return Response(status=201)

# Run the Flask server
if __name__ == "__main__":
    app.run(port=3978)
