from pathlib import Path
import sys

def test_pyproject_toml_pytest_configuration():
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    assert pyproject.exists(), "pyproject.toml must exist in repo root"

    content = pyproject.read_text(encoding="utf-8")
    assert "[tool.pytest.ini_options]" in content
    assert 'pythonpath = ["."]' in content
    assert 'testpaths = ["tests"]' in content

def test_sys_path_contains_repository_root():
    root = str(Path(__file__).resolve().parent.parent)
    assert any(Path(p).resolve() == Path(root).resolve() for p in sys.path)
