"""Export the manual architecture trace to a local MIDI preview file."""

from pathlib import Path

from prevox.export.midi import MidiRenderer
from prevox.manual_example import build_manual_trace


def main() -> None:
    music = build_manual_trace().state.music
    if music is None:
        raise RuntimeError("manual trace did not produce accepted MusicIR")

    target = Path("artifacts/midi/manual_trace.mid")
    MidiRenderer().write(music, target)
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
