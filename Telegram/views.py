import asyncio
import json
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views import View
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, Update

from Utils.language_utils import LanguageUtils

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_POST, name='dispatch')
class TelegramBotView(View):
    def __init__(self):
        super().__init__()
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.menus = {
            'en-us': ['/start', '/help', '/test1', '/test2'],
            'zh-cn': ['/開始', '/幫助', '/測試1', '/測試2'],
            'zh-hans': ['/开始', '/帮助', '/测试1', '/测试2']
        }
        self.lang_utils = LanguageUtils()

    async def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        language_code = data['message']['from']['language_code']
        print(language_code)
        update = Update.de_json(data, self.bot)

        if update.message:
            print('test1')
            user_message = update.message.text

            response_message = await self.process_message(user_message, language_code)

            await update.message.reply_text(response_message)

        return JsonResponse({'status': 'ok'})

    async def run_listener_in_background(self, listener_func):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, listener_func)

    async def process_message(self, user_message, language_code):
        first_space_index = user_message.find(' ')

        if first_space_index != -1:
            command = user_message[:first_space_index].strip()
            message = user_message[first_space_index + 1:].strip()
        else:
            command = user_message
            message = ""

        menu = self.menus.get(language_code, [])

        if command == '/start':
            if message == 'start':
                print('test2')
                print('test3')
            if message == 'stop':
                print('test4')
                print('test5')
        elif command == '/help':
            response_message = self.lang_utils.translate(language_code, 'help')
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton(item) for item in menu]], one_time_keyboard=True)
            return response_message.encode('utf-8').decode('unicode-escape'), reply_markup
        else:
            response_message = self.lang_utils.translate(language_code, 'help')
            return response_message.encode('utf-8').decode('unicode-escape'), None