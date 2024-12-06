"""Audio file handler implementation"""

from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf
from pydub import AudioSegment

from ..exceptions import FileError
from ..types import AudioInfo, FileContent, FileMetadata
from .base import BaseHandler


class AudioHandler(BaseHandler):
    """Handler for audio files"""

    async def read(self, path: Path) -> FileContent:
        """Read audio file"""
        try:
            metadata = await self._get_metadata(path)
            data, sample_rate = sf.read(str(path))

            # Extract audio info
            info = AudioInfo(
                duration=len(data) / sample_rate,
                sample_rate=sample_rate,
                channels=data.shape[1] if len(data.shape) > 1 else 1,
                format=path.suffix[1:],  # Remove dot from extension
                metadata=metadata.metadata,
            )

            return FileContent(content=data, metadata={"info": info}, format="audio")
        except Exception as e:
            raise FileError(f"Failed to read audio file: {e!s}", cause=e)

    async def write(
        self,
        path: Path,
        content: np.ndarray,
        metadata: dict[str, Any] | None = None,
        sample_rate: int = 44100,
    ) -> FileMetadata:
        """Write audio file"""
        try:
            sf.write(str(path), content, sample_rate)
            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write audio file: {e!s}", cause=e)

    def concatenate(self, segments: list[np.ndarray], crossfade: int = 100) -> np.ndarray:
        """
        Concatenate audio segments with optional crossfade

        Args:
            segments: List of audio segments
            crossfade: Crossfade duration in milliseconds

        Returns:
            np.ndarray: Concatenated audio

        """
        if not segments:
            return np.array([])

        if len(segments) == 1:
            return segments[0]

        result = segments[0]
        for segment in segments[1:]:
            if crossfade > 0:
                # Convert crossfade from ms to samples
                xf_samples = int(crossfade * 44.1)  # Assuming 44.1kHz
                result = np.concatenate(
                    (
                        result[:-xf_samples],
                        result[-xf_samples:] * np.linspace(1, 0, xf_samples)
                        + segment[:xf_samples] * np.linspace(0, 1, xf_samples),
                        segment[xf_samples:],
                    ),
                )
            else:
                result = np.concatenate((result, segment))

        return result

    def apply_effects(
        self, audio: np.ndarray | AudioSegment, effects: dict[str, Any],
    ) -> np.ndarray | AudioSegment:
        """
        Apply audio effects

        Args:
            audio: Audio data
            effects: Dictionary of effects to apply

        Returns:
            Union[np.ndarray, AudioSegment]: Processed audio

        """
        result = audio

        if isinstance(result, np.ndarray):
            # NumPy array effects
            if effects.get("normalize", False):
                result = result / np.max(np.abs(result))

            if "fade_in" in effects or "fade_out" in effects:
                fade_in = effects.get("fade_in", 0)
                fade_out = effects.get("fade_out", 0)
                samples = len(result)

                if fade_in:
                    fade_in_samples = int(fade_in * 44.1)  # Assuming 44.1kHz
                    result[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)

                if fade_out:
                    fade_out_samples = int(fade_out * 44.1)
                    result[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)

            if "speed" in effects:
                speed = float(effects["speed"])
                if speed != 1.0:
                    samples = len(result)
                    result = np.interp(
                        np.linspace(0, samples, int(samples / speed)),
                        np.arange(samples),
                        result,
                    )

            if effects.get("reverse", False):
                result = np.flip(result)

        else:
            # pydub AudioSegment effects
            segment: AudioSegment = result

            if effects.get("normalize", False):
                # Implementação manual da normalização para AudioSegment
                peak_amplitude = segment.max
                if peak_amplitude > 0:
                    segment = segment.apply_gain(-peak_amplitude)

            if "fade_in" in effects:
                segment = segment.fade_in(int(effects["fade_in"] * 1000))

            if "fade_out" in effects:
                segment = segment.fade_out(int(effects["fade_out"] * 1000))

            if "speed" in effects:
                speed = float(effects["speed"])
                if speed != 1.0:
                    segment = segment._spawn(
                        segment.raw_data, overrides={"frame_rate": int(segment.frame_rate * speed)},
                    )

            if effects.get("reverse", False):
                segment = segment.reverse()

            result = segment

        return result
