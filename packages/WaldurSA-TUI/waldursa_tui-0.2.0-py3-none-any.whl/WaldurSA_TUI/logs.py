from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label, Input, DataTable, Button, Rule
from textual.containers import Container, Vertical, Horizontal
from textual_datepicker import DateSelect
from textual.worker import Worker, WorkerState, get_current_worker
from textual.reactive import reactive
from rich.text import Text
from textual import work
from cysystemd.reader import JournalReader, JournalOpenMode, Rule as ReRule
from WaldurSA_TUI import error
from WaldurSA_TUI import detailed_log

import datetime
import re
import os
import asyncio


class LabelItem(ListItem):
    def __init__(self, content: str) -> None:
        super().__init__()

        self.content = content

    def compose(self) -> ComposeResult:
        yield Label(self.content, id="side_menu_logs_button")

    def get_content(self):
        return self.content


class Logs(Container):
    countdown = reactive(30)

    def __init__(self):
        super().__init__()

        self.list_view_menu = ListView(classes="box", id="side_menu_logs")
        self.search_bar = Input(placeholder="Search...", id="search_bar_logs")
        self.logs_raw = []
        self.logs_filtered = []
        self.selectedView = "Processing Orders"  # the default view
        self.dataTable = DataTable(id="logs_table")
        self.display_worker = None

        self.refresh_button = Button(
            "Refreshing in " + str(self.countdown) + "s", id="refresh"
        )
        self.refresh_status = "started"

        self.fromtime = ""
        self.totime = ""

    async def test_menu(
        self,
    ):  # if there are more than these three options, it will be removed/changed
        test_list = []
        test_list.append("Processing Orders")
        test_list.append("User Membership Synchronization")
        test_list.append("Usage Reporting")
        return test_list

    async def update_logs(self, logs):
        self.logs_raw = logs
        self.logs_filtered = logs

    @work(exclusive=True, thread=True, group="getLogs")
    async def get_logs(self, side_menu_text):
        unit = ""

        if side_menu_text == "Processing Orders":
            unit = "waldur-agent-order-process.service"
        elif side_menu_text == "User Membership Synchronization":
            unit = "waldur-agent-membership-sync.service"
        elif side_menu_text == "Usage Reporting":
            unit = "waldur-agent-report.service"

        rules = ReRule("_SYSTEMD_UNIT", unit)

        reader = JournalReader()
        reader.open(JournalOpenMode.SYSTEM)
        reader.seek_head()
        reader.add_filter(rules)

        pattern = re.compile(r"\[(.*)\]\s+\[(.*)\]\s+(.*)")

        logs = []
        if not get_current_worker().is_cancelled:
            for entry in reader:
                matches = pattern.match(entry["MESSAGE"])
                if matches:
                    log_level, timestamp, message = matches.groups()
                    if (
                        log_level.lower() == "error"
                        or log_level.lower() == "exception"
                        or "error" in message.lower()
                    ):
                        logs.append(
                            (
                                Text(timestamp.split(",")[0], style="red"),
                                Text(log_level, style="red"),
                                Text(message, style="red"),
                            )
                        )
                    else:
                        logs.append(
                            (
                                Text(timestamp.split(",")[0]),
                                Text(log_level),
                                Text(message),
                            )
                        )

        if not get_current_worker().is_cancelled:
            self.app.call_from_thread(self.update_logs, logs)

    def compose(self) -> ComposeResult:
        yield self.list_view_menu
        with Vertical(id="logdates"):
            with Horizontal(classes="height-auto"):
                yield DateSelect(
                    placeholder="From date",
                    format="YYYY-MM-DD",
                    picker_mount="#logdates",
                    classes="column",
                    id="from_date",
                )
                yield DateSelect(
                    placeholder="To date",
                    format="YYYY-MM-DD",
                    picker_mount="#logdates",
                    classes="column",
                    id="to_date",
                )
                yield Button("input date", id="dateframe")
            with Horizontal(classes="height-auto"):
                yield Input(
                    placeholder="from: xx:xx", id="from_time", validate_on=["changed"]
                )
                yield Input(
                    placeholder="to: xx:xx", id="to_time", validate_on=["changed"]
                )
                yield Button("Input timeframe", id="timeframe")

            with Horizontal(classes="height-auto width-full"):
                with Horizontal(classes="height-auto left-align leftSearch"):
                    yield self.search_bar
                with Horizontal(classes="height-auto right-align rightSort"):
                    yield Button("Sort alphabetically", id="sort_alpha")

            with Horizontal(classes="height-auto width-full"):
                with Horizontal(classes="height-auto left-align"):
                    yield Button("Clear filters", id="clear_filter")
                with Horizontal(classes="height-auto right-align"):
                    yield self.refresh_button
                    yield Button(
                        "Export", id="export", classes="margin-left-1"
                    )  # OK button to close the popup

            yield Rule(line_style="heavy")
            yield self.dataTable

    async def on_list_view_selected(self, event: ListView.Selected):
        if event.list_view.id == "side_menu_logs":
            side_menu_text = event.item.get_content()
            self.selectedView = side_menu_text

            self.logs_raw.clear()
            self.logs_filtered.clear()
            table = self.query_one(DataTable)
            table.clear()
            table.loading = True
            self.get_logs(self.selectedView)

    async def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "search_bar_logs":
            input_text = event.value.lower()

            temp = self.logs_filtered.copy()
            self.logs_filtered.clear()

            for log in temp:
                if input_text in str(log[2]).lower():
                    self.logs_filtered.append(log)

            table = self.query_one(DataTable)
            table.clear()
            table.loading = True
            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(self.display_logs(), exclusive=True)
            table.loading = False

    async def on_input_changed(self, event: Input.Changed):
        if event.input.id == "from_time":
            self.fromtime = event.value
        if event.input.id == "to_time":
            self.totime = event.value

    # Opens new screen with detailed view of one log when clicked on a log in datatabel
    async def on_data_table_row_selected(self, event: DataTable.RowSelected):
        indx = event.row_key
        log_row = DataTable.get_row(self.dataTable, indx)
        date = log_row[0]
        status = log_row[1]
        log_msg = log_row[2]

        self.app.push_screen(
            detailed_log.DetailedLogPopUp(
                date,
                status,
                log_msg,
            )
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "export":
            newpath = "src/test_export_logs"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            for nr, log in enumerate(self.logs_filtered):
                file = open("src/test_export_logs/log_" + str(nr + 1) + ".txt", "w")
                for item in log:
                    file.write(item + "\n")
                file.close()

        if event.button.id == "refresh":
            if self.refresh_status == "started":
                self.refresh_status = "stopped"
            elif self.refresh_status == "stopped":
                self.refresh_status = "started"

        if event.button.id == "clear_filter":
            self.logs_filtered.clear()
            self.logs_filtered = self.logs_raw.copy()

            table = self.query_one(DataTable)
            table.clear()
            table.loading = True
            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(self.display_logs(), exclusive=True)
            table.loading = False

        if event.button.id == "dateframe":
            # dates = self.query_one("#logdates", DateSelect)
            date_select_from = self.query_one("#from_date")
            date_select_to = self.query_one("#to_date")

            table = self.query_one(DataTable)
            table.clear()
            table.loading = True
            temp = self.logs_filtered.copy()
            self.logs_filtered.clear()

            def convert_to_datetime(time):
                date = str(time).split(" ")[0].split("-")

                return datetime.datetime(int(date[0]), int(date[1]), int(date[2]))

            if date_select_from.date is not None and date_select_to.date is not None:
                from_date = convert_to_datetime(date_select_from.date)
                to_date = convert_to_datetime(date_select_to.date)

                if from_date > to_date:
                    self.app.push_screen(
                        error.ErrorPopup(
                            "From time is bigger than to time",
                            "Time error",
                        )
                    )

                for log in temp:
                    time = convert_to_datetime(str(log[0]))
                    if time >= from_date and time <= to_date:
                        self.logs_filtered.append(log)

            elif date_select_from.date is not None:
                from_date = convert_to_datetime(date_select_from.date)
                for log in temp:
                    time = convert_to_datetime(str(log[0]))
                    if time >= from_date:
                        self.logs_filtered.append(log)

            elif date_select_to.date is not None:
                to_date = convert_to_datetime(date_select_to.date)
                for log in temp:
                    time = convert_to_datetime(str(log[0]))
                    if time <= to_date:
                        self.logs_filtered.append(log)

                if self.display_worker is not None:
                    if self.display_worker.is_running:
                        self.display_worker.cancel()
                    self.display_worker = None

                self.display_worker = self.run_worker(
                    self.display_logs(), exclusive=True
                )
                table.loading = False

            else:
                self.app.push_screen(
                    error.ErrorPopup(
                        "No dates selected",
                        "Time error",
                    )
                )

            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(self.display_logs(), exclusive=True)
            table.loading = False

        if event.button.id == "timeframe":
            table = self.query_one(DataTable)
            table.clear()
            table.loading = True
            temp = self.logs_filtered.copy()
            self.logs_filtered.clear()

            def check_time(time):
                pattern = r"(\d\d:\d\d)"
                matches = re.match(pattern, time)
                if matches:
                    times = time.split(":")
                    if int(times[0]) < 0 or int(times[0]) > 23:
                        self.app.push_screen(
                            error.ErrorPopup(
                                "Hours must be between 0 and 23",
                                "Time error",
                            )
                        )
                        return False
                    elif int(times[1]) < 0 or int(times[1]) > 59:
                        self.app.push_screen(
                            error.ErrorPopup(
                                "Minutes must be between 0 and 59",
                                "Time error",
                            )
                        )
                        return False

                else:
                    self.app.push_screen(
                        error.ErrorPopup(
                            "Inputed time is not a correct",
                            "Input error",
                        )
                    )
                    return False
                return True

            pattern = r".*\s(..):(..).*"

            if self.fromtime != "" and self.totime != "":
                if check_time(self.fromtime) and check_time(self.totime):
                    fromtime = int("".join(self.fromtime.split(":")))
                    totime = int("".join(self.totime.split(":")))

                    if fromtime > totime:
                        self.app.push_screen(
                            error.ErrorPopup(
                                "From time is bigger than to time",
                                "Time error",
                            )
                        )

                    for log in temp:
                        matches = re.match(pattern, str(log[0]))
                        if matches:
                            h, m = matches.groups()
                            time = int(h + m)
                            if time >= fromtime and time <= totime:
                                self.logs_filtered.append(log)

            elif self.fromtime != "":
                if check_time(self.fromtime):
                    fromtime = int("".join(self.fromtime.split(":")))

                    for log in temp:
                        matches = re.match(pattern, str(log[0]))
                        if matches:
                            h, m = matches.groups()
                            time = int(h + m)
                            if time >= fromtime:
                                self.logs_filtered.append(log)

            elif self.totime != "":
                if check_time(self.totime):
                    totime = int("".join(self.totime.split(":")))
                    for log in temp:
                        matches = re.match(pattern, str(log[0]))
                        if matches:
                            h, m = matches.groups()
                            time = int(h + m)
                            if time <= totime:
                                self.logs_filtered.append(log)

            else:
                self.app.push_screen(
                    error.ErrorPopup(
                        "No timeframe selected",
                        "Time error",
                    )
                )
            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(self.display_logs(), exclusive=True)
            table.loading = False

        if event.button.id == "sort_alpha":
            self.logs_filtered.sort(key=lambda x: str(x[2]))
            table = self.query_one(DataTable)
            table.clear()
            table.loading = True
            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(self.display_logs(), exclusive=True)
            table.loading = False

    async def on_mount(self):
        await self.make_listView_menu(await self.test_menu())
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Date", "Status", "Log")
        table = self.query_one(DataTable)
        table.loading = True
        self.get_logs(self.selectedView)

        self.timer = self.set_interval(1, self.tick)

    def tick(self) -> None:
        if self.refresh_status == "started":
            self.countdown = self.countdown - 1
            self.refresh_button.label = "Refreshing in " + str(self.countdown) + "s"
            if self.countdown == 0:
                self.countdown = 30
                table = self.query_one(DataTable)
                table.clear()
                table.loading = True
                self.get_logs(self.selectedView)

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS and event.worker.group == "getLogs":
            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(self.display_logs(), exclusive=True)

    async def display_logs(self):
        table = self.query_one(DataTable)
        table.clear()
        batchsize = 500
        table.loading = False
        for i in range(0, len(self.logs_filtered), batchsize):
            batch = self.logs_filtered[i : i + batchsize]
            for j in range(len(batch)):
                table.add_row(*batch[j])
            await asyncio.sleep(0.2)

    async def make_listView_menu(self, list_buttons):
        for button in list_buttons:
            labelItem_button = LabelItem(button)
            self.list_view_menu.append(labelItem_button)
