
class MessageReceive:
    def __init__(self, id, timestamp, content):
        self.id = id
        self.timestamp = timestamp
        self.content = content

    def __repr__(self):
        return f"ProcessedMessage(id={self.id}, timestamp={self.timestamp}, content={self.content})"


class AgentStatusRequest:
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        return f"AgentStatusRequest(code={self.code})"
