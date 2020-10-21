import aiohttp_jinja2
from aiohttp import web

from models.message import Message


class MessageView(web.View):

    @aiohttp_jinja2.template('messages.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        if self.match_info['type'] == 'inbox':
            messages = await Message.get_inbox_messages_by_user(db=self.app['db'], user_id=self.session['user']['_id'])
        elif self.match_info['type'] == 'outbox':
            messages = await Message.get_send_messages_by_user(db=self.app['db'], user_id=self.session['user']['_id'])
        else:
            messages = []
        return dict(messages=messages)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        await Message.create_message(db=self.app['db'], from_user=self.session['user']['_id'],
                                     to_user=data['to_user'], message=data['message_text'])

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)
