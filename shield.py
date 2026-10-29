"""
SovereignGuard AI - Core Resilience & Deterministic Shield Engine
Autor: Talia González López (Applied AI Architect)
Propiedad Intelectual Soberana - Grado Enterprise
"""

import logging
import re
import time
from functools import wraps
from typing import Callable, Any, Dict, Union

# Configuración de observabilidad pura para microservicios y servidores
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] [SovereignShield] %(message)s"
)
logger = logging.getLogger("SovereignGuardShield")


class SovereignResilienceShield:
    """
    Capa de Soberanía Técnica:
    Combina reintentos resilientes ante saturación de nube (429/503)
    con sanitización determinista por Regex para neutralizar alucinaciones.
    Completamente agnóstica a la UI (desacoplada de Streamlit).
    """

    @staticmethod
    def smart_retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0):
        """
        Decorador de nivel Staff: Envuelve llamadas a APIs de LLMs, atrapando fallos
        de red e infraestructura y reintentando con retroceso exponencial.
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                delay = initial_delay
                for attempt in range(1, max_retries + 1):
                    try:
                        logger.info(f"🔄 [Intento {attempt}/{max_retries}] Invocando inferencia en: {func.__name__}...")
                        return func(*args, **kwargs)
                    
                    except Exception as e:
                        error_str = str(e)
                        logger.warning(f"⚠️ [Fallo detectado en intento {attempt}]: {error_str}")
                        
                        # Detección de sobrecarga o límites de cuota (503 / 429)
                        if "503" in error_str or "overloaded" in error_str.lower():
                            logger.warning(f"⏳ Nodo de IA Saturado (503). Aplicando espera estratégica de {delay}s...")
                        elif "429" in error_str or "quota" in error_str.lower():
                            logger.error(f"🛑 Límite de Cuota Alcanzado (429). Activando retroceso exponencial ({delay}s)...")

                        # Si se agotan los reintentos, degradación elegante (sin colapso 500)
                        if attempt == max_retries:
                            logger.error("🚨 [Fallo Crítico]: Reintentos agotados. Activando contingencia de degradación.")
                            return "FALLO_DE_INFRAESTRUCTURA_DEGRADADO"
                        
                        time.sleep(delay)
                        delay *= 2  # Retroceso exponencial (1s -> 2s -> 4s)
                        
                return "ERROR_INESPERADO"
            return wrapper
        return decorator

    @staticmethod
    def handle_infrastructure_errors(error: Union[str, Exception]) -> Dict[str, str]:
        """
        Manejo determinista de códigos de error de nube inyectados o interceptados.
        Sincronizado con router.py y app_pagos.py.
        """
        err_msg = str(error).upper()

        if "503" in err_msg or "OVERLOADED" in err_msg:
            logger.warning("🛡️ Intercepción de Escudo: Error 503 (Servicio Sobrecargado).")
            return {
                "status": "CIRCUIT_BREAKER_TRIGGERED",
                "action": "Tráfico pausado. Redirigiendo a nodo SLM secundario.",
                "retry_recommended": "True"
            }
        
        elif "429" in err_msg or "QUOTA" in err_msg:
            logger.warning("🛡️ Intercepción de Escudo: Error 429 (Límite de Cuota).")
            return {
                "status": "RATE_LIMIT_ENGAGED",
                "action": "Activando backoff exponencial silencioso en la capa intermedia.",
                "retry_recommended": "True"
            }
        
        logger.error(f"🛡️ Intercepción de Escudo: Error no clasificado ({err_msg}).")
        return {
            "status": "UNHANDLED_INFRA_FAULT",
            "action": "Derivando a revisión de Auditoría de Sistemas.",
            "retry_recommended": "False"
        }

    @staticmethod
    def sanitize_output(llm_output: str) -> str:
        """
        El Cincel de Talia: Filtra y limpia el ruido probabilístico del LLM 
        para garantizar datos atómicos en el Switch Transaccional.
        """
        try:
            llm_output = str(llm_output)
            # Extracción quirúrgica mediante Regex
            decision_pattern = r"DECISIÓN:\s*(PROCEDENTE|IMPROCEDENTE|BLOQUEO)"
            match = re.search(decision_pattern, llm_output, re.IGNORECASE)
            
            if match:
                return match.group(1).upper()
            
            # Fallback determinista de seguridad
            upper_output = llm_output.upper()
            if "PROCEDENTE" in upper_output: 
                return "PROCEDENTE"
            if "IMPROCEDENTE" in upper_output: 
                return "IMPROCEDENTE"
            if "BLOQUEO" in upper_output: 
                return "BLOQUEO"
            if "FINAL ANSWER:" in upper_output:
                return upper_output.split("FINAL ANSWER:")[-1].strip()
            
            return "ERROR_DE_FORMATO"

        except Exception as e:
            logger.error(f"Error durante sanitización regex: {e}")
            return "RESCATE_MANUAL_REQUERIDO"