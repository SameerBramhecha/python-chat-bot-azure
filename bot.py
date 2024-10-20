import os
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential

class FaqBot(ActivityHandler):
    def __init__(self):
        self.client = ConversationAnalysisClient(
            endpoint=os.getenv("CLU_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("CLU_API_KEY"))
        )

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()
        response = self.client.analyze_conversations(
            documents=[text],
            project_name=os.getenv("CLU_PROJECT_NAME"),
            deployment_name=os.getenv("CLU_DEPLOYMENT_NAME")
        )

        # Get the top intent
        top_intent = response.documents[0].intent
        if top_intent == "FAQ":
            await turn_context.send_activity("Sure, here is the answer to your FAQ.")
        else:
            await turn_context.send_activity("I'm sorry, I don't understand.")
