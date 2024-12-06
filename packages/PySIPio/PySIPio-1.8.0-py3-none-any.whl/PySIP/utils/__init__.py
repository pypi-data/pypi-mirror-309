import asyncio
import io
import re
from edge_tts import Communicate
from pydub.audio_segment import AudioSegment


def mp3_to_wav(f, target_channels=1, target_framerate=8000):
    """
    Convert MP3 audio from the temporary chunk to WAV format.
    """
    output_chunk = io.BytesIO()
    decoded_chunk = AudioSegment.from_mp3(f)
    decoded_chunk = decoded_chunk.set_channels(target_channels)
    decoded_chunk = decoded_chunk.set_frame_rate(target_framerate)
    decoded_chunk.export(output_chunk, format="wav")
    return output_chunk


async def generate_audio(text: str, voice: str) -> io.BytesIO:
    """
    this genertes the real TTS using edge_tts for this part.
    """
    com = Communicate(text, voice)
    temp_chunk = io.BytesIO()
    async for chunk in com.stream():
        if chunk["type"] == "audio":
            await asyncio.to_thread(temp_chunk.write, chunk["data"])

    await asyncio.to_thread(temp_chunk.seek, 0)
    decoded_audio = await asyncio.to_thread(mp3_to_wav, temp_chunk)
    return decoded_audio


def get_caller_number(invite_message):
    """Extract phone number from SIP INVITE From header
    Returns: phone number as string or None"""

    from_header = invite_message.headers.get("From", "")

    # Look for number pattern after "sip:"
    match = re.search(r"sip:(\+?\d+)@", from_header)
    if match:
        return match.group(1)

    # Alternate: look for number in display name
    match = re.search(r'"(\+?\d+)".*<sip:', from_header)
    if match:
        return match.group(1)

    return None
