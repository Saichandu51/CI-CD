import os
import subprocess
import json
from pathlib import Path
import tempfile

# Settings
ARTIFACT_NAME = "ci-status"
DEST_FILE = "data/ci_status.json"

# Create data dir if not exists
Path("data").mkdir(exist_ok=True)

try:
    # Get latest workflow run ID
    result = subprocess.run(
        ["gh", "run", "list", "--limit", "1", "--json", "databaseId", "--jq", ".[0].databaseId"],
        capture_output=True, text=True, check=True
    )
    run_id = result.stdout.strip()

    print(f"Fetching artifact from run ID: {run_id}")

    # Use a temp directory to extract the artifact
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(
            ["gh", "run", "download", run_id, "-n", ARTIFACT_NAME, "-D", tmpdir],
            check=True
        )

        # Copy to data/ci_status.json
        src = Path(tmpdir) / "ci_status.json"
        dst = Path(DEST_FILE)

        if src.exists():
            dst.write_text(src.read_text())
            print(f"Updated {DEST_FILE}")
        else:
            print("ci_status.json not found in artifact.")
except subprocess.CalledProcessError as e:
    print(f"Error fetching CI status: {e}")
