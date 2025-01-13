from typing import Dict, Any, Optional
from phi.tools import Toolkit
from phi.utils.log import logger
import requests


class CoveringTools(Toolkit):
    def __init__(self, base_url: str):
        """
        Inisialisasi CoveringTools dengan base URL service FastAPI.
        :param base_url: Base URL dari service FastAPI.
        """
        super().__init__(name="covering_tools")
        self.base_url = base_url
        self.register(self.send_covering)

    def send_covering(self, covering_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mengirimkan covering ke server FastAPI.
        Args:
            covering_data (Dict[str, Any]): Data covering yang akan dikirimkan.
        Returns:
            Dict[str, Any]: Respons JSON dari server.
        """
        logger.info("Sending covering to the server...")
        print("Sending Covering...")
        try:
            url = f"{self.base_url}/covering"
            logger.debug(f"Sending POST request to {url} with data: {covering_data}")
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=covering_data, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info("Covering sent successfully.")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending covering: {e}")
            return {"status": "error", "message": str(e)}
