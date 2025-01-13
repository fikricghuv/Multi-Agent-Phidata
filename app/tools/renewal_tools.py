from typing import Dict, Any, Optional
from phi.tools import Toolkit
from phi.utils.log import logger
import requests

class RenewalTools(Toolkit):
    def __init__(self, base_url: str):
        """
        Inisialisasi RenewalTools dengan base URL service FastAPI.
        :param base_url: Base URL dari service FastAPI.
        """
        super().__init__(name="renewal_tools")
        self.base_url = base_url
        self.register(self.send_renewal)

    def send_renewal(self, renewal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mengirimkan renewal ke server FastAPI.
        Args:
            renewal_data (Dict[str, Any]): Data klaim yang akan dikirimkan.
        Returns:
            Dict[str, Any]: Respons JSON dari server.
        """
        logger.info("Sending renewal to the server...")
        try:
            url = f"{self.base_url}/renewal"
            logger.debug(f"Sending POST request to {url} with data: {renewal_data}")
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=renewal_data, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info("Renewal sent successfully.")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending Renewal: {e}")
            return {"status": "error", "message": str(e)}
        