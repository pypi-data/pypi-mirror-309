from enum import IntEnum

from PySide6.QtGui import QTextDocument


class TextDocument:
    class ResourceType(IntEnum):
        Unknown = QTextDocument.ResourceType.UnknownResource
        Html = QTextDocument.ResourceType.HtmlResource
        Image = QTextDocument.ResourceType.ImageResource
        StyleSheet = QTextDocument.ResourceType.StyleSheetResource
        Markdown = QTextDocument.ResourceType.MarkdownResource
        User = QTextDocument.ResourceType.UserResource
