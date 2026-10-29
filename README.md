# 🛡️ **SovereignGuard AI: The Resilience Orchestrator**

**Hardening Agentic Workflows for High-Availability Financial & Enterprise Systems** 
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red.svg)
![Orchestration](https://img.shields.io/badge/AI-SLM%20%2F%20Multi--Agent-green.svg)
![Sovereignty](https://img.shields.io/badge/Sovereignty-Proprietary-orange.svg)

---

## 📑 Executive Summary

**SovereignGuard AI** no es una implementación de IA convencional; es una **Capa de Resiliencia Determinista y Enrutamiento Híbrido** diseñada para proteger la integridad operacional, minimizar la latencia y controlar los costos de inferencia en sistemas empresariales y de alta frecuencia.

Diseñado para resolver el *"Reliability Gap"* (Brecha de Confiabilidad) y los costos descontrolados de los modelos de lenguaje actuales, SovereignGuard asegura que la automatización agéntica nunca comprometa la Atomicidad de los Datos, la seguridad de la infraestructura ni la soberanía de decisión humana.

🔗 **Live HITL Audit Demo:** [s-guard-ai.streamlit.app](https://s-guard-ai.streamlit.app)

---

## 🚀 Key Technical Differentiators

### 1. Decoupled REST Microservice Layer (FastAPI Core)
* **Arquitectura Orientada a Servicios:** El motor central está desacoplado de la interfaz gráfica y expuesto mediante endpoints REST asíncronos en **FastAPI**, permitiendo su consumo directo por backends bancarios, aplicaciones móviles o switches transaccionales:
  * `GET /health`: Liveness y readiness probe para balanceadores de carga y orquestadores (AWS/K8s).
  * `POST /v1/router/classify`: Enrutador SLM de ultra-baja latencia (<1.5s) para triage de intenciones.
  * `POST /v1/shield/sanitize`: Intercepción y extracción determinista de datos atómicos vía Regex.
  * `POST /v1/guard/evaluate`: Pipeline transaccional de extremo a extremo con firma criptográfica forense SHA-256.

### 2. Hybrid SLM Router & Token Economy (<1.5s Latency)
* **Enrutamiento de Baja Latencia:** Utiliza modelos de lenguaje pequeños (*Small Language Models - SLMs*) optimizados para tareas deterministas de alta frecuencia, respondiendo en menos de 1.5 segundos.
* **Economía de Tokens:** Evita el uso innecesario de LLMs pesados de frontera para tareas repetitivas, reduciendo los costos operativos de inferencia en más de un 70%.

### 3. 🛡️ SovereignResilienceShield & Decorador de Reintento
Para garantizar una disponibilidad del 99.9% en entornos transaccionales, SovereignGuard incorpora una capa de protección agnóstica de infraestructura:
* **Smart Retry with Exponential Backoff (`smart_retry_with_backoff`):** Decorador de nivel Staff que envuelve llamadas críticas a APIs de IA, reintentando de forma silenciosa (*shadow retry*) y duplicando el tiempo de espera para mitigar saturaciones de nube (429 Rate Limits / 503 Overloaded).
* **Cincel Determinista (Regex Sanitizer):** Capa de saneamiento que intercepta las respuestas caóticas o conversacionales de los LLMs y las convierte en datos atómicos y estructurados (`PROCEDENTE`, `IMPROCEDENTE`, `BLOQUEO`), previniendo alucinaciones en el core transaccional.

### 4. Human-in-the-Loop (HITL) & Immutable Audit Trail
* **Panel de Soberanía Operativa:** Impide que los agentes ejecuten acciones destructivas (*Ghost Approvals*). El sistema congela la ejecución hasta recibir el veredicto humano mediante controles estrictos: **`Proceed`**, **`Modify`**, o **`Reject`**.
* **Trazabilidad Forense:** Cada decisión humana queda registrada en una bitácora inmutable en tiempo real con firma criptográfica SHA-256 y trazabilidad de credenciales regulatorias (Cédula A).

---

## 🏗️ Architecture & Modular Design

El repositorio está estructurado bajo principios estrictos de *Clean Code* y desacoplamiento para garantizar escalabilidad:

```text
sovereign-guard-suite/
│
├── .gitignore
├── requirements.txt   # Dependencias de producción (FastAPI, Uvicorn, Streamlit, Pandas)
├── shield.py          # Capa de Resiliencia Desacoplada (Escudo Regex y Backoff Exponencial)
├── router.py          # Lógica del Hybrid SLM Router y optimización de tokens
├── api.py             # Microservicio REST Core (FastAPI / Endpoints transaccionales)
├── app.py             # Panel de Control Principal (Streamlit Dashboard & Auditoría HITL)
└── app_pagos.py       # Triage transaccional financiero bajo protocolo ISO 8583
```
## ⚡ Quickstart

### 1. Levantar el Microservicio REST (FastAPI Backend)
```bash
uvicorn api:app --reload --port 8000
```
*Documentación interactiva Swagger disponible automáticamente en: [http://localhost:8000/docs](http://localhost:8000/docs)*

### 2. Levantar el Panel de Auditoría HITL (Streamlit Dashboard)
```bash
streamlit run app.py
```

## 💡 Core Philosophy: Sovereign Engineering
*"La mayoría de los agentes de IA operan en un vacío probabilístico. Si tu arquitectura no permite el control determinista, la memoria relacional y la soberanía humana, tu automatización se romperá en cuanto los procesos dependan de más de un factor crítico."*

-Talia González López, Applied AI Architect.


## 📬 **Contact & Professional Links**

Talia González López
* Applied AI Architec
* Founder of [#AgenticBuildersLATAM](https://www.linkedin.com/groups/37010179/)
* [LinkedIn](https://www.linkedin.com/in/talia-gonzalezl/)
* [Live App](https://s-guard-ai.streamlit.app)
* Technical Briefings & War Stories: [YouTube Channel - Agentic AI War Stories](https://www.youtube.com/@TaliaGonzalezL749)
