import ctypes

from ctypes import wintypes

enumWindows = ctypes.windll.user32.EnumWindows
enumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int)
)
getWindowText = ctypes.windll.user32.GetWindowTextW
getWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
isWindowVisible = ctypes.windll.user32.IsWindowVisible


def getWindowHandleByTitle(title):
    """A nice wrapper for FindWindow()."""
    return ctypes.windll.user32.FindWindowW(None, title)


class RECT(ctypes.Structure):
    """A nice wrapper of the RECT structure.

    Microsoft Documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/dd162897(v=vs.85).aspx
    """

    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def getAllTitles():
    # This code taken from https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/
    # A correction to this code (for enumWindowsProc) is here: http://makble.com/the-story-of-lpclong
    titles = []

    def foreach_window(hWnd, lParam):
        if isWindowVisible(hWnd):
            length = getWindowTextLength(hWnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            getWindowText(hWnd, buff, length + 1)
            titles.append(buff.value)
        return True

    enumWindows(enumWindowsProc(foreach_window), 0)

    return titles


def getWindowGeometry(title):
    """A nice wrapper for GetWindowRect(). TODO

    Syntax:
    BOOL GetWindowRect(
      HWND   hWnd,
      LPRECT lpRect
    );

    Microsoft Documentation:
    https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-getwindowrect
    """
    hWnd = getWindowHandleByTitle(title)
    rect = RECT()
    result = ctypes.windll.user32.GetWindowRect(hWnd, ctypes.byref(rect))
    if result != 0:
        return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
    else:
        return None


def screensize():
    """Returns the width and height of the screen as a two-integer tuple.

    Returns:
      (width, height) tuple of the screen size, in pixels.
    """
    return (
        ctypes.windll.user32.GetSystemMetrics(0),
        ctypes.windll.user32.GetSystemMetrics(1),
    )
