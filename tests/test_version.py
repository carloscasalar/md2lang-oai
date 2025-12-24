"""Test version consistency between pyproject.toml and CHANGELOG.md."""

import re
from pathlib import Path


def test_version_matches_changelog():
    """Verify that pyproject.toml version matches the latest CHANGELOG.md version."""
    root = Path(__file__).parent.parent

    # Read version from pyproject.toml
    pyproject = (root / "pyproject.toml").read_text()
    version_match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
    assert version_match, "Could not find version in pyproject.toml"
    project_version = version_match.group(1)

    # Read latest version from CHANGELOG.md
    changelog = (root / "CHANGELOG.md").read_text()
    # Match lines like: ## [1.1.0] - 2025-12-24 or ## [Unreleased]
    changelog_versions = re.findall(r"^##\s+\[([^\]]+)\]", changelog, re.MULTILINE)
    assert changelog_versions, "Could not find any versions in CHANGELOG.md"
    latest_changelog_version = changelog_versions[0]

    # Allow [Unreleased] for in-progress changes
    if latest_changelog_version.lower() == "unreleased":
        # If unreleased is present, check the second entry
        assert len(changelog_versions) >= 2, "CHANGELOG.md should have at least one released version"
        latest_changelog_version = changelog_versions[1]

    assert project_version == latest_changelog_version, (
        f"Version mismatch: pyproject.toml has '{project_version}' "
        f"but CHANGELOG.md has '{latest_changelog_version}'"
    )
