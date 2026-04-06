import pytest

from detect_ticket import extract_ticket_info, get_changed_tickets


class TestGetChangedTickets:
    def test_parses_diff_output(self):
        diff = ".planning/tickets/001-basic-minesweeper.yaml\n.planning/tickets/002-advanced.yaml\n"
        result = get_changed_tickets(diff)
        assert result == [
            ".planning/tickets/001-basic-minesweeper.yaml",
            ".planning/tickets/002-advanced.yaml",
        ]

    def test_empty_diff(self):
        assert get_changed_tickets("") == []

    def test_whitespace_only_diff(self):
        assert get_changed_tickets("  \n  \n") == []

    def test_strips_whitespace(self):
        diff = "  .planning/tickets/001.yaml  \n"
        assert get_changed_tickets(diff) == [".planning/tickets/001.yaml"]


class TestExtractTicketInfo:
    def test_extracts_numeric_id(self):
        files = [".planning/tickets/001-basic-minesweeper-web.yaml"]
        ticket_id, ticket_file = extract_ticket_info(files)
        assert ticket_id == "001"
        assert ticket_file == ".planning/tickets/001-basic-minesweeper-web.yaml"

    def test_extracts_longer_id(self):
        files = [".planning/tickets/1234-something.yaml"]
        ticket_id, _ = extract_ticket_info(files)
        assert ticket_id == "1234"

    def test_uses_first_file(self):
        files = [
            ".planning/tickets/001-first.yaml",
            ".planning/tickets/002-second.yaml",
        ]
        ticket_id, ticket_file = extract_ticket_info(files)
        assert ticket_id == "001"
        assert ticket_file == ".planning/tickets/001-first.yaml"

    def test_empty_list(self):
        ticket_id, ticket_file = extract_ticket_info([])
        assert ticket_id == ""
        assert ticket_file == ""

    def test_non_numeric_filename(self):
        files = [".planning/tickets/no-number.yaml"]
        ticket_id, ticket_file = extract_ticket_info(files)
        assert ticket_id == ""
        assert ticket_file == ".planning/tickets/no-number.yaml"

    def test_yml_extension(self):
        files = [".planning/tickets/005-feature.yml"]
        ticket_id, _ = extract_ticket_info(files)
        assert ticket_id == "005"
