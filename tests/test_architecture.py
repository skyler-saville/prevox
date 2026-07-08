import ast
from dataclasses import is_dataclass
from pathlib import Path
import unittest

from prevox import domain


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src" / "prevox"
DOMAIN_ROOT = SOURCE_ROOT / "domain"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


class ArchitectureTests(unittest.TestCase):
    def test_domain_layer_does_not_import_outer_layers(self) -> None:
        forbidden_prefixes = (
            "prevox.analysis",
            "prevox.diagnostics",
            "prevox.inspection",
            "prevox.manual_example",
            "prevox.transforms",
            "prevox.export",
            "prevox.infrastructure",
            "prevox.cli",
        )

        violations = {
            str(path.relative_to(PROJECT_ROOT)): sorted(
                module
                for module in imported_modules(path)
                if module.startswith(forbidden_prefixes)
            )
            for path in DOMAIN_ROOT.glob("*.py")
        }
        violations = {
            path: modules for path, modules in violations.items() if modules
        }

        self.assertEqual(violations, {})

    def test_rendering_terms_do_not_become_music_ir_fields(self) -> None:
        forbidden_fields = {
            "articulation",
            "cc",
            "channel",
            "instrument",
            "midi_channel",
            "patch",
            "pedal",
            "plugin",
            "program",
            "track",
            "velocity",
        }
        music_ir_types = (
            domain.Note,
            domain.Motif,
            domain.Phrase,
            domain.Voice,
            domain.Section,
            domain.Song,
            domain.MusicIR,
            domain.RealizedNote,
        )

        violations = {
            value_type.__name__: sorted(
                forbidden_fields.intersection(value_type.__annotations__)
            )
            for value_type in music_ir_types
        }
        violations = {
            type_name: fields
            for type_name, fields in violations.items()
            if fields
        }

        self.assertEqual(violations, {})

    def test_core_domain_values_remain_frozen_dataclasses(self) -> None:
        core_values = (
            domain.IntentTarget,
            domain.Intent,
            domain.PredictedEffect,
            domain.ProposalRationale,
            domain.Proposal,
            domain.Measurement,
            domain.Critique,
            domain.AcceptanceDecision,
            domain.PitchClass,
            domain.Pitch,
            domain.TonalContext,
            domain.Note,
            domain.Placement,
            domain.Motif,
            domain.Phrase,
            domain.Voice,
            domain.Section,
            domain.Song,
            domain.RealizedNote,
            domain.MusicIR,
            domain.CompositionState,
        )

        mutable = [
            value_type.__name__
            for value_type in core_values
            if not is_dataclass(value_type)
            or not value_type.__dataclass_params__.frozen
        ]

        self.assertEqual(mutable, [])

    def test_analysis_and_transform_layers_do_not_import_renderers(self) -> None:
        forbidden_prefixes = (
            "prevox.export",
            "prevox.infrastructure",
            "prevox.cli",
        )
        checked_paths = [
            SOURCE_ROOT / "analysis.py",
            *(SOURCE_ROOT / "transforms").glob("*.py"),
        ]
        violations = {
            str(path.relative_to(PROJECT_ROOT)): sorted(
                module
                for module in imported_modules(path)
                if module.startswith(forbidden_prefixes)
            )
            for path in checked_paths
        }
        violations = {
            path: modules for path, modules in violations.items() if modules
        }

        self.assertEqual(violations, {})


if __name__ == "__main__":
    unittest.main()
