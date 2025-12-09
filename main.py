from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import random

from database import Base, engine, SessionLocal
from models import InsuranceClaim, ClaimStatus
from schemas import ClaimSubmission, ClaimResponse

app = FastAPI(title="Sentracare Insurance Bridge Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/insurance/claims", response_model=ClaimResponse, tags=["claims"])
def submit_claim(data: ClaimSubmission, db: Session = Depends(get_db)):
    
    # --- LOGIC SIMULASI BPJS/ASURANSI ---
    # Di dunia nyata, ini akan connect ke server BPJS V-Claim
    
    status = ClaimStatus.APPROVED
    msg = "Klaim berhasil disetujui otomatis."

    # Simulasi Logic:
    if data.total_bill > 5000000:
        status = ClaimStatus.PENDING
        msg = "Nominal besar, menunggu verifikasi manual."
    elif "Z99" in data.diagnosis_code: # Contoh kode diagnosa ditolak
        status = ClaimStatus.REJECTED
        msg = "Kode diagnosa tidak ditanggung asuransi ini."
    
    new_claim = InsuranceClaim(
        patient_name=data.patient_name,
        bpjs_number=data.bpjs_number,
        diagnosis_code=data.diagnosis_code,
        treatment_description=data.treatment_description,
        total_bill=data.total_bill,
        status=status,
        response_message=msg
    )
    
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim

@app.get("/insurance/claims", response_model=List[ClaimResponse], tags=["claims"])
def get_all_claims(db: Session = Depends(get_db)):
    return db.query(InsuranceClaim).order_by(InsuranceClaim.created_at.desc()).all()