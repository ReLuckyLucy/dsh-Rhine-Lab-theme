import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "package_source.py"


class PackageSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "example-repo"
        self.repo.mkdir()
        (self.repo / "VERSION").write_text("1.2.3\n", encoding="utf-8")
        (self.repo / "README.md").write_text("example\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "add", "VERSION", "README.md"], cwd=self.repo, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Template Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "initial"],
            cwd=self.repo,
            check=True,
        )
        self.sha = subprocess.check_output(["git", "rev-parse", "--short=7", "HEAD"], cwd=self.repo, text=True).strip()

    def run_script(self, ref):
        env = os.environ.copy()
        env.update({"GITHUB_REPOSITORY": "example/example-repo", "GITHUB_REF": ref})
        return subprocess.run(
            [sys.executable, str(SCRIPT)], cwd=self.repo, env=env, text=True, capture_output=True
        )

    def test_branch_push_packages_committed_files_with_version_and_commit(self):
        (self.repo / "untracked-secret.txt").write_text("not archived", encoding="utf-8")
        result = self.run_script("refs/heads/main")
        self.assertEqual(result.returncode, 0, result.stderr)
        archive = self.repo / result.stdout.strip()
        self.assertEqual(archive.name, f"example-repo-v1.2.3-{self.sha}.zip")
        with zipfile.ZipFile(archive) as package:
            self.assertIn(f"example-repo-v1.2.3-{self.sha}/README.md", package.namelist())
            self.assertNotIn("untracked-secret.txt", "\n".join(package.namelist()))

    def test_tag_must_match_version_file(self):
        result = self.run_script("refs/tags/v1.2.4")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("VERSION", result.stderr)

    def test_matching_tag_uses_the_same_package_name(self):
        result = self.run_script("refs/tags/v1.2.3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(result.stdout.strip()).name, f"example-repo-v1.2.3-{self.sha}.zip")

    def test_copied_template_archives_its_workflow_and_readme(self):
        copied = Path(self.temp.name) / "copied-template"
        copied.mkdir()
        for entry in ("VERSION", "README.md", "LICENSE", ".gitignore", ".github", "img", "screenshots", "scripts", "tests"):
            source = SCRIPT.parents[1] / entry
            destination = copied / entry
            if source.is_dir():
                shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(source, destination)
        subprocess.run(["git", "init", "-q"], cwd=copied, check=True)
        subprocess.run(["git", "-c", "core.autocrlf=false", "add", "."], cwd=copied, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Template Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "template"],
            cwd=copied,
            check=True,
        )
        result = subprocess.run(
            [sys.executable, "scripts/package_source.py"], cwd=copied, text=True, capture_output=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(copied / result.stdout.strip()) as package:
            names = "\n".join(package.namelist())
            self.assertIn("/.github/workflows/archive.yml", names)
            self.assertIn("/README.md", names)
            self.assertNotIn("__pycache__", names)


if __name__ == "__main__":
    unittest.main()
