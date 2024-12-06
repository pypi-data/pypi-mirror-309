"""File optimizer implementation"""

from pathlib import Path

import cv2
from PIL import Image
from pydub import AudioSegment

from ..exceptions import FileError
from .base import BaseHandler


class FileOptimizer(BaseHandler):
    """Handler for optimizing files"""

    async def optimize_image(
        self,
        path: Path,
        output_path: Path,
        quality: int = 85,
        max_size: tuple[int, int] | None = None,
    ) -> None:
        """Optimize image file"""
        try:
            # Open image with PIL
            img = Image.open(path)

            # Resize if max_size specified
            if max_size:
                img.thumbnail(max_size)

            # Save with optimized quality
            img.save(output_path, quality=quality, optimize=True)

        except Exception as e:
            raise FileError(f"Failed to optimize image: {e!s}", cause=e)

    async def optimize_video(
        self,
        path: Path,
        output_path: Path,
        target_size_mb: float = 8.0,
        fps: float | None = None,
        resolution: tuple[int, int] | None = None,
    ) -> None:
        """Optimize video file"""
        try:
            # Open video
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened():
                raise FileError("Failed to open video file")

            # Get video properties
            orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            orig_fps = cap.get(cv2.CAP_PROP_FPS)

            # Calculate output parameters
            out_fps = fps if fps else orig_fps
            if resolution:
                out_width, out_height = resolution
            else:
                out_width, out_height = orig_width, orig_height

            # Create video writer using integer fourcc code
            fourcc = int(cv2.CAP_PROP_FOURCC)
            out = cv2.VideoWriter(str(output_path), fourcc, out_fps, (out_width, out_height))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if resolution:
                    frame = cv2.resize(frame, (out_width, out_height))

                out.write(frame)

            cap.release()
            out.release()

        except Exception as e:
            raise FileError(f"Failed to optimize video: {e!s}", cause=e)

    async def optimize_audio(
        self, path: Path, output_path: Path, bitrate: str = "128k", normalize_volume: bool = False,
    ) -> None:
        """Optimize audio file"""
        try:
            # Load audio
            audio = AudioSegment.from_file(path)

            # Apply volume normalization if requested
            if normalize_volume:
                # Calculate normalization parameters
                max_possible = 32767  # Max possible amplitude for 16-bit audio
                peak_amplitude = max(
                    abs(min(audio.get_array_of_samples())), abs(max(audio.get_array_of_samples())),
                )

                if peak_amplitude > 0:
                    normalize_ratio = float(max_possible) / peak_amplitude
                    audio = audio.apply_gain(normalize_ratio)

            # Export with specified bitrate
            audio.export(
                output_path, format=output_path.suffix.lstrip("."), parameters=["-b:a", bitrate],
            )

        except Exception as e:
            raise FileError(f"Failed to optimize audio: {e!s}", cause=e)
