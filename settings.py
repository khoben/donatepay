from dotenv import load_dotenv
import os

load_dotenv()

WIDGET_LINK = 'http://widget.donatepay.ru/alert-box/widget/{}'
SOCKET_LINK = 'http://widget.donatepay.ru/socket/token'
SOCKET_CONNECT_URL = 'ws://136.243.1.101:3002/connection/websocket'
TOKEN = os.getenv('TOKEN')
