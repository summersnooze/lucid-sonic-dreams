"""Command-line helper to render a Lucid Sonic Dreams video.

This script wraps ``LucidSonicDream`` so you can point it at a song and
quickly generate a synced video without writing your own Python snippet.
Only the most common options are exposed here; for full control refer to
``LucidSonicDream.hallucinate`` in ``lucidsonicdreams.main``.
"""

import argparse
from pathlib import Path

from lucidsonicdreams import LucidSonicDream


def positive_float(value: str) -> float:
    float_val = float(value)
    if float_val <= 0:
        raise argparse.ArgumentTypeError("Value must be positive")
    return float_val


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a Lucid Sonic Dreams video from an audio file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--song",
        required=True,
        help="Path to the input audio file (e.g., mp3, wav).",
    )
    parser.add_argument(
        "--style",
        default="abstract photos",
        help=(
            "Name of a bundled style (call show_styles() for the list) or a"
            " local .pkl weight file."
        ),
    )
    parser.add_argument(
        "--output",
        default="lucid-sonic-dreams.mp4",
        help="Output video filename (mp4).",
    )
    parser.add_argument(
        "--start",
        type=float,
        default=0.0,
        help="Start time within the song, in seconds.",
    )
    parser.add_argument(
        "--duration",
        type=positive_float,
        default=None,
        help="How many seconds of audio to render. Defaults to full track.",
    )
    parser.add_argument(
        "--fps",
        type=positive_float,
        default=43,
        help="Frames per second for the video.",
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=None,
        help="Square output resolution (e.g., 512 for 512x512).",
    )
    parser.add_argument(
        "--speed-fpm",
        type=positive_float,
        default=12,
        help="Speed factor in frames per minute.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="Number of frames to generate in parallel.",
    )
    parser.add_argument(
        "--truncation",
        type=float,
        default=1.0,
        help="Truncation psi value for StyleGAN2 sampling (0-1).",
    )
    parser.add_argument(
        "--motion-randomness",
        type=float,
        default=0.5,
        help="Randomness applied to camera motion (0-1).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    song_path = Path(args.song)

    if not song_path.exists():
        raise SystemExit(f"Audio file not found: {song_path}")

    dreamer = LucidSonicDream(song=str(song_path), style=args.style)
    dreamer.hallucinate(
        file_name=args.output,
        fps=int(args.fps),
        resolution=args.resolution,
        start=args.start,
        duration=args.duration,
        speed_fpm=int(args.speed_fpm),
        batch_size=args.batch_size,
        motion_randomness=args.motion_randomness,
        truncation=args.truncation,
    )


if __name__ == "__main__":
    main()
