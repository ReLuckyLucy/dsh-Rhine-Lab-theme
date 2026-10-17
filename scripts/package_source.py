"""Archive the committed source at HEAD using the version in VERSION."""

import os
import re
import subprocess
import sys
from pathlib import Path


VERSION_PATTERN = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?")


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def main():
    root = Path.cwd()
    try:
        version = git("show", "HEAD:VERSION").strip()
        commit = git("rev-parse", "--short=7", "HEAD")
    except subprocess.CalledProcessError as error:
        raise ValueError("请先提交 VERSION 文件和项目文件，再进行归档。") from error

    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("VERSION 必须是 1.2.3 或 1.2.3-rc.1 这样的版本号。")

    ref = os.getenv("GITHUB_REF", "")
    if ref.startswith("refs/tags/v") and ref.removeprefix("refs/tags/v") != version:
        raise ValueError(f"标签 {ref.removeprefix('refs/tags/')} 与 VERSION 中的 {version} 不一致。")

    repository = os.getenv("GITHUB_REPOSITORY", "").rsplit("/", 1)[-1] or root.name
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", repository):
        raise ValueError("仓库名称包含不能用于归档文件名的字符。")

    archive_name = f"{repository}-v{version}-{commit}"
    output_dir = root / "artifacts"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"{archive_name}.zip"
    subprocess.run(
        ["git", "archive", "--format=zip", f"--prefix={archive_name}/", f"--output={output}", "HEAD"],
        check=True,
    )
    print(output.relative_to(root).as_posix())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
