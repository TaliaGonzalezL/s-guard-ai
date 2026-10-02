from typing import Dict, Any
from shield import SovereignResilienceShield

class HybridSLMRouter:
    """
    Simula un SLM optimizado para ruteo de baja latencia (<1.5s) 
    en una arquitectura multi-agente.
    """
    @staticmethod
    def classify_intent(query: str) -> Dict[str, Any]:
        query_upper = query.upper()
        
        # Interceptando fallos de infraestructura mediante el escudo
        if "503" in query_upper or "OVERLOADED" in query_upper:
            shield_action = SovereignResilienceShield.handle_infrastructure_errors("503")
            return {"agent": "SYSTEM_SHIELD", "action": shield_action, "type": "error"}
        
        if "429" in query_upper or "QUOTA" in query_upper:
            shield_action = SovereignResilienceShield.handle_infrastructure_errors("429")
            return {"agent": "SYSTEM_SHIELD", "action": shield_action, "type": "error"}

        # Ruteo de intención financiera
        if any(word in query_upper for word in ["FRAUDE", "ROBO", "CARGO NO RECONOCIDO", "ACLARACION"]):
            return {"agent": "FRAUD_DISPUTE_AGENT", "model": "SLM-Fast-Router (7B)", "routing_cost": "Low ($0.0001)", "type": "success"}
        
        elif any(word in query_upper for word in ["PRESTAMO", "CREDITO", "PAGO", "SALDO", "DEUDA"]):
            return {"agent": "LENDING_OPERATIONS_AGENT", "model": "SLM-Fast-Router (7B)", "routing_cost": "Low ($0.0001)", "type": "success"}
            
        else:
            return {"agent": "GENERAL_SUPPORT_AGENT", "model": "SLM-Fast-Router (7B)", "routing_cost": "Low ($0.0001)", "type": "info"}