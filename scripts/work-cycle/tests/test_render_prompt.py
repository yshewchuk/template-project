import pytest

from render_prompt import render_template


class TestRenderTemplate:
    def test_simple_substitution(self):
        template = "Hello {{name}}, welcome to {{place}}."
        result = render_template(template, {"name": "Alice", "place": "Wonderland"})
        assert result == "Hello Alice, welcome to Wonderland."

    def test_multiple_occurrences(self):
        template = "{{x}} + {{x}} = 2 * {{x}}"
        result = render_template(template, {"x": "5"})
        assert result == "5 + 5 = 2 * 5"

    def test_whitespace_in_braces(self):
        template = "{{ name }} and {{  name  }}"
        result = render_template(template, {"name": "Bob"})
        assert result == "Bob and Bob"

    def test_undefined_variable_left_as_is(self, capsys):
        template = "Hello {{name}}, age {{age}}"
        result = render_template(template, {"name": "Bob"})
        assert result == "Hello Bob, age {{age}}"
        captured = capsys.readouterr()
        assert "undefined template variable 'age'" in captured.err

    def test_empty_template(self):
        result = render_template("", {})
        assert result == ""

    def test_no_placeholders(self):
        template = "Just plain text, no variables here."
        result = render_template(template, {"x": "unused"})
        assert result == "Just plain text, no variables here."

    def test_multiline_template(self):
        template = "Line 1: {{a}}\nLine 2: {{b}}\nLine 3: {{a}}"
        result = render_template(template, {"a": "A", "b": "B"})
        assert result == "Line 1: A\nLine 2: B\nLine 3: A"

    def test_variable_with_dots(self):
        template = "File: {{file.name}}"
        result = render_template(template, {"file.name": "test.yaml"})
        assert result == "File: test.yaml"

    def test_variable_with_hyphens(self):
        template = "ID: {{pr-id}}"
        result = render_template(template, {"pr-id": "001-M1-PR1"})
        assert result == "ID: 001-M1-PR1"

    def test_empty_value(self):
        template = "Value: [{{x}}]"
        result = render_template(template, {"x": ""})
        assert result == "Value: []"

    def test_value_with_special_chars(self):
        template = "Path: {{path}}"
        result = render_template(template, {"path": ".planning/plans/001.yaml"})
        assert result == "Path: .planning/plans/001.yaml"

    def test_realistic_prompt(self):
        template = (
            "You are implementing PR: {{pr_id}} — \"{{pr_title}}\"\n"
            "Plan file: {{plan_file}}\n"
            "Milestone: {{milestone_id}}\n"
        )
        result = render_template(template, {
            "pr_id": "001-M1-PR2",
            "pr_title": "Cell reveal logic",
            "plan_file": ".planning/plans/001.yaml",
            "milestone_id": "001-M1",
        })
        assert "001-M1-PR2" in result
        assert "Cell reveal logic" in result
        assert ".planning/plans/001.yaml" in result
