"""Media file handler implementation"""

import io
from pathlib import Path

import cv2
import moviepy.editor as mp
import numpy as np
from PIL import Image, ImageFilter
from pydub import AudioSegment

from ..exceptions import FileError
from ..types import MediaInfo
from .base import BaseHandler


class MediaHandler(BaseHandler):
    """Handler for image, video and audio files"""

    SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    SUPPORTED_VIDEO_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    SUPPORTED_AUDIO_FORMATS = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

    async def read_image(self, path: Path) -> Image.Image:
        """Read image file"""
        try:
            return Image.open(path)
        except Exception as e:
            raise FileError(f"Failed to read image: {e!s}", cause=e)

    async def read_video(self, path: Path) -> cv2.VideoCapture:
        """Read video file"""
        try:
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened():
                raise FileError("Failed to open video file")
            return cap
        except Exception as e:
            raise FileError(f"Failed to read video: {e!s}", cause=e)

    async def read_audio(self, path: Path) -> AudioSegment:
        """Read audio file"""
        try:
            return AudioSegment.from_file(path)
        except Exception as e:
            raise FileError(f"Failed to read audio: {e!s}", cause=e)

    async def get_media_info(self, path: Path) -> MediaInfo:
        """Get media file information"""
        try:
            suffix = path.suffix.lower()

            if suffix in self.SUPPORTED_IMAGE_FORMATS:
                img = await self.read_image(path)
                return MediaInfo(
                    type="image",
                    width=img.width,
                    height=img.height,
                    format=img.format,
                    mode=img.mode,
                    channels=len(img.getbands()),
                )

            if suffix in self.SUPPORTED_VIDEO_FORMATS:
                cap = await self.read_video(path)
                return MediaInfo(
                    type="video",
                    width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    duration=float(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)),
                    fps=cap.get(cv2.CAP_PROP_FPS),
                    total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                )

            if suffix in self.SUPPORTED_AUDIO_FORMATS:
                audio = await self.read_audio(path)
                return MediaInfo(
                    type="audio",
                    duration=len(audio) / 1000.0,
                    channels=audio.channels,
                    sample_width=audio.sample_width,
                    frame_rate=audio.frame_rate,
                )

            raise FileError(f"Unsupported media format: {suffix}")

        except Exception as e:
            raise FileError(f"Failed to get media info: {e!s}", cause=e)

    # Image Operations
    async def resize_image(
        self, image: Image.Image, size: tuple[int, int], keep_aspect: bool = True,
    ) -> Image.Image:
        """Resize image"""
        try:
            if keep_aspect:
                image.thumbnail(size)
                return image
            return image.resize(size)
        except Exception as e:
            raise FileError(f"Failed to resize image: {e!s}", cause=e)

    async def convert_image(self, image: Image.Image, format: str, **kwargs) -> bytes:
        """Convert image format"""
        try:
            output = io.BytesIO()
            image.save(output, format=format, **kwargs)
            return output.getvalue()
        except Exception as e:
            raise FileError(f"Failed to convert image: {e!s}", cause=e)

    async def apply_filter(self, image: Image.Image, filter_name: str, **params) -> Image.Image:
        """Apply image filter"""
        try:
            if filter_name == "blur":
                return image.filter(ImageFilter.GaussianBlur(params.get("radius", 2)))
            if filter_name == "sharpen":
                return image.filter(ImageFilter.SHARPEN)
            if filter_name == "grayscale":
                return image.convert("L")
            raise FileError(f"Unknown filter: {filter_name}")
        except Exception as e:
            raise FileError(f"Failed to apply filter: {e!s}", cause=e)

    # Video Operations
    async def extract_frames(
        self,
        video: cv2.VideoCapture,
        start_time: float = 0,
        end_time: float | None = None,
        interval: float = 1.0,
    ) -> list[np.ndarray]:
        """Extract frames from video"""
        try:
            frames = []
            fps = video.get(cv2.CAP_PROP_FPS)
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

            start_frame = int(start_time * fps)
            end_frame = int(end_time * fps) if end_time else total_frames
            interval_frames = int(interval * fps)

            video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            current_frame = start_frame
            while current_frame < end_frame:
                ret, frame = video.read()
                if ret:
                    frames.append(frame)
                current_frame += interval_frames
                video.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

            return frames
        except Exception as e:
            raise FileError(f"Failed to extract frames: {e!s}", cause=e)

    async def create_video(
        self, frames: list[np.ndarray], output_path: Path, fps: float = 30.0, codec: str = "mp4v",
    ) -> None:
        """Create video from frames"""
        try:
            if not frames:
                raise FileError("No frames provided")

            height, width = frames[0].shape[:2]
            fourcc = int(cv2.CAP_PROP_FOURCC)

            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

            for frame in frames:
                out.write(frame)

            out.release()

        except Exception as e:
            raise FileError(f"Failed to create video: {e!s}", cause=e)

    # Audio Operations
    async def trim_audio(
        self, audio: AudioSegment, start_ms: int, end_ms: int | None = None,
    ) -> AudioSegment:
        """Trim audio segment"""
        try:
            # First get the slice of audio data
            if end_ms is not None:
                # For a specific end time, slice both start and end
                slice_data = audio[start_ms:end_ms]
            else:
                # For no end time, slice from start to the end
                slice_data = audio[start_ms:]

            # Ensure we're working with an AudioSegment
            if not isinstance(slice_data, AudioSegment):
                raise FileError("Failed to slice audio segment")

            return slice_data

        except Exception as e:
            raise FileError(f"Failed to trim audio: {e!s}", cause=e)

    async def adjust_audio(
        self, audio: AudioSegment, volume_db: float = 0, speed: float = 1.0, normalize: bool = False,
    ) -> AudioSegment:
        """Adjust audio properties"""
        try:
            result = audio

            if volume_db != 0:
                result = result + volume_db

            if speed != 1.0:
                result = result._spawn(
                    result.raw_data, overrides={"frame_rate": int(result.frame_rate * speed)},
                )

            if normalize:
                max_possible = 32767  # Max possible amplitude for 16-bit audio
                peak_amplitude = max(
                    abs(min(result.get_array_of_samples())), abs(max(result.get_array_of_samples())),
                )

                if peak_amplitude > 0:
                    normalize_ratio = float(max_possible) / peak_amplitude
                    result = result.apply_gain(normalize_ratio)

            return result

        except Exception as e:
            raise FileError(f"Failed to adjust audio: {e!s}", cause=e)

    async def mix_audio(
        self, segments: list[AudioSegment], crossfade_ms: int = 100,
    ) -> AudioSegment:
        """Mix multiple audio segments"""
        try:
            if not segments:
                raise FileError("No audio segments provided")

            result = segments[0]
            for segment in segments[1:]:
                result = result.append(segment, crossfade=crossfade_ms)

            return result

        except Exception as e:
            raise FileError(f"Failed to mix audio: {e!s}", cause=e)

    async def extract_audio(self, video_path: Path, output_path: Path) -> None:
        """Extract audio from video"""
        try:
            video = mp.VideoFileClip(str(video_path))
            if video.audio is None:
                raise FileError("Video has no audio track")

            video.audio.write_audiofile(str(output_path))
            video.close()

        except Exception as e:
            raise FileError(f"Failed to extract audio: {e!s}", cause=e)

    async def add_audio_to_video(
        self, video_path: Path, audio_path: Path, output_path: Path,
    ) -> None:
        """Add audio track to video"""
        try:
            video = mp.VideoFileClip(str(video_path))
            audio = mp.AudioFileClip(str(audio_path))

            final_video = video.set_audio(audio)
            final_video.write_videofile(str(output_path))

            video.close()
            audio.close()

        except Exception as e:
            raise FileError(f"Failed to add audio to video: {e!s}", cause=e)
