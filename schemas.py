from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Input Schema
class ClaimSubmission(BaseModel):
    patient_name: str
    bpjs_number: str
    diagnosis_code: str
    treatment_description: str
    total_bill: float

# Output Schema (YANG INI TADI KURANG LENGKAP)
class ClaimResponse(BaseModel):
    id: int
    patient_name: str       # <-- Ditambahkan
    bpjs_number: str
    diagnosis_code: str     # <-- Ditambahkan
    total_bill: float       # <-- Ditambahkan (Penyebab Error Utama)
    status: str
    response_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True