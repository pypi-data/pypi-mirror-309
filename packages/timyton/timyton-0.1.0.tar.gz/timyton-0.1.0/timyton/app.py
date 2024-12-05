import datetime
import uuid

import httpx
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal
from textual.events import DescendantBlur
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList
from textual.validation import Validator, ValidationResult
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Select,
)

from .data import (
    Config,
    TimesheetLine,
    Work,
    delete_timesheet_line,
    get_employees,
    get_timesheet_lines,
    get_timesheet_line,
    get_works,
    get_line_id,
    load_config,
    save_config,
    save_timesheet_line,
    synchronise_lines,
)


def format_duration(duration: datetime.timedelta | None) -> str:
    if duration is None:
        return ""
    minutes, seconds = divmod(duration.total_seconds(), 60)
    hours, minutes = divmod(minutes, 60)
    if not seconds:
        return "{:02}:{:02}".format(int(hours), int(minutes))
    else:
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def parse_duration(value: str) -> datetime.timedelta:
    hours, minutes, seconds = 0, 0, 0
    match len(splits := value.split(":")):
        case 1:
            minutes = int(splits[0])
        case 2:
            hours, minutes = map(int, splits)
        case 3:
            hours, minutes, seconds = map(int, splits)
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)


class WorkValidator(Validator):
    def __init__(self, works: list[Work]) -> None:
        super().__init__()
        self.works = works

    def validate(self, value) -> ValidationResult:
        if value in {w.name for w in self.works}:
            return self.success()
        else:
            return self.failure("Not a work")


class DurationValidator(Validator):
    def validate(self, value) -> ValidationResult:
        if not isinstance(value, str):
            return self.failure("Not a string")

        match len(splits := value.split(":")):
            case 1 | 2 | 3:
                try:
                    list(map(int, splits))
                    return self.success()
                except (ValueError, TypeError):
                    return self.failure(f"{value} is not a valid duration")
            case _:
                return self.failure("Too many ':'")


class TimesheetLineScreen(ModalScreen):
    DEFAULT_CSS = """
    #editor {
        padding: 1;
        border: thick $background;
        background: $surface;

        grid-size: 2;
        grid-columns: 1fr 3fr;

        width: 75vw;
        height: 25;
    }

    #buttons {
        align: right middle;
        column-span: 2;
    }

    Label {
        padding: 1;
    }

    Button {
        margin: 0 2;
    }
    """

    is_valid_duration: reactive[bool] = reactive(False)
    is_valid_work: reactive[bool] = reactive(False)
    is_valid_form: reactive[bool] = reactive(False)

    def __init__(
        self,
        config: Config,
        line: TimesheetLine | None,
        date: datetime.date | None = None,
    ) -> None:
        super().__init__()
        self.config = config
        if not line:
            line = TimesheetLine()
        self.line = line
        if date is not None:
            line.date = date

    @property
    def date(self) -> datetime.date:
        if not self.line:
            return datetime.date.today()
        return self.line.date if self.line.date else datetime.date.today()

    def compose(self) -> ComposeResult:
        with Grid(id="editor"):
            yield Label("Duration")
            yield Input(placeholder="HH:MM", id="duration")
            yield Label("Work")
            yield Input(id="work")
            yield Label("Description")
            yield Input(id="description")
            with Horizontal(id="buttons"):
                yield Button("Cancel", id="cancel")
                yield Button("Save", id="save")

    @work(exclusive=True, exit_on_error=False)
    async def on_mount(self) -> None:
        works = await get_works(self.config)
        work_wid = self.query_one("#work", Input)
        work_wid.validators = [WorkValidator(works)]
        work_wid.suggester = SuggestFromList(
            [w.name for w in works if w.active_on(self.date)]
        )

        if not self.line:
            return

        duration_wid = self.query_one("#duration", Input)
        duration_wid.value = format_duration(self.line.duration)
        duration_wid.validators = [DurationValidator()]

        work_wid.value = self.line.work_name
        self.query_one("#description", Input).value = self.line.description
        self.is_valid_duration = True
        self.is_valid_work = True

    @work(exclusive=True, exit_on_error=False)
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "cancel":
                self.dismiss(None)
            case "save":
                duration_wid = self.query_one("#duration", Input)
                work_wid = self.query_one("#work", Input)
                description_wid = self.query_one("#description", Input)

                for w in await get_works(self.config):
                    if w.name == work_wid.value:
                        break
                else:
                    return

                self.line.dirty = True
                if not self.line.id:
                    self.line.id = get_line_id()
                if not self.line.date:
                    self.line.date = datetime.date.today()
                self.line.duration = parse_duration(duration_wid.value)
                self.line.description = description_wid.value
                if not self.line.uuid:
                    self.line.uuid = str(uuid.uuid4())
                self.line.work_name = w.name
                self.line.work = w.id
                self.dismiss(self.line)

    def watch_is_valid_form(self, value: bool) -> None:
        save_button: Button = self.query_one("#save", Button)
        save_button.disabled = not self.is_valid_form

    @on(Input.Changed)
    def update_validity(self, event: Input.Changed) -> None:
        if event.validation_result:
            match event.input.id:
                case "duration":
                    self.is_valid_duration = event.validation_result.is_valid
                case "work":
                    self.is_valid_work = event.validation_result.is_valid
                case "description":
                    return
        self.is_valid_form = self.is_valid_work and self.is_valid_duration

    @on(DescendantBlur)
    def reformat_duration(self, event: DescendantBlur) -> None:
        duration_wid: Input = self.query_one("#duration", Input)
        duration_validation = duration_wid.validate(duration_wid.value)
        if duration_validation and duration_validation.is_valid:
            duration_wid.value = format_duration(parse_duration(duration_wid.value))


class Preferences(ModalScreen):
    DEFAULT_CSS = """
    #preferences {
        padding: 1;
        border: thick $background;
        background: $surface;

        grid-size: 2;
        grid-columns: 1fr 2fr;
        grid-gutter: 1;

        width: 50vw;
        height: 27;
    }

    #app_key_box  {
        grid-size: 2;
        grid-columns: 4fr 1fr;
    }

    #buttons {
        align: right middle;
        column-span: 2;
    }
    """

    app_key: reactive[str | None] = reactive(None)

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

    def compose(self) -> ComposeResult:
        with Grid(id="preferences"):
            yield Label("Server Address")
            yield Input(
                placeholder="https://tryton.dunder-mifflin.example",
                id="address",
            )
            yield Label("Database")
            yield Input(placeholder="dunder-mifflin", id="database")
            yield Label("User Name")
            yield Input(placeholder="michael", id="username")
            yield Label("Application Key")
            with Grid(id="app_key_box"):
                yield Input(disabled=True, id="app_key")
                yield Button("Reset", variant="warning", disabled=True, id="reset")
                yield Button(
                    "Register", variant="primary", disabled=True, id="register"
                )
            yield Label("Employee")
            yield Select([], id="employee")
            with Horizontal(id="buttons"):
                yield Button("Close", id="close")

    @work(exclusive=True, exit_on_error=False)
    async def on_mount(self) -> None:
        self.app_key = self.config.app_key
        self.query_one("#address", Input).value = self.config.address
        self.query_one("#database", Input).value = self.config.database
        self.query_one("#username", Input).value = self.config.username
        employee_wid = self.query_one("#employee", Select)
        employee_wid.set_options(
            (e.name, e.id) for e in await get_employees(self.config)
        )
        employee_wid.value = self.config.employee

    def watch_app_key(self, new_key: str | None) -> None:
        if new_key is None:
            return
        self.config.app_key = new_key
        self.query_one("#app_key", Input).value = new_key[:10] + "…" if new_key else ""
        self.query_one("#reset", Button).disabled = not bool(new_key)
        self.query_one("#register", Button).disabled = bool(new_key)
        self.query_one("#employee", Select).disabled = not bool(new_key)
        self.query_one("#reset", Button).styles.display = (
            "none" if not self.config.app_key else "block"
        )
        self.query_one("#register", Button).styles.display = (
            "block" if not self.config.app_key else "none"
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        match event.input.id:
            case "address":
                self.config.address = event.value
            case "database":
                self.config.database = event.value
            case "username":
                self.config.username = event.value

    @on(Select.Changed)
    def employee_changed(self, event: Select.Changed) -> None:
        self.config.employee = event.value
        save_config(self.config)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        user_app_url = f"{self.config.address}/{self.config.database}/user/application/"
        if event.button.id == "close":
            self.app.pop_screen()
        elif event.button.id == "reset":
            async with httpx.AsyncClient() as client:
                # Use request while trytond still expects form-data on DELETE
                await client.request(
                    "DELETE",
                    user_app_url,
                    json={
                        "user": self.config.username,
                        "key": self.config.app_key,
                        "application": "timesheet",
                    },
                )
            self.app_key = ""
            self.query_one("#close", Button).focus()
        elif event.button.id == "register":
            async with httpx.AsyncClient() as client:
                key_request = await client.post(
                    user_app_url,
                    json={
                        "user": "nicoe",
                        "application": "timesheet",
                    },
                )
                key_request.raise_for_status()
                self.app_key = key_request.json()
            self.query_one("#employee", Select).focus()
            save_config(self.config)


class Timyton(App[None]):
    ENABLE_COMMAND_PALETTE = False
    TITLE = "timyton"
    BINDINGS = [
        Binding("n", "new_line", "New line"),
        Binding("d", "delete_line", "Delete line"),
        Binding("j", "next_line", "Next Line", show=False),
        Binding("k", "previous_line", "Previous Line", show=False),
        Binding("h", "previous_day", "Previous Day", show=False),
        Binding("left", "previous_day", "Previous Day", show=False),
        Binding("l", "next_day", "Next Day", show=False),
        Binding("right", "next_day", "Next Day", show=False),
        Binding("t", "go_today", "Today"),
        Binding("q", "quit", "Quit"),
        Binding("p", "show_preferences", "Show Preferences"),
    ]

    DEFAULT_CSS = """
    #date {
        height: 3;
        width: 100%;
        content-align: center middle;
        border: solid white;
    }

    #timesheets {
        height: 1fr;
    }

    Preferences {
        align: center middle;
    }

    TimesheetLineScreen {
        align: center middle;
    }

    DataTable {
        width: 100%;
    }
    """

    date: reactive[datetime.date] = reactive(datetime.date.today)

    def __init__(self) -> None:
        super().__init__()
        self.config: Config = load_config()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("", id="date")
        yield DataTable()
        yield Footer()

    async def on_mount(self) -> None:
        self.date = datetime.date.today()
        table = self.query_one(DataTable)
        self.column_keys = table.add_columns("Duration", "Work", "Description")
        table.cursor_type = "row"
        if not self.config.employee:
            self.action_show_preferences()
        await synchronise_lines(self.config)

    def action_show_preferences(self) -> None:
        def update_preferences(preferences: dict) -> None:
            self.config = save_config(Config(**preferences))

        self.push_screen(Preferences(self.config), update_preferences)

    @work(exclusive=True, exit_on_error=False)
    async def watch_date(self, new_date: datetime.date) -> None:
        label = self.query_one("#date", Label)
        text = Text.from_markup(
            f"[bold]{new_date.strftime(self.config.date_fmt)}[/bold]"
        )
        label.update(text)

        table = self.query_one(DataTable)
        table.clear()
        for line in await get_timesheet_lines(self.config, self.date):
            table.add_row(
                format_duration(line.duration),
                line.work_name,
                line.description,
                key=str(line.id),
            )

    def action_previous_day(self) -> None:
        self.date -= datetime.timedelta(days=1)

    async def action_next_day(self) -> None:
        self.date += datetime.timedelta(days=1)

    def action_go_today(self) -> None:
        self.date = datetime.date.today()

    def action_next_line(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_coordinate = table.cursor_coordinate.down()

    def action_previous_line(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_coordinate = table.cursor_coordinate.up()

    @work(exclusive=True, exit_on_error=False)
    async def action_new_line(self) -> None:
        new_line = TimesheetLine()

        async def add_line(line: TimesheetLine | None) -> None:
            if not line:
                return
            table: DataTable = self.query_one(DataTable)
            table.add_row(
                format_duration(line.duration),
                line.work_name,
                line.description,
                key=str(line.id),
            )
            save_timesheet_line(line)

        self.push_screen(
            TimesheetLineScreen(self.config, new_line, self.date), add_line
        )

    @work(exclusive=True, exit_on_error=False)
    async def action_delete_line(self) -> None:
        table: DataTable = self.query_one(DataTable)
        if table.is_valid_coordinate(table.cursor_coordinate):
            row_key, column_key = table.coordinate_to_cell_key(table.cursor_coordinate)
            table.remove_row(row_key)
            if row_key.value is not None:
                delete_timesheet_line(int(row_key.value))

    @on(DataTable.RowSelected)
    @work(exclusive=True, exit_on_error=False)
    async def action_edit_line(self, event: DataTable.RowSelected) -> None:
        if event.row_key.value is not None:
            line = get_timesheet_line(int(event.row_key.value))
        else:
            line = None

        async def update_line(line: TimesheetLine | None) -> None:
            if not line:
                return
            table: DataTable = self.query_one(DataTable)
            table.update_cell(
                event.row_key, self.column_keys[0], format_duration(line.duration)
            )
            table.update_cell(event.row_key, self.column_keys[1], line.work_name)
            table.update_cell(event.row_key, self.column_keys[2], line.description)
            save_timesheet_line(line)

        self.push_screen(TimesheetLineScreen(self.config, line), update_line)

    async def action_quit(self) -> None:
        await synchronise_lines(self.config)
        self.exit(0)


def run() -> None:
    Timyton().run()
