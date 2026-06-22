# backend/services/exceptions.py


class AgentException(Exception):
    """
    Base exception for agent errors.
    """
    pass


class MemoryException(Exception):
    """
    Memory-related errors.
    """
    pass


class ToolException(Exception):
    """
    Tool execution errors.
    """
    pass


class LLMException(Exception):
    """
    LLM-related errors.
    """
    pass


class SpeechToTextException(Exception):
    """
    STT-related errors.
    """
    pass


class TextToSpeechException(Exception):
    """
    TTS-related errors.
    """
    pass


class AvatarException(Exception):
    """
    Avatar-related errors.
    """
    pass