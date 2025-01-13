from typing import Dict, Any
from phi.tools import Toolkit
from phi.utils.log import logger

class FeedbackHandlerTools(Toolkit):
    def __init__(self):
        """
        Agent untuk mengelola dan menganalisis feedback dari customer.
        """
        super().__init__(name="feedback_handler_tools")
        self.feedback_storage = []  # Tempat penyimpanan feedback sementara
        self.register(self.collect_feedback)
        self.register(self.analyze_feedback)

    def collect_feedback(self, feedback_data: dict) -> str:
        """
        Mengumpulkan feedback dari pengguna.

        Args:
            feedback_data (dict): Data feedback yang diberikan oleh user, harus memiliki key 'user_feedback'.

        Returns:
            str: Konfirmasi bahwa feedback telah diterima.
        """
        if not isinstance(feedback_data, dict) or "user_feedback" not in feedback_data:
            raise ValueError("Data feedback harus dalam format {'user_feedback': 'feedback_text'}")

        try:
            logger.info("Menerima feedback dari user...")

            # Validasi input apakah memiliki key 'user_feedback'
            if not isinstance(feedback_data, dict) or "user_feedback" not in feedback_data:
                raise ValueError("Data feedback harus dalam format {'user_feedback': 'feedback_text'}")

            # Ambil nilai feedback
            user_feedback = feedback_data["user_feedback"]

            # Inisialisasi storage jika belum ada
            if not hasattr(self, 'feedback_storage'):
                self.feedback_storage = []

            # Simpan feedback ke storage
            self.feedback_storage.append(user_feedback)
            logger.debug(f"Feedback diterima: {user_feedback}")

            return "Terima kasih atas feedback Anda! Kami akan memperbaiki layanan kami berdasarkan masukan Anda."
        except Exception as e:
            logger.error(f"Terjadi kesalahan saat mengumpulkan feedback: {e}")
            return "Maaf, terjadi kesalahan saat memproses feedback Anda."


    def analyze_feedback(self) -> Dict[str, Any]:
        """
        Menganalisis feedback yang telah dikumpulkan.
        Returns:
            Dict[str, Any]: Statistik analisis feedback.
        """
        if not self.feedback_storage:
            return {"status": "error", "message": "Tidak ada feedback untuk dianalisis."}

        # Contoh analisis sederhana: hitung kategori feedback
        positive = [fb for fb in self.feedback_storage if "baik" in fb.lower()]
        negative = [fb for fb in self.feedback_storage if "buruk" in fb.lower()]
        neutral = [fb for fb in self.feedback_storage if fb not in positive and fb not in negative]

        logger.info("Analisis feedback selesai.")
        return {
            "total_feedback": len(self.feedback_storage),
            "positive": len(positive),
            "negative": len(negative),
            "neutral": len(neutral),
        }
