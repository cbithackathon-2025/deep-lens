from pathlib import Path

def test_api_dockerfile_existence_and_syntax():
    dockerfile_path = Path(__file__).resolve().parent.parent / "services" / "api" / "Dockerfile"
    assert dockerfile_path.exists(), "services/api/Dockerfile must exist"

    content = dockerfile_path.read_text(encoding="utf-8")
    assert "FROM python:3.11-slim" in content
    assert "WORKDIR /app" in content
    assert "requirements.txt" in content
    assert "EXPOSE 8000" in content
    assert "uvicorn" in content
