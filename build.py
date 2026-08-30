import os
import shutil
import subprocess
import tempfile
import re
from pathlib import Path

# This script is a poetry build directive which copies the alembic migrations from the branch or rev indicated in pyproject.toml.

def build(setup_kwargs):
	destination = Path(os.getcwd()) / "migrations"
	with open("pyproject.toml","r",encoding="utf-8") as file:
		for line in file:
			if line.startswith("gearboxdatamodel"): 
				match = re.search("(?P<url>https?://[^\s]+)\",\s*(branch|rev)\s*=\s*\"(?P<branch>.*)\"",line)
				if match is not None:
					repo_url=(match.group("url"))
					branch=(match.group("branch"))
					git_args = ["git", "clone", "-b", branch, repo_url] 
					with tempfile.TemporaryDirectory() as tmpdir:
						git_args.append(tmpdir)
						try: 
							subprocess.run(
								git_args, 
								check=True, 
								capture_output=True
							)
						except subprocess.CalledProcessError as e:
							print(f"ERROR: {e.stderr}")
							raise subprocess.CalledProcessError(f"Build.py build directive error in subprocess: {e}")
						except Exception as e: 
							raise Exception(f"Build.py build directive error in subprocess: {e}")

						source_dir = Path(tmpdir) / "migrations"
						if not source_dir.exists(): 
							raise FileNotFoundError(f"{source_dir.name} not found in repo.")
						if destination.exists():
							shutil.rmtree(destination)
						shutil.copytree(source_dir, destination)
						print(f"Successfully copied {source_dir.name} to {destination}")
				else:
					raise Exception("Unable to locate gearboxDataModel dependency in pyproject.toml.")

if __name__ == "__main__":
	build({})
