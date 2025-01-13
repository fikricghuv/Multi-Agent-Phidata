from typing import Dict, Any, Optional
from phi.tools import Toolkit
from phi.utils.log import logger
import requests


class ClaimTools(Toolkit):
    def __init__(self, base_url: str):
        """
        Inisialisasi ClaimTools dengan base URL service FastAPI.
        :param base_url: Base URL dari service FastAPI.
        """
        super().__init__(name="claim_tools")
        self.base_url = base_url
        self.register(self.send_claim)

    def send_claim(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mengirimkan klaim ke server FastAPI.
        Args:
            claim_data (Dict[str, Any]): Data klaim yang akan dikirimkan.
        Returns:
            Dict[str, Any]: Respons JSON dari server.
        """
        logger.info("Sending claim to the server...")
        try:
            url = f"{self.base_url}/claim"
            logger.debug(f"Sending POST request to {url} with data: {claim_data}")
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=claim_data, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info("Claim sent successfully.")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending claim: {e}")
            return {"status": "error", "message": str(e)}
