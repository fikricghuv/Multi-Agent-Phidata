from fastapi import APIRouter, HTTPException
from app.controller.agent_controller import executive_director_agent, escalation_agent
from rich.pretty import pprint
import psycopg2
from psycopg2.extras import RealDictCursor
import re
from app.model.models import ClaimRequest, RenewalRequest, QuestionRequest, CoveringRequest, MessageTelegeamRequest

router = APIRouter()

# Koneksi ke PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="ai_agent_db",
        user="postgres",
        password="AgenticAI",
        cursor_factory=RealDictCursor
    )

@router.post("/claim")
def hit_service_claim(claim: ClaimRequest):
    """
    Endpoint untuk melakukan klaim.
    Args:
        claim (ClaimData): Data klaim yang dikirimkan oleh client.
    Returns:
        dict: Respons konfirmasi klaim.
    """
    try:
        processed_claim = f"Data pengajuan klaim dengan nomor polis {claim.policy_id} berhasil dilakukan, mohon ditunggu untuk prosesnya."
        return processed_claim
    except Exception as e:
        print_error = f"Terjadi kesalahan: {e}"
        return print_error
        # raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {e}")

@router.post("/covering")
def hit_service_covering(covering: CoveringRequest):
    """
    Endpoint untuk melakukan covering policy.
    Args:
        covering (CoveringData): Data covering yang dikirimkan oleh client.
    Returns:
        str: Respons konfirmasi Covering.
    """
    try:
        processed_covering = f"Data pengajuan covering atas nama {covering.name} berhasil dilakukan, mohon ditunggu untuk prosesnya."
        return processed_covering
    except Exception as e:
        print_error = f"Terjadi kesalahan: {e}"
        return print_error

@router.post("/renewal")
def hit_service_renewal(renewal: RenewalRequest):
    """
    Endpoint untuk melakukan renewal policy.
    Args:
        renewal (RenewalData): Data renewal yang dikirimkan oleh client.
    Returns:
        str: Respons konfirmasi renewal.
    """
    try:
        processed_renewal = f"Data pengajuan renewal dengan nomor polis {renewal.policy_id} berhasil dilakukan."
        return processed_renewal
    except Exception as e:
        print_error = f"Terjadi kesalahan: {e}"
        return print_error
    
@router.post("/send-message")
def send_message_to_user(request: MessageTelegeamRequest):
    """
    Endpoint untuk mengirimkan pesan ke pengguna Telegram.
    Args:
        request (MessageRequest): Data permintaan pengiriman pesan.
    Returns:
        dict: Respons dari Telegram API.
    """
    try:
        response = escalation_agent.run(request.chat_id, request.message)
        if response["status"] == "success":
            return {"status": "success", "data": response["data"]}
        else:
            raise HTTPException(status_code=400, detail=response["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

@router.post("/ask-agent-brins")
def ask_question(request: QuestionRequest):
    """
    Endpoint untuk mengajukan pertanyaan ke multi_ai_agent.
    """

    # Logging pertanyaan yang diterima
    print(f"User Question: {request.question}")

    # Jalankan pertanyaan pada Executive Director Agent
    try:
        response = executive_director_agent.run(request.question, stream=False)

        # Logging memory dan summary (jika diperlukan)
        # pprint(executive_director_agent.memory.memories)
        # pprint(executive_director_agent.memory.summary)

        # Membersihkan respons dari metadata tool calls
        cleaned_response = re.sub(
            r"\nRunning:\n - .*?\(.*?\)\n\n", 
            "", 
            response.content
        )
        print(f"Response : {cleaned_response}")
        # Simpan percakapan ke database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ai.chat_history (user_input, bot_response) VALUES (%s, %s)",
                (request.question, cleaned_response)
            )
            conn.commit()

            cursor.close()
            conn.close()
        except Exception as e:
            print("Error saving to database:", e)

        return {"response": cleaned_response}
    
    except Exception as e:
        print("Error in agent execution:", e)
        return {"error": "Terjadi kesalahan saat memproses permintaan."}
