class ChatWithVidException(Exception):
    """Base exception class for Chat with Vid application."""

    pass


class InvalidURLException(ChatWithVidException):
    """Exception raised for invalid URLs."""

    def __init__(self, message: str = "Invalid URL provided"):
        self.message = message
        super().__init__(self.message)
