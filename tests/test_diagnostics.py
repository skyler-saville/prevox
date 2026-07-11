import unittest

from prevox.diagnostics import (
    Diagnostic,
    DiagnosticLocation,
    DiagnosticReport,
    DiagnosticSeverity,
)
from prevox.inspection import format_diagnostic_report


class DiagnosticTests(unittest.TestCase):
    def test_report_distinguishes_blocking_errors_from_notes(self) -> None:
        report = DiagnosticReport(
            (
                Diagnostic(
                    code="example.note",
                    severity=DiagnosticSeverity.INFO,
                    message="kept motif unchanged",
                ),
                Diagnostic(
                    code="example.error",
                    severity=DiagnosticSeverity.ERROR,
                    message="cannot compile phrase",
                ),
            )
        )

        self.assertTrue(report.has_errors)
        self.assertFalse(report.is_success)
        self.assertEqual(len(report.errors), 1)

    def test_location_formats_as_domain_path(self) -> None:
        location = DiagnosticLocation(
            (
                "Song 'Manual Trace'",
                "Section 'verse-a'",
                "Motif 'motif-a'",
            )
        )

        self.assertEqual(
            str(location),
            "Song 'Manual Trace' → Section 'verse-a' → Motif 'motif-a'",
        )

    def test_diagnostic_report_has_canonical_readable_output(self) -> None:
        report = DiagnosticReport(
            (
                Diagnostic(
                    code="transform.invalid_diminution_divisor",
                    severity=DiagnosticSeverity.ERROR,
                    message="cannot diminish by 0",
                    location=DiagnosticLocation(("Motif 'verse-a'",)),
                    expected=("divisor is greater than one",),
                    notes=("diminution preserves exact rational time",),
                ),
            )
        )

        rendered = format_diagnostic_report(report)

        self.assertIn(
            "ERROR transform.invalid_diminution_divisor: "
            "cannot diminish by 0",
            rendered,
        )
        self.assertIn("Location: Motif 'verse-a'", rendered)
        self.assertIn("Expected: divisor is greater than one", rendered)
        self.assertIn(
            "Note: diminution preserves exact rational time",
            rendered,
        )


if __name__ == "__main__":
    unittest.main()
