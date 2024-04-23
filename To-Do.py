import flet as ft
import calendar
from datetime import datetime

cal = calendar.Calendar()

# pre-defined calendar maps ...
date_class: dict[int, str] = {
    0: "Mo",
    1: "Tu",
    2: "We",
    3: "Th",
    4: "Fr",
    5: "Sa",
    6: "Su",
}

month_class: dict[int, str] = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

# Date class to handle calendar logic ...
class Settings:
    year: int = datetime.now().year
    month: int = datetime.now().month

    @staticmethod
    def get_year():
        return Settings.year

    @staticmethod
    def get_month():
        return Settings.month

    @staticmethod
    def get_date(delta: int):
        if delta == 1:
            if Settings.month + delta > 12:
                Settings.month = 1
                Settings.year += 1
            else:
                Settings.month += 1

        if delta == -1:
            if Settings.month + delta < 1:
                Settings.month = 12
                Settings.year -= 1
            else:
                Settings.month -= 1


date_box_style = {
    "width": 30,
    "height": 30,
    "alignment": ft.alignment.center,
    "shape": ft.BoxShape("rectangle"),
    "animate": ft.Animation(400, "ease"),
    "border_radius": 5,
}

class DateBox(ft.Container):
    def __init__(
        self,
        day: int,
        date: str = None,
        date_instance: ft.Column = None,
        task_instance: ft.Column = None,
        opacity_: float | int = None,
    ):
        super(DateBox, self).__init__(
            **date_box_style,
            data=date,
            opacity=opacity_,
            on_click=self.selected,
        )

        self.day = day
        self.date_instance = date_instance
        self.task_instance = task_instance
        self.content = ft.Text(self.day, text_align="center")

    def selected(self, e: ft.TapEvent):
        if self.date_instance:
            self.task_instance.event.value = ""

            for row in self.date_instance.controls[1:]:
                for date in row.controls:
                    date.bgcolor = "#20303e" if date == e.control else None
                    date.border = (
                        ft.border.all(0.5, "#4fadf9") if date == e.control else None
                    )

                    if date == e.control:
                        self.task_instance.date.value = e.control.data
                        events = get_events_for_date(e.control.data)
                        self.task_instance.event.value = "\n".join(events) if events else ""

            self.date_instance.update()
            self.task_instance.update()


def get_events_for_date(date: str):
    # Placeholder: Return events for the date from a database or data source
    # For now, returning an empty list
    return []


class DateGrid(ft.Column):
    def __init__(self, year: int, month: int, task_instance: object):
        super(DateGrid, self).__init__()

        self.year = year
        self.month = month
        self.task_manager = task_instance
        self.date = ft.Text(f"{month_class[self.month]} {self.year}")
        self.year_and_month = ft.Container(
            bgcolor="#20303e",
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
            content=ft.Row(
                alignment="center",
                controls=[
                    ft.IconButton(
                        "chevron_left",
                        on_click=lambda e: self.update_date_grid(e, -1),
                    ),
                    ft.Container(
                        width=150, content=self.date, alignment=ft.alignment.center
                    ),
                    ft.IconButton(
                        "chevron_right",
                        on_click=lambda e: self.update_date_grid(e, 1),
                    ),
                ],
            ),
        )

        self.controls.insert(1, self.year_and_month)

        week_days = ft.Row(
            alignment="spaceEvenly",
            controls=[
                DateBox(day=date_class[index], opacity_=0.7) for index in range(7)
            ],
        )

        self.controls.insert(1, week_days)
        self.populate_date_grid(self.year, self.month)

    def populate_date_grid(self, year: int, month: int):
        del self.controls[2:]

        for week in cal.monthdayscalendar(year, month):
            row = ft.Row(alignment="spaceEvenly")
            for day in week:
                if day != 0:
                    row.controls.append(
                        DateBox(day, self.format_date(day), self, self.task_manager)
                    )
                else:
                    row.controls.append(DateBox(" "))

            self.controls.append(row)

    def update_date_grid(self, e: ft.TapEvent, delta: int):
        Settings.get_date(delta)
        self.update_year_and_month(
            Settings.get_year(),
            Settings.get_month(),
        )

        self.populate_date_grid(
            Settings.get_year(),
            Settings.get_month(),
        )

        self.update()

    def update_year_and_month(self, year: int, month: int):
        self.year = year
        self.month = month
        self.date.value = f"{month_class[self.month]} {self.year}"

    def format_date(self, day: int):
        return f"{month_class[self.month]} {day}, {self.year}"


def input_style(height: int):
    return {
        "height": height,
        "focused_border_color": "blue",
        "border_radius": 5,
        "cursor_height": 16,
        "cursor_color": "white",
        "content_padding": 10,
        "border_width": 1.5,
        "text_size": 12,
    }


class TaskManager(ft.Column):
    def __init__(self):
        super(TaskManager, self).__init__()

        self.date = ft.TextField(
            label="Date", read_only=True, value=" ", **input_style(38)
        )
        
        self.event = ft.TextField(
            label="Event", **input_style(38)
        )
        self.event.placeholder = "Enter event..."

        self.controls = [self.date, self.event]


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1f2128"

    task_manager = TaskManager()

    grid = DateGrid(
        year=Settings.get_year(), month=Settings.get_month(), task_instance=task_manager
    )

    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    height=350,
                    border=ft.border.all(0.75, "#4fadf9"),
                    border_radius=10,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=grid,
                ),
                ft.Divider(color="transparent", height=20),
                task_manager,
            ],
        ),
    )

    page.update()


ft.app(main)
