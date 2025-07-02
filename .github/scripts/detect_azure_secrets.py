import re
import sys
import json
import os
from typing import Union
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r'[\'"]?subscription_id[\'"]?\s*[:=]\s*[\'"][0-9a-f\-]{36}[\'"]', re.IGNORECASE),
    re.compile(r'[\'"]?resource_group_name[\'"]?\s*[:=]\s*[\'"][a-zA-Z0-9\-_]+[\'"]', re.IGNORECASE),
    re.compile(r'[\'"]?project_name[\'"]?\s*[:=]\s*[\'"][a-zA-Z0-9\-_]+[\'"]', re.IGNORECASE),
    re.compile(r'[\'"]?api_key[\'"]?\s*[:=]\s*[\'"][A-Za-z0-9\-_]{40,}[\'"]', re.IGNORECASE),
    re.compile(
        r'[\'"]?azure_endpoint[\'"]?\s*[:=]\s*[\'"]https:\/\/[a-zA-Z0-9\-\.]+\.azure\.com[\/a-zA-Z0-9\.\-]*[\'"]',
        re.IGNORECASE,
    ),
    re.compile(r'export\s+[A-Z_][A-Z0-9_]*\s*=\s*["\'][^"\']+["\']', re.IGNORECASE),
    re.compile(
        r'os\.environ\[\s*["\']\s*[A-Za-z0-9_]*(API_KEY|ENDPOINT|PROJECT_NAME|SUBSCRIPTION_ID|RESOURCE_GROUP)[A-Za-z0-9_]*\s*["\']\s*\]\s*=\s*["\'][^"\']+["\']',
        re.IGNORECASE,
    ),
]


def check_ipynb_for_secrets(filename: Union[str, os.PathLike]) -> bool:
    """Jupyter notebooks can't be parsed directly - need to convert to JSON first"""
    try:
        with Path(filename).open("r", encoding="utf-8") as file:
            notebook_data = json.load(file)
            failed = False
            for cell in notebook_data.get("cells", []):
                if cell["cell_type"] == "code":
                    for line_number, line in enumerate(cell["source"], start=1):
                        for pattern in SECRET_PATTERNS:
                            if pattern.search(line):
                                print(f"Secret detected in {filename} on line {line_number}: {line.strip()}")
                                failed = True
            return failed
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Failed to read {filename}. Skipping secrets check. Error: {e}")
        return True


def main() -> None:
    failed = False

    for filename in sys.argv[1:]:
        if filename.endswith((".py", ".yaml", ".yml", ".md")):
            try:
                with Path(filename).open("r", encoding="utf-8") as file:
                    for line_number, line in enumerate(file, start=1):
                        for pattern in SECRET_PATTERNS:
                            if pattern.search(line):
                                print(f"Secret detected in {filename} on line {line_number}: {line.strip()}")
                                failed = True
            except UnicodeDecodeError:
                print(f"Failed to read {filename}. Skipping secrets check.")
        elif filename.endswith(".ipynb") and check_ipynb_for_secrets(filename):
            failed = True

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
