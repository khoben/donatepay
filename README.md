# Donatepay WebSocket connector
## Setup (tested on python 3.9.5)

0. Get DonatePay token:

    Grab token from [widget link](https://donatepay.ru/donation/notifications/)
    ```sh
    https://widget.donatepay.ru/alert-box/widget/{YOUR-TOKEN-HERE}
    ```

1. Create .env file with token

    ```sh
    TOKEN={YOUR-TOKEN-HERE}
    ```

2. Create and activate the virtual environment (not necessary)

3. Install dependencies
    ```sh
    pip install -r requirements.txt
   ```
4. Run it
    ```sh
    python main.py
   ```
