"""
SovereignGuard AI - Enterprise REST API Gateway
Autor: Talia González López (Applied AI Architect)
Propiedad Intelectual Soberana - Desacoplamiento de Servicios
"""

import time
import hashlib
from datetime import datetime
from typing import Optional, Literal, Dict, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Importamos nuestro arsenal desacoplado
from router import HybridSLMRouter
from shield import SovereignResilienceShield

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="🛡️ SovereignGuard AI Core API",
    version="2.0.0",
    description="Microservicio REST determinista y desacoplado para auditoría, enrutamiento SLM y sanitización agéntica."
)

# CORS Middleware para permitir conexiones desde cualquier frontend (Streamlit, React, apps bancarias)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. ESQUEMAS DE DATOS (Pydantic Models)
# ==========================================

class IntentQueryRequest(BaseModel):
    query: str = Field(..., example="¡Ayuda! Veo un cargo no reconocido en mi tarjeta de la app.")

class SanitizeRequest(BaseModel):
    raw_llm_output: str = Field(
        ..., 
        example="Tras analizar el log bancario ISO 8583, mi DECISIÓN: BLOQUEO por sospecha de phishing."
    )

class TransactionEvaluationRequest(BaseModel):
    transaction_id: str = Field(..., example="TXN-99482-MX")
    amount: float = Field(..., gt=0, example=35200.50)
    intent_description: str = Field(..., example="Cargo en línea no reconocido en comercio internacional.")
    pos_entry_mode: Optional[str] = Field(default="01", example="05")
    auditor_credential: Optional[str] = Field(default="Cédula A - CNSF", example="Cédula A - CNSF")

class EvaluationResponse(BaseModel):
    transaction_id: str
    router_agent: str
    atomic_verdict: Literal["PROCEDENTE", "IMPROCEDENTE", "BLOQUEO", "ERROR_DE_FORMATO", "RESCATE_MANUAL_REQUERIDO"]
    deterministic_guarantee: bool
    latency_ms: float
    audit_hash_sha256: str
    timestamp_utc: str

# ==========================================
# 2. ENDPOINTS DE INFRAESTRUCTURA Y SALUD
# ==========================================

@app.get("/health", tags=["Infraestructura"])
def health_check() -> Dict[str, Any]:
    """
    Liveness and Readiness probe para balanceadores de carga y orquestadores (Kubernetes/AWS).
    """
    return {
        "status": "OPERATIONAL",
        "shield_engine": "ACTIVE",
        "router_engine": "ACTIVE",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# ==========================================
# 3. ENDPOINTS TRANSACCIONALES INDEPENDIENTES
# ==========================================

@app.post("/v1/router/classify", tags=["SLM Router (<1.5s)"])
def classify_intent(request: IntentQueryRequest) -> Dict[str, Any]:
    """
    Enrutador SLM de ultra-baja latencia para triage financiero y control de Token Economy.
    """
    start_time = time.perf_counter()
    decision = HybridSLMRouter.classify_intent(request.query)
    latency = (time.perf_counter() - start_time) * 1000
    
    decision["latency_ms"] = round(latency, 2)
    return decision


@app.post("/v1/shield/sanitize", tags=["Cincel Regex Determinista"])
def sanitize_ai_output(request: SanitizeRequest) -> Dict[str, Any]:
    """
    Capa de saneamiento determinista. Intercepta alucinaciones y fuerza estados atómicos.
    """
    verdict = SovereignResilienceShield.sanitize_output(request.raw_llm_output)
    return {
        "raw_input": request.raw_llm_output,
        "atomic_verdict": verdict,
        "deterministic": True
    }


@app.post("/v1/guard/evaluate", response_model=EvaluationResponse, tags=["Core Pipeline Completo"])
def evaluate_transaction(payload: TransactionEvaluationRequest):
    """
    Pipeline Transaccional Completo:
    1. Triage vía SLM Router.
    2. Simulación de inferencia resiliente.
    3. Cincel Regex determinista (shield.py).
    4. Firma forense SHA-256 para Audit Trail inmutable (Cédula A).
    """
    start = time.perf_counter()

    # 1. Triage inicial con el Router
    route = HybridSLMRouter.classify_intent(payload.intent_description)

    # 2. Inferencia con mock de salida de LLM (Simulando la llamada que envuelve el decorador)
    if "PHISHING" in payload.intent_description.upper():
        raw_output = f"Alerta! Dominio sospechoso. DECISIÓN: BLOQUEO para {payload.transaction_id}."
    elif payload.pos_entry_mode == "05":
        raw_output = f"NIP verificado en POS. DECISIÓN: IMPROCEDENTE para {payload.transaction_id}."
    else:
        raw_output = f"Transacción dentro de norma. DECISIÓN: PROCEDENTE para {payload.transaction_id}."

    # 3. El Cincel Regex limpia la salida
    verdict = SovereignResilienceShield.sanitize_output(raw_output)

    # 4. Generación del Hash Forense SHA-256 (Gobernanza Cédula A)
    raw_audit = f"{payload.transaction_id}|{verdict}|{payload.amount}|{payload.auditor_credential}|{datetime.utcnow().isoformat()}"
    audit_hash = hashlib.sha256(raw_audit.encode()).hexdigest()

    latency = (time.perf_counter() - start) * 1000

    return EvaluationResponse(
        transaction_id=payload.transaction_id,
        router_agent=route.get("agent", "UNKNOWN_AGENT"),
        atomic_verdict=verdict,
        deterministic_guarantee=True,
        latency_ms=round(latency, 2),
        audit_hash_sha256=audit_hash,
        timestamp_utc=datetime.utcnow().isoformat()
    )