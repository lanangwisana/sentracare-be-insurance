from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from datetime import datetime
from database import Base
import enum

class ClaimStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"

    id = Column(Integer, primary_key=True, index=True)
    
    # Data Pasien (HL7 PID Segment Simulation)
    patient_name = Column(String(100), nullable=False)
    bpjs_number = Column(String(50), index=True, nullable=False)
    
    # Data Klinis (HL7 DG1 Segment Simulation)
    diagnosis_code = Column(String(20), nullable=False) # Contoh: A01.0 (Kode ICD-10)
    treatment_description = Column(Text, nullable=True)
    
    # Data Keuangan
    total_bill = Column(Float, nullable=False)
    
    status = Column(String(20), default=ClaimStatus.PENDING)
    response_message = Column(Text, nullable=True) # Balasan dari server asuransi
    
    created_at = Column(DateTime, default=datetime.utcnow)