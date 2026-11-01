import sys
from pathlib import Path

# Automatically ensure repository root is in sys.path for test discovery
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
