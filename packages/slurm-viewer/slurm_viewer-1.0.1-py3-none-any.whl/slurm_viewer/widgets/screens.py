from __future__ import annotations

from typing import Any

from rich.style import Style
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.widgets import Button, SelectionList, DataTable, Label
from textual.widgets.selection_list import Selection

from slurm_viewer.data.queue_model import Queue
from slurm_viewer.data.node_model import Node
from slurm_viewer.widgets.column_selector import ColumnSelection
from slurm_viewer.widgets.table_formatting import format_value


class SelectColumnsScreen(ModalScreen):
    BINDINGS = [('escape', 'pop_screen')]
    DEFAULT_CSS = """
    SelectColumnsScreen {
        align: center middle;
        width: auto;
        height: auto;
    }
    
    SelectColumnsScreen SelectionOrderList {
        align: center middle;
        height: auto;
        width: 100%;
    }
    
    SelectColumnsScreen Vertical {
        height: auto;
        width: 45;
    }
    
    SelectColumnsScreen Horizontal {
        width: auto;
        height: auto;
    }
    
    SelectColumnsScreen Button {
        width: 23;
    }
    """

    def __init__(self, selected_columns: list[str], remaining_columns: list[str]) -> None:
        super().__init__()
        self.selected_columns = selected_columns
        self.remaining_columns = remaining_columns

    def compose(self) -> ComposeResult:
        with Vertical():
            selections = [Selection(x, x, True) for x in self.selected_columns]
            selections.extend([Selection(x, x, False) for x in self.remaining_columns])

            yield SelectionList[str](*selections)
            with Horizontal():
                yield Button('Ok', variant='success', id='ok')
                yield Button('Cancel', variant='warning', id='cancel')

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'ok':
            self.dismiss(self.result())
        else:
            self.dismiss(None)

    def result(self) -> list[str]:
        data: list[str] = self.query_one(SelectionList).selected
        return data


class SelectPartitionScreen(ModalScreen):
    BINDINGS = [
        ('delete', 'deselect_all'),
        ('insert', 'select_all'),
        ('escape', 'pop_screen')
    ]

    DEFAULT_CSS = """
    SelectPartitionScreen {
        align: center middle;
        width: auto;
        height: auto;
    }
    
    SelectPartitionScreen Vertical {
        height: auto;
        width: auto;
    }
    
    SelectPartitionScreen Horizontal {
        width: auto;
        height: auto;
    }
    
    SelectPartitionScreen Horizontal Button {
        margin: 2;
        width: 10;
    }
    """

    def __init__(self, partitions: list[str], selected_partitions: list[str]) -> None:
        super().__init__()
        self.partitions = partitions
        self.selected_partitions = selected_partitions

    def compose(self) -> ComposeResult:
        with Vertical():
            yield ColumnSelection(self.partitions, self.selected_partitions, id='partitions')
            with Horizontal():
                yield Button('Ok', variant='success', id='ok')
                yield Button('Cancel', variant='warning', id='cancel')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'ok':
            self.dismiss(self.result())
        else:
            self.dismiss(None)

    def action_deselect_all(self) -> None:
        self.query_one(ColumnSelection).deselect_all()

    def action_select_all(self) -> None:
        self.query_one(ColumnSelection).select_all()

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def result(self) -> list[str]:
        data: list[str] = self.query_one(ColumnSelection).selected_columns()
        return data


class DetailScreen(ModalScreen[None]):
    BINDINGS = [('escape', 'pop_screen')]

    DEFAULT_CSS = """
    DetailScreen {
        align: center middle;
        width: auto;
        height: auto;
        & > DataTable {
            width: auto;
            min-width: 50%;
            height: auto;
            background: $panel;
        }
        & > Label {
            background: $panel;
        }
    }
    """

    def __init__(self, model: Node | Queue, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.model = model
        columns = set(self.model.model_fields.keys())
        columns.update(name for name, value in vars(type(self.model)).items() if isinstance(value, property))
        self._columns = sorted(columns)

    def compose(self) -> ComposeResult:
        data_table: DataTable = DataTable(show_row_labels=False)
        data_table.add_columns('key', 'value')
        data_table.cursor_type = 'row'
        data_table.zebra_stripes = True
        data_table.border_title = 'Detailed information'
        yield data_table
        yield Label()

    def on_mount(self) -> None:
        def format_func(_value: Any, style: Style) -> Text:
            if isinstance(_value, float):
                return Text(f'{_value:.2f}', style=style, justify='left')

            return Text(str(_value), style=style, justify='left')

        data_table = self.query_one(DataTable)

        for key in sorted(self._columns):
            value = getattr(self.model, key)
            if value is None:
                continue
            data_table.add_row(key, format_value(self.model, key, _format_func=format_func))

        data_table.sort(data_table.coordinate_to_cell_key(Coordinate(0, 0)).column_key)

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    @on(DataTable.RowHighlighted)
    def row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        key = event.control.get_row_at(event.cursor_row)[0]
        self.query_one(Label).update(f'{key}: {self._get_description(key)}')

    def _get_description(self, key: str) -> str:
        default = 'No description available.'
        if key in self.model.model_fields:
            desc = self.model.model_fields[key].description
            return desc if desc is not None else default

        if key in self.model.model_computed_fields:
            desc = self.model.model_computed_fields[key].description
            return desc if desc is not None else default

        return default
