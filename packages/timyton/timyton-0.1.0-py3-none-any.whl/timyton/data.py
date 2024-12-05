import datetime
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx
from xdg_base_dirs import xdg_config_home, xdg_data_home

from .utils import BearerAuth

TIMEOUT: datetime.timedelta = datetime.timedelta(days=1)
__FAKE_LINE_ID = -1


@dataclass
class Config:
    date_fmt: str = "%x"
    address: str = ""
    database: str = ""
    username: str = ""
    employee: int | None = None
    app_key: str = ""

    @property
    def base_url(self):
        return f"{self.address}/{self.database}/timesheet"


def config_file() -> Path:
    (config_dir := xdg_config_home() / "timyton").mkdir(parents=True, exist_ok=True)
    return config_dir / "config"


def load_config() -> Config:
    source_file = config_file()
    return (
        Config(**json.loads(source_file.read_text()))
        if source_file.exists()
        else save_config(Config())
    )


def save_config(config: Config) -> Config:
    config_file().write_text(json.dumps(asdict(config)))
    return load_config()


def has_expired(source: str) -> bool:
    with sqlite3.connect(db_file(), detect_types=sqlite3.PARSE_DECLTYPES) as connection:
        last_dt = connection.execute(
            "SELECT last_update FROM dates WHERE source = ?", (source,)
        ).fetchone()
    if last_dt:
        (last_dt,) = last_dt
    else:
        last_dt = datetime.datetime(datetime.MINYEAR, 1, 1)
    return (datetime.datetime.now() - last_dt) > TIMEOUT


def adapt_date_iso(val: datetime.date) -> str:
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()


def adapt_datetime_iso(val: datetime.datetime) -> str:
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()


def adapt_timedelta(val: datetime.timedelta) -> int:
    """Adapt datetime.timedelta to integer"""
    return int(val.total_seconds())


sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
sqlite3.register_adapter(datetime.timedelta, adapt_timedelta)


def convert_date(val: bytes) -> datetime.date:
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())


def convert_datetime(val: bytes) -> datetime.datetime:
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())


def convert_timedelta(val: bytes) -> datetime.timedelta:
    """Convert int to datetime.timedelta object."""
    return datetime.timedelta(seconds=float(val))


sqlite3.register_converter("DATE", convert_date)
sqlite3.register_converter("DATETIME", convert_datetime)
sqlite3.register_converter("INTERVAL", convert_timedelta)


def db_file() -> Path:
    (data_dir := xdg_data_home() / "timyton").mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(data_dir / "cache.db") as connection:
        existing_tables = {
            r[0]
            for r in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
                " AND name IN ('timesheets', 'works', 'employees', 'dates')"
            )
        }
        if len(existing_tables) < 4:
            if "timesheets" not in existing_tables:
                connection.execute(
                    """CREATE TABLE timesheets (
                        id INTEGER PRIMARY KEY,
                        work INTEGER,
                        date DATE,
                        duration INTERVAL,
                        description VARCHAR,
                        uuid VARCHAR,
                        dirty BOOLEAN,
                        deleted BOOLEAN
                    )"""
                )
            if "works" not in existing_tables:
                connection.execute(
                    """CREATE TABLE works (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR,
                        start DATE,
                        end DATE
                    )"""
                )
            if "employees" not in existing_tables:
                connection.execute(
                    """CREATE TABLE employees (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR
                    )"""
                )
            if "dates" not in existing_tables:
                connection.execute(
                    """CREATE TABLE dates (
                        source VARCHAR PRIMARY KEY,
                        last_update DATETIME
                    )"""
                )
    return data_dir / "cache.db"


@dataclass
class Employee:
    id: int
    name: str


async def get_employees(config: Config) -> list[Employee]:
    q = "SELECT id, name FROM employees"
    with sqlite3.connect(db_file()) as connection:
        cached_employees = [Employee(*r) for r in connection.execute(q)]
    if cached_employees and not has_expired("employees"):
        return cached_employees

    employees_url = f"{config.base_url}/employees"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(employees_url, auth=BearerAuth(config.app_key))
            employees = response.json()
    except httpx.ConnectError:
        return cached_employees

    with sqlite3.connect(db_file()) as connection:
        connection.execute("DELETE FROM employees")
        for employee in employees:
            connection.execute(
                "INSERT INTO employees(id, name) VALUES (?, ?)",
                (employee["id"], employee["name"]),
            )
        connection.execute(
            """INSERT INTO dates(source, last_update) VALUES ('employees', ?)
            ON CONFLICT(source) DO UPDATE SET last_update=excluded.last_update
            """,
            (datetime.datetime.now(),),
        )

    return [Employee(**e) for e in employees]


@dataclass
class TimesheetLine:
    id: int = 0
    work: int | None = None
    work_name: str = ""
    date: datetime.date | None = None
    duration: datetime.timedelta | None = None
    description: str = ""
    uuid: str | None = None
    dirty: bool = False


async def get_timesheet_lines(
    config: Config, date: datetime.date
) -> list[TimesheetLine]:
    try:
        await get_works(config)
    except httpx.ConnectError:
        pass

    q = """
        SELECT
            t.id, w.id, w.name, t.date, t.duration, t.description,
            t.uuid, t.dirty
        FROM timesheets AS t INNER JOIN works AS w ON t.work = w.id
        WHERE t.date = ?"""
    with sqlite3.connect(db_file(), detect_types=sqlite3.PARSE_DECLTYPES) as connection:
        timesheets = [TimesheetLine(*t) for t in connection.execute(q, (date,))]

    unsaved = any(l.dirty or l.id < 0 for l in timesheets)

    source = f'lines-{date.strftime("%Y-%m-%d")}'
    if unsaved or not has_expired(source):
        return timesheets

    employee_lines_url = (
        f"{config.base_url}/employee/{config.employee}/"
        f"lines/{date.strftime('%Y-%m-%d')}"
    )
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                employee_lines_url, auth=BearerAuth(config.app_key)
            )
            remote_lines = response.json()
    except httpx.ConnectError:
        return timesheets

    timesheets = []
    with sqlite3.connect(db_file()) as connection:
        for r_line in remote_lines:
            r_line["dirty"] = False
            r_line["date"] = date
            r_line["duration"] = datetime.timedelta(seconds=r_line["duration"])
            r_line["work_name"] = r_line["work.name"]
            del r_line["work.name"]
            timesheets.append(TimesheetLine(**r_line))
            connection.execute(
                """INSERT INTO timesheets(
                    id, work, date, duration, description, uuid, dirty)
                VALUES (?, ?, ?, ?, ?, ?, FALSE)
                ON CONFLICT(id) DO UPDATE SET
                    uuid=excluded.uuid,
                    work=excluded.work,
                    date=excluded.date,
                    duration=excluded.duration,
                    description=excluded.description
                """,
                (
                    r_line["id"],
                    r_line["work"],
                    r_line["date"],
                    r_line["duration"],
                    r_line["description"],
                    r_line["uuid"],
                ),
            )
        connection.execute(
            """INSERT INTO dates(source, last_update)
            VALUES (?, ?) ON CONFLICT(source) DO UPDATE SET
                last_update=excluded.last_update
            """,
            (source, datetime.datetime.now()),
        )

    return timesheets


def get_timesheet_line(line_id: int) -> TimesheetLine | None:
    q = """
        SELECT
            t.id, w.id, w.name, t.date, t.duration, t.description,
            t.uuid, t.dirty
        FROM timesheets AS t INNER JOIN works AS w ON t.work = w.id
        WHERE t.id = ?"""
    with sqlite3.connect(db_file(), detect_types=sqlite3.PARSE_DECLTYPES) as connection:
        row = connection.execute(q, (line_id,))
        if not row:
            return None
        return TimesheetLine(*row.fetchone())


def save_timesheet_line(line: TimesheetLine) -> None:
    q = """INSERT INTO timesheets(id, work, date, duration, description, uuid, dirty)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        work=excluded.work, date=excluded.date, duration=excluded.duration,
        description=excluded.description, uuid=excluded.uuid, dirty=excluded.dirty
    """
    with sqlite3.connect(db_file()) as connection:
        connection.execute(
            q,
            (
                line.id,
                line.work,
                line.date,
                line.duration,
                line.description,
                line.uuid,
                line.dirty,
            ),
        )


def delete_timesheet_line(line_id: int) -> None:
    with sqlite3.connect(db_file()) as connection:
        connection.execute("UPDATE timesheets SET deleted=true WHERE id=?", (line_id,))


async def synchronise_lines(config: Config) -> None:
    with sqlite3.connect(db_file(), detect_types=sqlite3.PARSE_DECLTYPES) as connection:
        connection.execute("DELETE FROM timesheets WHERE id < 0 AND deleted=true")
        deleted_lines = connection.execute(
            "SELECT id FROM timesheets WHERE deleted=true"
        )

        to_delete = []
        try:
            async with httpx.AsyncClient() as client:
                for (deleted,) in deleted_lines:
                    delete_request = await client.delete(
                        f"{config.base_url}/line/{deleted}",
                        auth=BearerAuth(config.app_key)
                    )
                    delete_request.raise_for_status()
                    to_delete.append(deleted)
        except httpx.ConnectError:
            pass

        if to_delete:
            ids = ",".join(map(str, to_delete))
            connection.execute("DELETE FROM timesheets WHERE id in (%s)" % ids)

        updated_lines = connection.execute(
            "SELECT id, uuid, work, date, duration, description FROM timesheets"
            " WHERE id > 0 AND dirty = true"
        )
        try:
            async with httpx.AsyncClient() as client:
                for id, uuid, work, date, duration, description in updated_lines:
                    update_request = await client.put(
                        f"{config.base_url}/line/{id}",
                        auth=BearerAuth(config.app_key),
                        json={
                            "id": id,
                            "uuid": uuid,
                            "work": work,
                            "date": date.isoformat(),
                            "duration": duration.total_seconds(),
                            "description": description,
                        },
                    )
                    update_request.raise_for_status()
                    connection.execute(
                        "UPDATE timesheets SET dirty=false WHERE id=?", (id,)
                    )
        except httpx.ConnectError:
            pass

        created_lines = connection.execute(
            "SELECT id, uuid, work, date, duration, description FROM timesheets"
            " WHERE id < 0"
        )
        try:
            async with httpx.AsyncClient() as client:
                for id, uuid, work, date, duration, description in created_lines:
                    create_request = await client.post(
                        f"{config.base_url}/line",
                        auth=BearerAuth(config.app_key),
                        json={
                            "id": id,
                            "uuid": uuid,
                            "work": work,
                            "date": date.isoformat(),
                            "duration": duration.total_seconds(),
                            "description": description,
                        },
                    )
                    create_request.raise_for_status()
                    created_data = create_request.json()
                    connection.execute(
                        "UPDATE timesheets SET dirty=false, id=? WHERE uuid=?",
                        (created_data["id"], uuid),
                    )
        except httpx.ConnectError:
            pass


@dataclass
class Work:
    id: int
    name: str
    start: datetime.date
    end: datetime.date

    def active_on(self, date: datetime.date) -> bool:
        if not self.start and not self.end:
            return True
        elif not self.start:
            return date <= self.end
        elif not self.end:
            return self.start <= date
        else:
            return self.start <= date <= self.end


async def get_works(config: Config) -> list[Work]:
    q = "SELECT id, name, start, end FROM works"
    with sqlite3.connect(db_file(), detect_types=sqlite3.PARSE_DECLTYPES) as connection:
        cached_works = [Work(*r) for r in connection.execute(q)]
    if cached_works and not has_expired("works"):
        return cached_works

    works_url = f"{config.base_url}/employee/{config.employee}/works"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(works_url, auth=BearerAuth(config.app_key))
            works = response.json()
    except httpx.ConnectError:
        return cached_works

    with sqlite3.connect(db_file()) as connection:
        connection.execute("DELETE FROM works")
        for work in works:
            connection.execute(
                "INSERT INTO works(id, name, start, end) " "VALUES (?, ?, ?, ?)",
                (
                    work["id"],
                    work["name"],
                    (
                        datetime.datetime.strptime(work["start"], "%Y-%m-%d").date()
                        if work["start"]
                        else None
                    ),
                    (
                        datetime.datetime.strptime(work["end"], "%Y-%m-%d").date()
                        if work["end"]
                        else None
                    ),
                ),
            )
        connection.execute(
            """INSERT INTO dates(source, last_update) VALUES ('works', ?)
            ON CONFLICT(source) DO UPDATE SET last_update=excluded.last_update
            """,
            (datetime.datetime.now(),),
        )

    return [Work(**w) for w in works]


def get_line_id() -> int:
    global __FAKE_LINE_ID
    __FAKE_LINE_ID -= 1
    return __FAKE_LINE_ID
