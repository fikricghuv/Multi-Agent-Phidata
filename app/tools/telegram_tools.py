from typing import Dict, Any
from phi.tools import Toolkit
from phi.utils.log import logger
import requests

TELEGRAM_BOT_TOKEN = "8004259969:AAEQ6FojZGFNPkP-aq9xuN8ca1ADLtDUUfc"
TELEGRAM_CHAT_ID = "975270162"

class TelegramTools(Toolkit):
    def __init__(self):
        """
        Inisialisasi TelegramTools dengan token bot Telegram.
        :param bot_token: Token bot Telegram.
        """
        super().__init__(name="telegram_tools")
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

        # Mendaftarkan fungsi send_message ke dalam tools
        self.register(self.send_message)

    def send_message(self, chat_id: str, message: str) -> Dict[str, Any]:
        """
        Mengirimkan pesan ke pengguna melalui bot Telegram.
        :param chat_id: ID chat Telegram penerima.
        :param message: Pesan yang akan dikirimkan.
        :return: Respons dari API Telegram dalam bentuk dictionary.
        """
        logger.info(f"Sending message to chat_id {chat_id}...")
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            logger.debug(f"Payload: {payload}")
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            # Parsing respons API
            result = response.json()
            if response.status_code == 200:
                logger.info(f"Message sent successfully to chat_id {chat_id} with the message: {message}")
                return (f"Message sent successfully to chat_id {chat_id} with the message: {message}")
                # return {"status": "success", "data": result.get("result", {})}
            else:
                logger.warning(f"Failed to send message: {result.get('description', 'Unknown error')}")
                return (f"Failed to send message: {result.get('description', 'Unknown error')}")
                # return {"status": "error", "message": result.get("description", "Unknown error")}
        except requests.RequestException as e:
            logger.error(f"Error sending message to chat_id {chat_id}: {e}")
            return (f"Error sending message to chat_id {chat_id}: {e}")
            # return {"status": "error", "message": str(e)}
