from enum import IntFlag

from PySide6.QtCore import QUrl


class Url(QUrl):
    class FormattingOptions(IntFlag):
        None_ = 0x0
        RemoveScheme = 0x1
        RemovePassword = 0x2
        RemoveUserInfo = RemovePassword | 0x4
        RemovePort = 0x8
        RemoveAuthority = RemoveUserInfo | RemovePort | 0x10
        RemovePath = 0x20
        RemoveQuery = 0x40
        RemoveFragment = 0x80
        RemoveFilename = 0x800
        PreferLocalFile = 0x200
        StripTrailingSlash = 0x400
        NormalizePathSegments = 0x1000
