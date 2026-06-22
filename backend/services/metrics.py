# backend/services/metrics.py

import time


class Metrics:

    def __init__(self):

        self.total_start = None

        self.stt_start = None
        self.stt_end = None

        self.llm_start = None
        self.llm_end = None

        self.tool_start = None
        self.tool_end = None

        self.tts_start = None
        self.tts_end = None

        self.total_end = None

    # ---------------------------------------------------
    # Total
    # ---------------------------------------------------

    def start_total(self):

        self.total_start = time.time()

    def end_total(self):

        self.total_end = time.time()

    def total_latency(self):

        if self.total_start and self.total_end:

            return round(
                self.total_end - self.total_start,
                3
            )

        return None

    # ---------------------------------------------------
    # Speech-to-Text
    # ---------------------------------------------------

    def start_stt(self):

        self.stt_start = time.time()

    def end_stt(self):

        self.stt_end = time.time()

    def stt_latency(self):

        if self.stt_start and self.stt_end:

            return round(
                self.stt_end - self.stt_start,
                3
            )

        return None

    # ---------------------------------------------------
    # LLM
    # ---------------------------------------------------

    def start_llm(self):

        self.llm_start = time.time()

    def end_llm(self):

        self.llm_end = time.time()

    def llm_latency(self):

        if self.llm_start and self.llm_end:

            return round(
                self.llm_end - self.llm_start,
                3
            )

        return None

    # ---------------------------------------------------
    # Tool
    # ---------------------------------------------------

    def start_tool(self):

        self.tool_start = time.time()

    def end_tool(self):

        self.tool_end = time.time()

    def tool_latency(self):

        if self.tool_start and self.tool_end:

            return round(
                self.tool_end - self.tool_start,
                3
            )

        return None

    # ---------------------------------------------------
    # TTS
    # ---------------------------------------------------

    def start_tts(self):

        self.tts_start = time.time()

    def end_tts(self):

        self.tts_end = time.time()

    def tts_latency(self):

        if self.tts_start and self.tts_end:

            return round(
                self.tts_end - self.tts_start,
                3
            )

        return None

    # ---------------------------------------------------
    # Export
    # ---------------------------------------------------

    def to_dict(self):

        return {

            "stt_latency":
                self.stt_latency(),

            "llm_latency":
                self.llm_latency(),

            "tool_latency":
                self.tool_latency(),

            "tts_latency":
                self.tts_latency(),

            "total_latency":
                self.total_latency()
        }