from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label
from textual.screen import ModalScreen

import os


class DetailedLogPopUp(ModalScreen):
    "Detailed view of a log."

    def __init__(self, date: str, status: str, log_msg: str) -> None:
        super().__init__()
        self.date = date
        self.status = status
        self.log_msg = log_msg

    def compose(self) -> ComposeResult:
        # Create the content for the modal (log details and OK button)
        with Horizontal():
            with Vertical():
                yield Container(
                    Label("Date       Time", id="date_label"),
                    Label(self.date, id="date"),
                )
            with Vertical():
                yield Container(
                    Label("Status", id="status_label"),
                    Label(self.status, id="status"),
                )
            yield Container(
                Button("Export", id="export_button"),
            )

        yield Container(
            Label("Log message", id="log_message"),
            Label(self.log_msg, id="log"),  # Display the log message
        )
        yield Container(
            Button.success("OK", id="close_button"),  # OK button to close the popup
            id="center",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Export the log
        if event.button.id == "export_button":
            newpath = "src/test_export_logs"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            file = open("src/test_export_logs/detailed_log.txt", "w")
            file.write("Date-Time: " + str(self.date) + "\n")
            file.write("Status: " + str(self.status) + "\n")
            file.write("Log message: " + str(self.log_msg) + "\n")
            file.close()

        # Close the popup when OK button is pressed
        if event.button.id == "close_button":
            self.app.pop_screen()
