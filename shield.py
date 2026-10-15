import logging
import re
import time
from functools import wraps
from typing import Callable, Any
import streamlit as st

# Configuración de observabilidad
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SovereignGuardShield")

class SovereignResilienceShield:
    """
    Capa de Soberanía Técnica: Combina reintentos resilientes ante caídas de nube (429/503)
    con sanitización determinista por Regex para evitar alucinaciones de LLMs.
    """

    @staticmethod
    def smart_retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0):
        """
        Decorador de nivel Staff: Envuelve llamadas a APIs de LLMs, atrapando fallos
        de infraestructura y reintentando en la sombra con retroceso exponencial.
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                delay = initial_delay
                for attempt in range(1, max_retries + 1):
                    try:
                        logger.info(f"🔄 [SovereignGuard Intento {attempt}/{max_retries}] Ejecutando: {func.__name__}...")
                        return func(*args, **kwargs)
                    
                    except Exception as e:
                        error_str = str(e)
                        logger.warning(f"⚠️ [Fallo de Infraestructura detectado]: {error_str}")
                        
                        # Detección de errores críticos de nube (503 / 429)
                        if "503" in error_str or "overloaded" in error_str.lower():
                            st.warning(f"⚠️ **SovereignGuard:** Nodo de IA Saturado (Intento {attempt}). Reintentando en la sombra...")
                        elif "429" in error_str or "quota" in error_str.lower():
                            st.error(f"🚨 **SovereignGuard:** Límite de Cuota Alcanzado. Aplicando backoff...")

                        if attempt == max_retries:
                            logger.error(f"🚨 [Fallo Crítico]: Se agotaron los reintentos. Activando respaldo elegante.")
                            return "FALLO_DE_INFRAESTRUCTURA_DEGRADADO"
                        
                        time.sleep(delay)
                        delay *= 2  # Retroceso exponencial
                        
                return "ERROR_INESPERADO"
            return wrapper
        return decorator

    @staticmethod
    def sanitize_output(llm_output: str) -> str:
        """
        El cincel de Talia: Limpia el ruido del LLM para entregar datos atómicos.
        """
        try:
            llm_output = str(llm_output)
            decision_pattern = r"DECISIÓN:\s*(PROCEDENTE|IMPROCEDENTE|BLOQUEO)"
            match = re.search(decision_pattern, llm_output, re.IGNORECASE)
            
            if match:
                return match.group(1).upper() 
            else:
                upper_output = llm_output.upper()
                if "PROCEDENTE" in upper_output: return "PROCEDENTE"
                if "IMPROCEDENTE" in upper_output: return "IMPROCEDENTE"
                if "BLOQUEO" in upper_output: return "BLOQUEO"
                if "FINAL ANSWER:" in upper_output:
                    return upper_output.split("FINAL ANSWER:")[-1].strip()
                return "ERROR_DE_FORMATO"
        except Exception:
            return "RESCATE_MANUAL_REQUERIDO"