import logging

# Configuración de logging para observabilidad
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SovereignShield")

class SovereignResilienceShield:
    """
    Capa de protección de infraestructura: Intercepta caídas de proveedores de IA 
    antes de que afecten la experiencia del usuario o saturen el sistema.
    """
    @staticmethod
    def handle_infrastructure_errors(error_code: str) -> str:
        if error_code == "503":
            logger.warning("⚠️ [SovereignGuard]: Nodo de IA Saturado (503). Activando Shadow Retry...")
            return "INFRA_LATENCY_RETRY (Shadow Retry Activated)"
        elif error_code == "429":
            logger.error("🚨 [SovereignGuard]: Límite de Cuota Alcanzado (429). Pausando throughput...")
            return "QUOTA_EXCEEDED_HALT"
        return "SUCCESS"