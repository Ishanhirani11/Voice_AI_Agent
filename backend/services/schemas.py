from pydantic import BaseModel


class AgentResponse(BaseModel):

    intent: str | None = None

    name: str | None = None
    phone: str | None = None

    date: str | None = None
    time: str | None = None

    old_date: str | None = None
    old_time: str | None = None

    new_date: str | None = None
    new_time: str | None = None

    response: str | None = None


class ToolResult(BaseModel):

    success: bool

    message: str