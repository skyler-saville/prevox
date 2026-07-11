"""Print the first completely manual Prevox pipeline."""

from prevox.manual_example import build_manual_trace


def main() -> None:
    print(build_manual_trace().format())


if __name__ == "__main__":
    main()
