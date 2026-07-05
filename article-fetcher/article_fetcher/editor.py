import os
import shlex
import subprocess
import tempfile
from pathlib import Path


def edit_in_editor(initial_text: str, *, suffix: str = ".md") -> str:
    editor_cmd = os.environ.get("EDITOR", "vi")
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding="utf-8") as tmp:
        tmp.write(initial_text)
        tmp_path = Path(tmp.name)
    try:
        subprocess.run(shlex.split(editor_cmd) + [str(tmp_path)], check=True)
        return tmp_path.read_text(encoding="utf-8")
    finally:
        tmp_path.unlink(missing_ok=True)


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} [y/N] ").strip().lower()
    return answer == "y"
