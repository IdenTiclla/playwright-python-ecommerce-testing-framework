# Practicing Playwright Python

## Description
This project is a simple demonstration of using Playwright for browser automation in Python.

## Requirements
- Python >= 3.12
- `uv` package manager (optional but recommended)

## Installation

### For Windows Users

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd practicing-playwright-python
   ```

2. **Install `uv`**:
   Open PowerShell as administrator and run:
   ```powershell
   (Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -UseBasicParsing).Content | powershell
   ```

3. **Create a virtual environment**:
   ```powershell
   uv venv
   ```

4. **Activate the virtual environment**:
   ```powershell
   .venv\Scripts\activate
   ```

5. **Install Playwright**:
   ```powershell
   uv pip install playwright
   ```

6. **Install the required browsers**:
   ```powershell
   playwright install
   ```

### For macOS Users

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd practicing-playwright-python
   ```

2. **Install `uv`**:
   You can install `uv` using the following command:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create a virtual environment**:
   ```bash
   uv venv
   ```

4. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

5. **Install Playwright**:
   ```bash
   uv pip install playwright
   ```

6. **Install the required browsers**:
   ```bash
   playwright install
   ```

### For Ubuntu Users

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd practicing-playwright-python
   ```

2. **Install `uv`**:
   You can install `uv` using the following command:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create a virtual environment**:
   ```bash
   uv venv
   ```

4. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

5. **Install Playwright**:
   ```bash
   uv pip install playwright
   ```

6. **Install the required browsers**:
   ```bash
   playwright install
   ```

## Usage

1. **Run the test script**:
   Create a file named `test_playwright.py` with the following content:
   ```python
   from playwright.sync_api import sync_playwright

   def main():
       with sync_playwright() as p:
           browser = p.chromium.launch(headless=False)
           page = browser.new_page()
           page.goto('https://example.com')
           print(f"Title: {page.title()}")
           browser.close()

   if __name__ == '__main__':
       main()
   ```

2. **Execute the script**:
   ```bash
   python test_playwright.py
   ```

## Updating Browsers
To update the browsers that Playwright will automate, run:
```bash
playwright install
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.