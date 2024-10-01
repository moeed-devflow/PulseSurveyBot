from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
import json

from PulseSurveyBot import PulseSurveyBot
import os

app_id = os.getenv("MICROSOFT_APP_ID")
app_password = os.getenv("MICROSOFT_APP_PASSWORD")

bot_settings = BotFrameworkAdapterSettings(app_id, app_password)

adapter = BotFrameworkAdapter(bot_settings)
bot = PulseSurveyBot()

async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    if response:
        return web.Response(text=json.dumps(response))
    return web.Response()

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3978)
