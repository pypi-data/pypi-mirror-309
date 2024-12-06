from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Callable

from textual import on
from textual.binding import Binding
from textual.widgets import DataTable
from textual.widgets.data_table import Column, ColumnKey, CellKey
from typing_extensions import Self

SORT_INDICATOR_UP: Final[str] = ' \u25b4'
SORT_INDICATOR_DOWN: Final[str] = ' \u25be'


@dataclass
class Sort:
    key: ColumnKey | None = None
    label: str = ''
    direction: bool = False

    def reverse(self) -> None:
        self.direction = not self.direction

    @property
    def indicator(self) -> str:
        return SORT_INDICATOR_UP if self.direction else SORT_INDICATOR_DOWN


class SortableDataTable(DataTable):
    DEFAULT_CSS = """
    SortableDataTable {
        height: 1fr;
        border: $foreground 80%;
    }
    """

    BINDINGS = [
        Binding('z', 'toggle_zebra', 'Toggle Zebra', show=False)
    ]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._sort = Sort()
        self.cursor_type = 'row'  # type: ignore
        self.show_row_labels = False
        self.sort_function: Callable[[Any], Any] | None = None

    def clear(self, columns: bool = False) -> Self:
        super().clear(columns)
        # _sort contains a column key that becomes invalid when clearing the columns, so reset it.
        self._sort = Sort()
        return self

    def column_names(self) -> list[Column]:
        data = self.columns.copy()
        if self._sort.key:
            column = data[self._sort.key]
            column.label.remove_suffix(self._sort.indicator)

        return list(data.values())

    @on(DataTable.HeaderSelected)
    def header_clicked(self, header: DataTable.HeaderSelected) -> None:
        if self._sort.key is not None:
            column = self.columns[self._sort.key]
            column.label.remove_suffix(self._sort.indicator)
            self._update_column_width(self._sort.key)

        sort_value = Sort(key=header.column_key)
        if self._sort.key == sort_value.key:
            sort_value = self._sort
            sort_value.reverse()

        assert sort_value.key
        self.columns[header.column_key].label += sort_value.indicator
        self._update_column_width(header.column_key)

        try:
            self.sort(sort_value.key, reverse=sort_value.direction, key=self.sort_function)
            self._sort = sort_value
        except TypeError:
            self.columns[header.column_key].label.remove_suffix(self._sort.indicator)
            print(f'Error sorting on column: {sort_value.key.value}')

    def _update_column_width(self, key: ColumnKey) -> None:
        self._update_column_widths({CellKey(row_key=next(iter(self.rows)), column_key=key)})

    def action_toggle_zebra(self) -> None:
        self.zebra_stripes = not self.zebra_stripes
