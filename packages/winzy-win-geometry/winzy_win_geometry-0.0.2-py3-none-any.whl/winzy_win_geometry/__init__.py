import winzy
import platform

import sys

if sys.platform.startswith("win"):
    from winzy_win_geometry._wingetsize import (
        screensize,
        getWindowGeometry,
        getAllTitles,
    )
else:
    from winzy_win_geometry._macosgetsize import (
        screensize,
        getWindowGeometry,
        getAllTitles,
    )


def get_window_geometry_percentage(window_title=None):
    """
    Returns the geometry of a specified window or the active window as a percentage of the screen size.

    Args:
        - window_title (str, optional): Title of the window to get geometry. If None, uses the active window.

    Returns:
        - dict: A dictionary with the window geometry in percentage {'width': xx, 'height': xx, 'x': xx, 'y': xx}.
    """
    os_type = platform.system()
    if os_type not in ["Windows", "Darwin"]:
        print("This function supports only Windows and macOS.")
        return None

    try:
        screen_width, screen_height = screensize()

        # Fetch the list of windows and filter by title
        if window_title:
            window = None
            for w in getAllTitles():
                if window_title in w:
                    window = getWindowGeometry(w)
                    break
            if not window:
                print(f"No window found with title containing '{window_title}'")
                return None
        else:
            # List all window titles and ask user to select one
            window_titles = getAllTitles()
            print("Available windows:")
            for i, title in enumerate(window_titles):
                print(f"{i+1}. {title}")
            choice = input("Enter the number of the window: ")
            try:
                choice = int(choice) - 1
                if choice < 0 or choice >= len(window_titles):
                    print("Invalid choice.")
                    return None
                window_title = window_titles[choice]
                window = getWindowGeometry(window_title)
            except ValueError:
                print("Invalid input.")
                return None

        # Get window geometry
        win_x, win_y, win_width, win_height = window

        # Calculate as a percentage of screen size
        width = round((win_width / screen_width) * 100, 2)
        height = round((win_height / screen_height) * 100, 2)
        left = round((win_x / screen_width) * 100, 2)
        top = round((win_y / screen_height) * 100, 2)

        geometry = {"width": width, "height": height, "x": left, "y": top}
        # print("Window geometry:")
        # for key, value in geometry.items():
        #     print(f"{key}: {value}%")
        print(f"{left} {top} {width} {height}")
        return geometry
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def create_parser(subparser):
    parser = subparser.add_parser(
        "wingeo", description="Get window geometry as a percentage of screen size."
    )
    # Add subprser arguments here.
    parser.add_argument("-t", "--title", help="Title of the window to get geometry.")
    return parser


class HelloWorld:
    """Get window geometry as a percentage of screen size."""

    __name__ = "wingeo"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.main)

    def main(self, args):
        _ = get_window_geometry_percentage(args.title)

    def hello(self, args):
        # this routine will be called when "winzy wingeo is called."
        print("Hello! This is an example ``winzy`` plugin.")


wingeo_plugin = HelloWorld()
