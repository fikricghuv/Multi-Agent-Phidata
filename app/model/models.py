from typing import Union
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str
    user_id: str
    session_id: str
    # run_id: str
    channel: str

class ClaimRequest(BaseModel):
    policy_id: str
    claim_reason: str
    claim_amount: float

class CoveringRequest(BaseModel):
    name: str
    product: str

class RenewalRequest(BaseModel):
    policy_id: str
    nik_number: str

# Model data untuk permintaan pengiriman pesan
class MessageTelegeamRequest(BaseModel):
    chat_id: int
    message: str
