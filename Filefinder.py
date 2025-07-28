import subprocess
import sys
from pathlib import Path

VENV_DIR = Path("./sbom_backend_venv")
REQUIREMENTS_FILE = Path("requirements.txt")
MAIN_SCRIPT = Path("Main.py")


def run(cmd, check=True):
    print(f"[cmd] {' '.join(map(str, cmd))}")
    subprocess.run(cmd, check=check)


def main():
    if not sys.executable:
        print("[!] Python interpreter not found.")
        sys.exit(1)

    print(f"[i] Using Python interpreter: {sys.executable}")

    if not VENV_DIR.exists():
        print("[i] Creating virtual environment...")
        run([sys.executable, "-m", "venv", str(VENV_DIR)])

    pip_path = VENV_DIR / "bin" / "pip"
    python_path = VENV_DIR / "bin" / "python"
    if not pip_path.exists():
        pip_path = VENV_DIR / "Scripts" / "pip.exe"
        python_path = VENV_DIR / "Scripts" / "python.exe"

    if not pip_path.exists() or not python_path.exists():
        print("[!] Virtual environment tools not found.")
        sys.exit(1)

    run([str(pip_path), "install", "--upgrade", "pip"])

    if REQUIREMENTS_FILE.exists():
        print(f"[i] Installing dependencies from {REQUIREMENTS_FILE}...")
        run([str(pip_path), "install", "-r", str(REQUIREMENTS_FILE)])
    else:
        print(f"[!] {REQUIREMENTS_FILE} not found.")
        sys.exit(1)

    if MAIN_SCRIPT.exists():
        print(f"[i] Running {MAIN_SCRIPT}...")
        run([str(python_path), str(MAIN_SCRIPT)])
    else:
        print(f"[!] {MAIN_SCRIPT} not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()