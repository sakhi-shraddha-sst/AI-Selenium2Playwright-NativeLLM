import requests
import json
import re

class Selenium2PlaywrightConverter:
    def __init__(self, model="codellama"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def validate_input(self, source_code):
        if not source_code or not source_code.strip():
            return "Error: Input is empty. Please provide Selenium Java code."
        
        # Check if already Playwright
        playwright_markers = ["@playwright/test", "page.goto(", "expect(page", "await page."]
        if any(marker in source_code for marker in playwright_markers):
            return "Error: Input appears to be Playwright code already. Conversion aborted."
        
        # Check if it looks like Selenium/Java (heuristic)
        selenium_markers = ["driver.", "findElement", "By.", "org.openqa.selenium", "import java", ".click()", ".sendKeys("]
        if not any(marker in source_code for marker in selenium_markers):
            return "Error: Input does not appear to be valid Selenium Java code. Please check your source."
            
        return None

    def convert(self, source_code):
        validation_error = self.validate_input(source_code)
        if validation_error:
            return {
                "converted_code": "",
                "status": "failure",
                "error": validation_error
            }

        prompt = self._build_prompt(source_code)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0  # For determinism
            }
        }
        
        try:
            response = requests.post(self.url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                raw_output = result.get("response", "")
                converted_code = self._extract_code(raw_output)
                return {
                    "converted_code": converted_code,
                    "status": "success",
                    "error": None
                }
            else:
                return {
                    "converted_code": "",
                    "status": "failure",
                    "error": f"Ollama error: {response.status_code}"
                }
        except Exception as e:
            return {
                "converted_code": "",
                "status": "failure",
                "error": str(e)
            }

    def _build_prompt(self, source_code):
        return f"""
[INST]
You are a strict Automation Code Translator. Your goal is to convert Selenium Java into Playwright TypeScript with 100% logic fidelity.

### CRITICAL RULES - DO NOT VIOLATE:
1. **NO HALLUCINATIONS**: Your output must reflect ONLY the logic found in the Source Code.
   - If the source DOES NOT have a URL, DO NOT add one.
   - If the source ONLY finds an element and doesn't click it, DO NOT add `.click()`.
   - DO NOT add comments explaining what you did; only preserve original comments.
   - DO NOT use the word "TODO" unless there is a genuine technical impossibility.
2. **STRICT FIDELITY**: If the input is 1 line, the conversion should be approximately 1 line (inside the test wrapper).
3. **PLAYWRIGHT SYNTAX**: 
   - Use `await page.locator('selector')` or `page.getBy...` + action.
   - **PREFER Locators** over `page.$` or `page.$$`. 
   - If only finding: `const el = page.locator('xpath=//tag');`
   - **NEVER** use `.element()`. It does not exist in Playwright.
4. **FRAMEWORK WRAPPER**: 
   - Include `import {{ test, expect }} from '@playwright/test';`.
   - Wrap logic in `test('converted test', async ({{ page }}) => {{ ... }});`.

### Source Code (Java/Selenium):
{source_code}
[/INST]
"""

    def _extract_code(self, text):
        # Extract code within triple backticks if present
        code_blocks = re.findall(r"```(?:typescript|javascript|ts|js)?\n(.*?)\n```", text, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()
        return text.strip()

if __name__ == "__main__":
    test_code = """
    driver.get("https://google.com");
    WebElement search = driver.findElement(By.name("q"));
    search.sendKeys("Playwright");
    search.submit();
    """
    converter = Selenium2PlaywrightConverter()
    print(json.dumps(converter.convert(test_code), indent=2))
