import Quartz


def getWindowGeometry(title):
    # TEMP - this is not a real api, I'm just using this name to store these notes for now.
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements
        | Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID,
    )
    for win in windows:
        if title in "%s %s" % (
            win[Quartz.kCGWindowOwnerName],
            win.get(Quartz.kCGWindowName, ""),
        ):
            w = win["kCGWindowBounds"]
            return (w["X"], w["Y"], w["Width"], w["Height"])


def screensize():
    return (
        Quartz.CGDisplayPixelsWide(Quartz.CGMainDisplayID()),
        Quartz.CGDisplayPixelsHigh(Quartz.CGMainDisplayID()),
    )


def getAllTitles():
    """Returns a list of strings of window titles for all visible windows."""

    # Source: https://stackoverflow.com/questions/53237278/obtain-list-of-all-window-titles-on-macos-from-a-python-script/53985082#53985082
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements
        | Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID,
    )
    return [
        "%s %s" % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, ""))
        for win in windows
    ]
