from textual.widgets import DataTable
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual_plotext import PlotextPlot
from textual.reactive import reactive
from rich.text import Text
from humanfriendly import format_timespan

import subprocess
import re


class Dashboard(Container):
    countdown = reactive(30)

    def __init__(self):
        super().__init__()

        self.table_columns = ("Service", "Uptime", "Last contact", "Status")
        self.service_last_seen = {}
        self.services = [
            "waldur-agent-membership-sync",
            "waldur-agent-order-process",
            "waldur-agent-report",
        ]
        self.service_statuses = []

    def compose(self) -> ComposeResult:
        with Vertical():
            yield DataTable()
            with Horizontal():
                yield PlotextPlot(id="plot1")
                yield PlotextPlot(id="plot2")

    def on_mount(self) -> None:
        for service in self.services:
            self.service_last_seen[service] = -1
        table = self.query_one(DataTable)
        table.cursor_type = "none"
        table.add_columns(*self.table_columns)
        self.get_logs()
        self.render_table()

        plt = self.query_one("#plot1").plt
        y = plt.sin()
        plt.plot(y)
        plt.title("Example 1")

        plt2 = self.query_one("#plot2").plt
        y = plt2.sin()
        plt2.plot(y)
        plt2.title("Example 2")

        self.timer = self.set_interval(1, self.tick)

    def tick(self) -> None:
        self.countdown = self.countdown - 1
        for service in self.service_last_seen:
            if self.service_last_seen[service] != -1:
                self.service_last_seen[service] += 1
        table = self.query_one(DataTable)
        table.clear()
        self.render_table()
        if self.countdown == 0:
            self.countdown = 30
            self.get_logs()

    def get_logs(self):
        statuses = []
        for service in self.services:
            status = self.get_systemd_process_status(service)
            if status["status"] == "OK":
                self.service_last_seen[status["name"]] = 0
            statuses.append(status)
        self.service_statuses = statuses

    def render_table(self):
        table = self.query_one(DataTable)
        for status in self.service_statuses:
            if status["status"] == "FAIL":
                table.add_row(
                    status["name"],
                    status["time"],
                    "No contact",
                    Text(status["status"], style=status["style"]),
                )
            else:
                table.add_row(
                    status["name"],
                    status["time"],
                    format_timespan(self.service_last_seen[status["name"]]) + " ago",
                    Text(status["status"], style=status["style"]),
                )

    def get_systemd_process_status(self, process_name):
        result = subprocess.run(
            ["systemctl", "status", process_name], capture_output=True, text=True
        )

        is_active = "active (running)" in result.stdout

        time_match = re.search(r"since (.*?); (.*? ago)", result.stdout)
        time = time_match.group(2) if time_match else "Unknown"

        return {
            "name": process_name,
            "status": "OK" if is_active else "FAIL",
            "style": "green" if is_active else "red",
            "time": time,
        }
