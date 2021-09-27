import asyncio
import json
import re

import requests

from centrifuge import Client, Credentials
from settings import SOCKET_CONNECT_URL, SOCKET_LINK, TOKEN, WIDGET_LINK


class DonatePaySocketConnector(object):

    def __init__(self, recover_messages=True):
        self.__client = self.__create_client(recover_messages=recover_messages)

    async def subscribe(self):
        await self.__client.connect()
        await self.__client.subscribe(
            channel="notifications#{}".format(self.__client.credentials.user),
            on_message=self.__message_handler,
            on_join=self.__join_handler,
            on_leave=self.__leave_handler
        )

    async def __message_handler(self, **kwargs):
        print("Event:", kwargs['data']['notification']['vars'])

    async def __join_handler(self, **kwargs):
        print("Join:", kwargs)

    async def __leave_handler(self, **kwargs):
        print("Leave:", kwargs)

    def __create_client(self, recover_messages):
        userId, auth = self.__prepare_auth_data()
        credentials = Credentials(userId, auth['time'], "", auth["token"])
        client = Client(SOCKET_CONNECT_URL, credentials,
                        recover_messages=recover_messages)

        return client

    def __prepare_auth_data(self):
        session = requests.session()
        r = session.get(WIDGET_LINK.format(TOKEN), verify=False)
        userId = re.search(
            r"function\sgetUserId\(\)\s{\s*return\sparseInt\('([\w\d]+)'\);", r.text).group(1)
        csrf = re.search(
            r"function\scsrf\(\)\s{\s*return\s'([\w\d]+)';", r.text).group(1)
        r_socket = session.post(
            SOCKET_LINK, data={'token': TOKEN, '_token': csrf})
        socket_auth_data = json.loads(r_socket.text)

        return userId, socket_auth_data


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    socket = DonatePaySocketConnector(recover_messages=False)
    asyncio.ensure_future(socket.subscribe())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Interrupted from keyboard")
    finally:
        loop.close()
