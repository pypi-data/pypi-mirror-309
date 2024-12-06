from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from WaldurSA_TUI import (
    configured_offerings,
    dashboard,
    logs,
    error,
    quit,
    detailed_log,
)

"""import configured_offerings
import dashboard
import logs

import quit
import error"""


class WaldurSATUIApp(App):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        ("q", "request_quit", "Quit"),
        ("e", "request_error", "Error Showcase"),
        ("l", "show_detailed_log", "Show detailed log"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="dashboard"):
            with TabPane("Dashboard", id="dashboard"):
                yield dashboard.Dashboard()
            with TabPane("Logs", id="logs"):
                yield logs.Logs()
            with TabPane("Configured offerings", id="configured_offerings"):
                yield configured_offerings.Configured_offerings()

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""

        def check_quit(quit: bool) -> None:
            """Called when QuitScreen is dismissed."""
            if quit:
                self.exit()

        self.push_screen(quit.QuitScreen(), check_quit)

    def action_request_error(self) -> None:
        # show error message
        self.app.push_screen(
            error.ErrorPopup("An unexpected error occurred!", "Test error")
        )

    def action_show_detailed_log(self) -> None:
        # show detailed log
        self.app.push_screen(
            detailed_log.DetailedLogPopUp(
                "2021-09-01 12:00:00", "INFO", "This is a detailed log message."
            )
        )


def main():
    app = WaldurSATUIApp()
    app.run()


if __name__ == "__main__":
    main()
