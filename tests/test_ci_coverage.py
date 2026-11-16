"""Regression checks for visible, token-independent CI coverage reporting."""

from pathlib import Path

import yaml


def test_coverage_is_printed_and_retained():
    workflow = yaml.safe_load(
        (Path(__file__).parents[1] / ".github/workflows/ci.yml").read_text()
    )
    steps = workflow["jobs"]["test"]["steps"]
    command = next(step["run"] for step in steps if step.get("name") == "Run tests")
    assert "--cov=pyhems" in command
    assert "--cov-report=term" in command
    assert "--cov-report=xml" in command
    assert "--cov-report=markdown:coverage.md" in command
    artifact = next(
        step for step in steps if step.get("name") == "Retain coverage reports"
    )
    assert artifact["if"] == "always()"
    assert set(artifact["with"]["path"].split()) == {"coverage.xml", "coverage.md"}
    assert artifact["with"]["if-no-files-found"] == "error"
    upload = next(step for step in steps if step.get("name") == "Upload coverage")
    assert upload["if"] == "github.repository == 'sayurin/pyhems'"
