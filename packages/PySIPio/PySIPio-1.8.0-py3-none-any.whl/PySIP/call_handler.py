import asyncio
import logging

from typing import List, Optional
from pydub import AudioSegment
from scipy.io.wavfile import io
from .filters import CallState
from .audio_stream import AudioStream
from .utils.async_utils import wait_for
from .utils.logger import logger
from .utils import generate_audio
from .exceptions import SIPTransferException


class CallHandler:
    def __init__(self, call) -> None:
        self.call = call
        self.audio_queue: asyncio.Queue = asyncio.Queue()
        self.previous_stream: Optional[AudioStream] = None
        self._voice = "en-US-AriaNeural"

    async def say(self, text: str):
        try:
            _audio_task = asyncio.create_task(
                generate_audio(text, self.voice)
            )
            app_stopped_task = asyncio.create_task(self.call._wait_stopped())

            # Wait for either audio processing task to complete or the application to stop
            done, pending = await asyncio.wait(
                [_audio_task, app_stopped_task], return_when=asyncio.FIRST_COMPLETED
            )

            # If the audio processing task is completed, retrieve the audio bytes
            if _audio_task in done:
                for _t in pending:
                    _t.cancel()
                self.audio_bytes = await _audio_task
                self.audio_stream = AudioStream(self.audio_bytes)
                await asyncio.to_thread(self.audio_stream.recv)
                await self.audio_queue.put(("audio", self.audio_stream))
                if self.call._is_call_stopped:
                    self.audio_stream.stream_done()

                return self.audio_stream

            # If the application stops before audio processing completes
            elif app_stopped_task in done:
                for _t in pending:
                    _t.cancel()
                logger.log(
                    logging.DEBUG,
                    "Call stopped before audio processing completed.",
                )
                raise RuntimeError("Call is no longer ongoing")

            else:
                raise RuntimeError("Unable to generate audio due to unknow error")

        except Exception as e:
            logger.log(logging.ERROR, str(e))
            raise e

    async def play(self, file_name: str, format: str = "wav"):
        """Simple method to play an audio in call"""
        temp_file = io.BytesIO()
        try:
            decoded_chunk: AudioSegment = AudioSegment.from_file(
                file_name, format=format
            )
        except Exception as e:
            raise e
        decoded_chunk = decoded_chunk.set_channels(1)
        decoded_chunk = decoded_chunk.set_frame_rate(8000)
        decoded_chunk.export(temp_file, format="wav")

        self.audio_stream = AudioStream(temp_file)
        await asyncio.to_thread(self.audio_stream.recv)
        await self.audio_queue.put(("audio", self.audio_stream))

        return self.audio_stream

    async def gather(
        self, length: int = 1, timeout: float = 7.0, finish_on_key=None, stream=None
    ):
        """This method gathers a dtmf tone with the specified
        length and then returns when done""" 
        if not self.call.sip_core.is_running.is_set():
            raise RuntimeError("Call is no longer ongoing")

        dtmf_future: asyncio.Future = asyncio.Future()
        dtmf_future.__setattr__("length", length)
        dtmf_future.__setattr__("timeout", timeout)
        dtmf_future.__setattr__("finish_on_key", finish_on_key)
        dtmf_future.__setattr__("stream", stream)
        await self.audio_queue.put(("dtmf", dtmf_future))

        try:
            result = await dtmf_future
            return str(result)
        except asyncio.CancelledError:
            if not dtmf_future.done():
                dtmf_future.cancel()
                try:
                    await dtmf_future
                except asyncio.CancelledError:
                    pass

            _task = asyncio.current_task()
            if (_task is not None) and _task.cancelling() > 0:
                raise

        except RuntimeError as e:
            raise e

        except asyncio.TimeoutError:
            raise

    async def gather_and_say(
        self,
        length: int = 1,
        delay: int = 7,
        loop: int = 3,
        finish_on_key=None,
        loop_msg: str = "",
        delay_msg: str = "",
    ):
        """This method waits for dtmf keys and then if received
        it instantly send it"""
        dtmf_result = None
        for _ in range(loop):
            try:
                dtmf_result = await self.gather(
                    length=length, timeout=delay, finish_on_key=finish_on_key
                )
                if dtmf_result:
                    dtmf_result = dtmf_result
                    return dtmf_result

            except asyncio.TimeoutError:
                text = delay_msg or "You did not press any keys, please try again"
                await self.say(text)
                continue

        text = (
            loop_msg
            or f"You failed to enter the key in {loop} tries. Hanging up the call"
        )
        stream = await self.say(text)
        await stream.wait_finished()

        return dtmf_result

    async def gather_and_play(
        self,
        file_name: str,
        format: str = "wav",
        length: int = 1,
        delay: int = 7,
        loop: int = 3,
        finish_on_key=None,
        loop_audio_file: str = "",
        delay_audio_file: str = "",
    ):
        """This method waits for dtmf keys and then if received
        it instantly send it"""
        dtmf_result = None
        for _ in range(loop):
            try:
                stream = await self.play(file_name, format)
                dtmf_result = await self.gather(
                    length=length,
                    timeout=delay,
                    finish_on_key=finish_on_key,
                    stream=stream,
                )
                if dtmf_result:
                    dtmf_result = dtmf_result
                    return dtmf_result

            except asyncio.TimeoutError:
                if delay_audio_file:
                    await self.play(delay_audio_file, format=format)
                else:
                    await self.say("You did not any keys please try again")
                continue

        if loop_audio_file:
            stream = await self.play(loop_audio_file, format=format)
        else:
            stream = await self.say(
                f"You failed to enter the key in {loop} tries. Hanging up the call"
            )
        await stream.wait_finished()

        return dtmf_result

    async def transfer_to(self, to: str | int):
        """
        Transfer the call that is currently on-going to the specified `to`
        Args:
            to (str|int): The target phone number to transfer the call to.
        """
        self.call._refer_future = asyncio.Future()
        self.refer_message = self.call.refer_generator(to)
        await self.call.sip_core.send(self.refer_message)
        logger.log(logging.DEBUG, f"Trnasfering the call to -> {to}")

        try:
            result = await asyncio.wait_for(self.call._refer_future, 5)
            return (result, None)

        except asyncio.TimeoutError:
            err = SIPTransferException(408, "Request Timeout")
            return (None, err)

        except SIPTransferException as exc:
            return (None, exc)

        except Exception as exc:
            err = SIPTransferException(9999, f"Unknown Error: {exc}")
            return (None, err)

    async def sleep(self, delay: float):
        await self.audio_queue.put(("sleep", delay))

    async def hangup(self):
        await self.call.stop("Caller hanged up")

    @property
    def dtmf_codes(self) -> List[str]:
        """Contains all the dtmf codes from the start of the call."""
        if self.call._dtmf_handler is not None:
            return self.call._dtmf_handler.dtmf_codes

        else:
            return []

    @property
    def call_id(self):
        """Retturns the call id of the current call"""
        return self.call.call_id

    @property
    def dtmf_handler(self):
        """Returns the dtmf handler for this call"""
        return self.call._dtmf_handler

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, value):
        self._voice = value

    async def send_handler(self):
        try:
            logger.log(logging.INFO, "CallHandler has been initialized..")

            while True:
                if not self.call.sip_core.is_running.is_set():
                    break  # Exit the loop if the call is not running

                if self.call.call_state in [CallState.ENDED, CallState.FAILED, CallState.BUSY]:
                    break

                if self.call.call_state is not CallState.ANSWERED:
                    await asyncio.sleep(0.1)
                    continue

                if not self.call._rtp_session:
                    await asyncio.sleep(0.1)
                    continue

                try:
                    event_type, result = await asyncio.wait_for(
                        self.audio_queue.get(), timeout=1.0
                    )

                    if event_type == "audio":
                        if self.previous_stream:
                            await self.previous_stream.wait_finished()

                        self.call._rtp_session.set_audio_stream(result)
                        self.previous_stream = result

                    elif event_type == "sleep":
                        await asyncio.sleep(result)

                    elif event_type == "drain":
                        self.call._rtp_session.set_audio_stream(None)
                        result.is_running.clear()

                    elif event_type == "dtmf":
                        stream = None
                        try:
                            length = result.length
                            timeout = result.timeout
                            finish_on_key = result.finish_on_key
                            stream = result.stream
                            logger.log(logging.INFO, "Started to wait for DTMF")
                            awaitable = None

                            if self.previous_stream:
                                asyncio.create_task(
                                    self.call._dtmf_handler.started_typing(
                                        self.call._rtp_session.set_audio_stream, None
                                    )
                                )
                                awaitable = self.previous_stream.stream_done_future

                            dtmf_task = asyncio.create_task(wait_for(
                                self.call._dtmf_handler.get_dtmf(length, finish_on_key),
                                timeout,
                                awaitable,
                            ))
                            app_stopped_task = asyncio.create_task(self.call._wait_stopped())
                            done, pending = await asyncio.wait(
                                [dtmf_task, app_stopped_task], return_when=asyncio.FIRST_COMPLETED
                            )
                            if dtmf_task in done:
                                app_stopped_task.cancel()
                                dtmf_result = await dtmf_task
                                self.previous_stream = stream
                                if stream:
                                    await self.call._rtp_session.set_audio_stream(None)
                                result.set_result(dtmf_result)

                            elif app_stopped_task in done:
                                dtmf_task.cancel()
                                result.set_exception(
                                    RuntimeError("App stopped before DTMF result.")
                                )

                        except asyncio.TimeoutError:
                            self.previous_stream = stream
                            if stream:
                                await self.call._rtp_session.set_audio_stream(None)
                            result.set_exception(asyncio.TimeoutError)

                except asyncio.TimeoutError:
                    pass

                except asyncio.CancelledError:
                    break

                finally:
                    await asyncio.sleep(0.1)

            while not self.audio_queue.empty():
                event_type, result = await self.audio_queue.get()
                if event_type == "audio":
                    result.stream_done()

                elif event_type == "dtmf":
                    result.set_exception(
                        RuntimeError("App stopped before DTMF result.")
                    )

            if self.previous_stream:
                self.previous_stream.stream_done()
                
            logger.log(logging.DEBUG, "The call handler has been stopped")
        except asyncio.CancelledError:
            logger.log(logging.DEBUG, "The send handler task has been cancelled")
            pass
