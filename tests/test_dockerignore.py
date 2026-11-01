from pathlib import Path

def test_dockerignore_configuration():
    dockerignore_path = Path(__file__).resolve().parent.parent / ".dockerignore"
    assert dockerignore_path.exists(), ".dockerignore must exist in repository root"

    content = dockerignore_path.read_text(encoding="utf-8")
    patterns = [".git", "__pycache__", ".venv", ".pytest_cache", ".env"]
    for pattern in patterns:
        assert pattern in content, f".dockerignore must exclude {pattern}"
