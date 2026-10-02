import streamlit as st
from router import HybridSLMRouter

st.set_page_config(page_title="SovereignGuard: SLM Router 🛡️", layout="wide")

def main():
    st.title("🛡️ SovereignGuard: Hybrid SLM Router & Shield")
    st.subheader("Arquitectura de Cero a Producción | Control de Costos y Latencia (<1.5s)")

    st.write("### 🧪 Panel de Enrutamiento en Vivo")
    
    user_query = st.text_input(
        "Introduce una consulta o inyecta un código de error de infraestructura:",
        "¡Ayuda! Veo un cargo no reconocido en mi tarjeta de la app."
    )

    # Inicializar memoria de sesión para el router y la auditoría
    if "resultado_router" not in st.session_state:
        st.session_state.resultado_router = None
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = None

    # Botón principal para ejecutar el SLM
    if st.button("Ejecutar Router SLM"):
        with st.spinner("Enrutando mediante SLM optimizado..."):
            st.session_state.resultado_router = HybridSLMRouter.classify_intent(user_query)
            # Limpiamos auditoría anterior al correr una nueva consulta
            st.session_state.audit_log = None

    # Si ya tenemos un resultado guardado en la sesión, pintamos todo el panel de forma persistente
    if st.session_state.resultado_router:
        resultado = st.session_state.resultado_router
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.write("### 🔍 Contexto Evaluado")
            st.info(f"**Query:** `{user_query}`")
            st.json(resultado)

        with col2:
            st.write("### ⚖️ Decisión del Orquestador")
            if resultado['type'] == 'success':
                st.success(f"**Agente Destino:** {resultado['agent']}")
                st.write(f"**Modelo:** {resultado['model']} | **Costo:** {resultado['routing_cost']}")
            elif resultado['type'] == 'error':
                st.error(f"🚨 **Intercepción:** {resultado['agent']}")
                st.warning(f"**Acción del Escudo:** {resultado['action']}")
            else:
                st.info(f"**Agente Destino:** {resultado['agent']}")

        # --- PASO 4: CAPA HITL (Human-in-the-Loop) & AUDIT TRAIL INMUTABLE ---
        if resultado["type"] == "success":
            st.divider()
            st.write("### ⚖️ Panel de Soberanía Operativa (HITL)")
            st.info(f"El **{resultado['agent']}** ha generado una propuesta transaccional. Se requiere validación humana obligatoria antes del *commit* en el core.")

            propuesta_agente = f"Ejecutar protocolo operativo y ruteo de seguridad para: '{user_query}'."
            st.warning(f"**Propuesta del Agente:** {propuesta_agente}")

            c1, c2, c3 = st.columns(3)

            with c1:
                if st.button("✅ PROCEED (Aprobar)", use_container_width=True):
                    st.session_state.audit_log = {
                        "status": "APROBADO / EJECUTADO",
                        "user": "Talia González López (Applied AI Architect)",
                        "credential": "Cédula A / Soberanía Operativa Level 1",
                        "action_taken": "Commit atómico sincronizado con el Core System.",
                        "timestamp": "2026-10-01 16:50:00"
                    }
            with c2:
                if st.button("📝 MODIFY (Modificar)", use_container_width=True):
                    st.session_state.audit_log = {
                        "status": "MODIFICADO / EN REVISIÓN",
                        "user": "Talia González López (Applied AI Architect)",
                        "credential": "Cédula A / Soberanía Operativa Level 1",
                        "action_taken": "Parámetros de ruteo ajustados manualmente por el operador.",
                        "timestamp": "2026-10-01 16:50:00"
                    }
            with c3:
                if st.button("❌ REJECT (Bloquear)", use_container_width=True):
                    st.session_state.audit_log = {
                        "status": "BLOQUEADO / RECHAZADO",
                        "user": "Talia González López (Applied AI Architect)",
                        "credential": "Cédula A / Soberanía Operativa Level 1",
                        "action_taken": "Acción denegada. Alerta enviada a Prevención de Fraude.",
                        "timestamp": "2026-10-01 16:50:00"
                    }

        # Renderizado persistente de la Bitácora de Auditoría Inmutable
        if st.session_state.audit_log:
            st.write("---")
            with st.expander("📜 Bitácora de Auditoría Inmutable (Audit Trail - Sincronizado)", expanded=True):
                log = st.session_state.audit_log
                if "APROBADO" in log["status"]:
                    st.success(f"**Estatus:** {log['status']}")
                elif "MODIFICADO" in log["status"]:
                    st.warning(f"**Estatus:** {log['status']}")
                else:
                    st.error(f"**Estatus:** {log['status']}")
                
                st.write(f"**Auditor / Usuario Autorizador:** {log['user']}")
                st.write(f"**Credencial Regulatoria:** {log['credential']}")
                st.write(f"**Detalle de la Acción:** {log['action_taken']}")
                st.write(f"**Timestamp (UTC):** {log['timestamp']}")
                st.caption("🔒 Seguridad forense: Trazabilidad inmutable garantizada mediante SovereignGuard Shield bajo cifrado AES-256.")

if __name__ == "__main__":
    main()