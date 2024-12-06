from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label, Input, DataTable
from textual.containers import Container, Vertical
from textual.worker import Worker, WorkerState, get_current_worker
from textual import work
from cysystemd.reader import JournalReader, JournalOpenMode, Rule as ReRule

import re
import yaml


class LabelItem(ListItem):
    def __init__(self, content: str) -> None:
        super().__init__()

        self.content = content

    def compose(self) -> ComposeResult:
        yield Label(self.content, id="side_menu_offerings_button")

    def get_content(self):
        return self.content


class Configured_offerings(Container):
    def __init__(self):
        super().__init__()

        self.list_view_menu = ListView(classes="box", id="side_menu_offerings_listview")
        self.search_bar = Input(placeholder="Search...", id="search_bar_offerings")
        self.dataTable = DataTable(id="data_table_offerings")
        self.offerings = []
        self.offerings2 = set()
        self.display_worker = None

    async def test_paramaters(self):  # will be removed when actual data is used
        test_list = []
        for i in range(1, 15):
            test_list.append(["Item " + str(i), "value " + str(i)])
        return test_list

    async def populate_table(self, offering_name):
        offering = self.get_offering_by_name(offering_name, self.offerings2)
        if offering is None:
            return
        self.dataTable.add_row("backend_type", offering["backend_type"])
        for key in offering["backend_settings"]:
            self.dataTable.add_row(key, offering["backend_settings"][key])
        for key in offering["backend_components"]:
            self.dataTable.add_row(key, offering["backend_components"][key])

    async def read_offerings(self, path):
        with open(path, "r") as file:
            yaml_loaded = yaml.safe_load(file)
            return yaml_loaded["offerings"]

    def get_offering_by_name(self, name, offerings):
        for offering in offerings:
            if offering["name"] == name:
                return offering
        return None

    @work(exclusive=True, thread=True, group="getOfferings")
    async def get_offerings(self):
        unit = "waldur-agent-report.service"

        rules = ReRule("_SYSTEMD_UNIT", unit)

        reader = JournalReader()
        reader.open(JournalOpenMode.SYSTEM)
        reader.seek_head()
        reader.add_filter(rules)

        pattern = re.compile(r"\[(.*)\]\s+\[(.*)\]\s+(.*)")
        pattern2 = re.compile(r"Using (.*) as a config source$")

        if not get_current_worker().is_cancelled:
            for entry in reader:  # find a way to only read first few entries
                matches = pattern.match(entry["MESSAGE"])
                if matches:
                    log_level, timestamp, message = matches.groups()
                    matches2 = pattern2.match(message)
                    if matches2:
                        self.offerings2 = await self.read_offerings(
                            matches2.groups()[0]
                        )

    def compose(self) -> ComposeResult:
        with Vertical(id="side_menu_offerings"):
            yield self.search_bar
            yield self.list_view_menu
        yield self.dataTable

    async def on_list_view_selected(self, event: ListView.Selected):
        if event.list_view.id == "side_menu_offerings_listview":
            side_menu_text = event.item.get_content()
            self.dataTable.clear()
            await self.populate_table(side_menu_text)

    async def on_input_submitted(self, event: Input.Submitted):
        input_text = event.value.lower()
        side_menu = self.query_one("#side_menu_offerings_listview", ListView)

        if input_text == "":
            for i in range(len(self.offerings)):
                if self.offerings[i] not in side_menu.children:
                    self.list_view_menu.append(self.offerings[i])
        else:
            for i in range(len(self.offerings)):
                if input_text in self.offerings[i].get_content().lower():
                    if self.offerings[i] not in side_menu.children:
                        side_menu.append(self.offerings[i])
                else:
                    for j in range(len(side_menu.children)):
                        if self.offerings[i] == side_menu.children[j]:
                            side_menu.remove_items(iter([j]))
                            break

    async def on_mount(self):
        self.list_view_menu.loading = True
        self.get_offerings()
        self.dataTable.add_columns("Item", "Value")

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS and event.worker.group == "getOfferings":
            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(
                self.display_offerings(), exclusive=True
            )

    async def display_offerings(self):
        list = self.list_view_menu
        list.clear()
        await self.make_listView_menu(self.offerings2)
        if len(list.children) > 0:
            await self.populate_table(list.children[0].get_content())
        list.loading = False

    async def make_listView_menu(self, offerings):
        for offering in offerings:
            labelItem_button = LabelItem(offering["name"])
            self.list_view_menu.append(labelItem_button)
            self.offerings.append(labelItem_button)
