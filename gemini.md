# Selenium to Playwright converter by local LLM - Constitution

## Data Schemas

### Request Schema (Frontend to Backend)
```json
{
  "source_code": "string",
  "filename": "string",
  "source_type": "text | file"
}
```

### Response Schema (Backend to Frontend)
```json
{
  "converted_code": "string",
  "status": "success | failure",
  "error": "string | null",
  "metadata": {
    "model": "CodeLlama",
    "conversion_time": "float"
  }
}
```

## Behavioral Rules
1.  **Deterministic Output**: Same Selenium input must yield the same Playwright output.
2.  **Logic Preservation**: Maintain test intent, flow, and comments. No invented logic.
3.  **Local Only**: Strictly no cloud APIs. Use local CodeLlama.
4.  **Graceful Degeneracy**: If a mapping is unknown, insert a `// TODO: [Explanation]` instead of hallucinating.
5.  **Clean Separation**: UI handles display; Tools/Backend handle LLM inference.
6.  **No Inference**: Do not guess selectors; use what is provided in the source.

## System Constraints
- One-click launch requirement.
- UI-Logic separation.
- No direct script execution by user.

## Architectural Invariants
- Deterministic tools.
- Decision layer (navigation) separate from processing.
- **Framework Compliance**: Every conversion must produce a standard `@playwright/test` file structure, not just a code snippet.

## Maintenance Log
- [2026-02-20] Constitution established.
