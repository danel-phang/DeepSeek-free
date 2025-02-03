class DeepSeekErrors(Exception):
    """Base class for exceptions in DeepSeek."""

class FileNotFoundError(DeepSeekErrors):
    """Exception raised for errors in the input file not found."""

    def __init__(self, message="File not found"):
        self.message = message
        super().__init__(self.message)

class InvalidFormatError(DeepSeekErrors):
    """Exception raised for errors in the input file format."""

    def __init__(self, message="Invalid file format"):
        self.message = message
        super().__init__(self.message)

class ProcessingError(DeepSeekErrors):
    """Exception raised for errors during processing."""

    def __init__(self, message="Error during processing"):
        self.message = message
        super().__init__(self.message)