# Selenium to Playwright converter by local LLM - Findings

## Research
- Goal: Convert Selenium Java code to Playwright (JS/TS) using Local CodeLlama.
- Model: CodeLlama (likely via Ollama or local llama-cpp).

## Constraints
- Must follow B.L.A.S.T. protocol.
- Must result in a one-click runnable application with an HTML UI.
- **Strictly Offline**: No external API calls allowed.

## Integration Notes
- Backend: Python (Flask/FastAPI) to interface with local model.
- Model Runner: Needs to check if Ollama is running or use a dedicated local library.
- Frontend: HTML/CSS/JS (Vanilla) for UI.

## Technical Discoveries
- Need to verify CodeLlama availability on the system.
- Need to define the prompt template for deterministic conversion.
