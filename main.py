import asyncio
import json
import re

import requests

from centrifuge import Client, Credentials
from settings import SOCKET_CONNECT_URL, SOCKET_LINK, TOKEN, WIDGET_LINK


@asyncio.coroutine
def message_handler(**kwargs):
    print("Message:", kwargs['data']['notification']['vars'])


@asyncio.coroutine
def join_handler(**kwargs):
    print("Join:", kwargs)


@asyncio.coroutine
def leave_handler(**kwargs):
    print("Leave:", kwargs)


def run(client):

    yield from client.connect()

    yield from client.subscribe(
        channel="notifications#{}".format(client.credentials.user),
        on_message=message_handler,
        on_join=join_handler,
        on_leave=leave_handler
    )


def create_client(recover_messages=True):
    userId, auth = prepare_auth_data()
    credentials = Credentials(userId, auth['time'], "", auth["token"])
    client = Client(SOCKET_CONNECT_URL, credentials,
                    recover_messages=recover_messages)

    return client


def prepare_auth_data():

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

    client = create_client(recover_messages=False)

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run(client=client))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Interrupted from keyboard")
    finally:
        loop.close()
