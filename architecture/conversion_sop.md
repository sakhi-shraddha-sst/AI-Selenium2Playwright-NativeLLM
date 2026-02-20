# Conversion SOP - Selenium to Playwright

## Goal
Convert Selenium Java test code to Playwright TypeScript/JavaScript using local CodeLlama while preserving business logic and ensuring determinism.

## Inputs
- `source_code`: The Selenium Java source code.
- `target_language`: Defaulting to Playwright TypeScript.

## Outputs
- `converted_code`: Runnable Playwright code that complies with `@playwright/test` standard.
- `metadata`: Execution stats.

## Framework Compliance Rules
1. **Runner Ready**: Code must be wrapped in `test(...)` and include `import { test, expect } from '@playwright/test'`.
2. **Modern Locators**: Prioritize `getByRole`, `getByLabel`, `getByPlaceholder`, and `getByTestId` over CSS/XPath where possible.
3. **Async/Await**: Ensure all Playwright actions and assertions are correctly awaited.
4. **Assertions**: Convert JUnit/TestNG assertions to Playwright `expect` assertions.

## Tool Responsibilities
- `converter_tool.py`: Handles interaction with Ollama, prompt engineering, and code cleanup.

## Execution Flow
1. **Sanitize**: Remove unnecessary imports and boilerplate from Selenium input.
2. **Contextualize**: Build the prompt for CodeLlama with clear instructions and behavioral rules.
3. **Inference**: Call Ollama API with the prompt.
4. **Post-Process**: Extract code from LLM response, fix common conversion artifacts.
5. **Validate**: Check for basic syntax correctness (optional but recommended).

## Edge Cases
- **Unknown APIs**: If CodeLlama doesn't know a mapping, it must insert a `// TODO`.
- **Complex Assertions**: Ensure Hard/Soft assertions are mapped correctly.
- **Dynamic Waits**: Prefer Playwright auto-waiting over explicit Thread.sleep or WebDriverWait.

## Failure Handling
- If Ollama is unreachable, return a clear error status via the API.
- If conversion fails to produce code, log the error and notify the UI.
