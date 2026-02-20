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
You are an expert Automation Engineer. Convert the following Selenium Java test code into a fully runnable Playwright TypeScript test file.

### Requirements for Runnability:
1. Use the `@playwright/test` framework structure: `import {{ test, expect }} from '@playwright/test';`.
2. Wrap the test logic in a `test('converted selenium test', async ({{ page }}) => {{ ... }});` block.
3. Map all Selenium actions (navigation, find element, click, sendKeys, assertions) to their Playwright equivalents.
4. Use modern locators like `page.getByRole()`, `page.getByLabel()`, `page.getByPlaceholder()`, or `page.locator()`.
5. Handle assertions using the `expect` library (e.g., `await expect(page.locator(...)).toBeVisible()`).
6. Preserve all original comments and test logic flow.
7. If a mapping is unknown, insert a `// TODO: [Explanation]`.
8. DO NOT return any conversational text. Return ONLY the code inside the code block.

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
    driver.get("https://example.com");
    driver.findElement(By.id("login")).click();
    driver.findElement(By.name("username")).sendKeys("testuser");
    """
    converter = Selenium2PlaywrightConverter()
    print(json.dumps(converter.convert(test_code), indent=2))
