from __future__ import annotations

import enum
from typing import Any

from textual import on
from textual.app import ComposeResult, App
from textual.containers import Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Checkbox, Button, Static
from textual.widgets.selection_list import Selection


class SelectionOrderRow(Widget):
    DEFAULT_CSS = """
    SelectionOrderRow {
        height: 3;
    }
    SelectionOrderRow Checkbox {
        width: 35;
    }
    SelectionOrderRow Button {
        max-width: 5;
    }
    """

    class Direction(enum.Enum):
        UP = enum.auto()
        DOWN = enum.auto()

    class Moved(Message):
        def __init__(self, _widget: SelectionOrderRow, direction: SelectionOrderRow.Direction) -> None:
            super().__init__()
            self.direction = direction
            self.widget = _widget

        @property
        def control(self) -> SelectionOrderRow:
            return self.widget

    def __init__(self, entry: Selection, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.id = str(entry.prompt)
        self.entry = entry

    def compose(self) -> ComposeResult:
        with Horizontal(id='horizontal'):
            yield Checkbox(str(self.entry.prompt), value=self.entry.value, id=f'checkbox_{self.id}')
            yield Button('⮝', id=f'button_up_{self.id}')
            yield Button('⮟', id=f'button_down_{self.id}')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == f'button_up_{self.id}':
            direction = SelectionOrderRow.Direction.UP
        else:
            direction = SelectionOrderRow.Direction.DOWN

        self.post_message(SelectionOrderRow.Moved(self, direction))

    @property
    def selected(self) -> bool:
        return self.query_one(f'#checkbox_{self.id}', Checkbox).value

    def disable(self, direction: Direction) -> None:
        if direction == SelectionOrderRow.Direction.UP:
            button_id = f'#button_up_{self.id}'
        else:
            button_id = f'#button_down_{self.id}'

        button = self.query_one(button_id, Button)
        button.disabled = True

    def enable_all(self, enable: bool) -> None:
        self.query_one(f'#button_up_{self.id}', Button).disabled = not enable
        self.query_one(f'#button_down_{self.id}', Button).disabled = not enable


class SelectionOrderList(Static):
    def __init__(self, entries: list[Selection], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.entries = entries

    def compose(self) -> ComposeResult:
        for entry in [x for x in self.entries if x.value]:
            yield SelectionOrderRow(entry=entry)
        for entry in [x for x in self.entries if not x.value]:
            yield SelectionOrderRow(entry=entry)

    def on_mount(self) -> None:
        self._update_button_status()

    # @on(Checkbox.Changed)
    # def _row_selection_changed(self, event: Checkbox.Changed) -> None:
    #     name = event.control.label
    #     state = event.control.value
    #     for index, entry in enumerate(self.entries):
    #         if str(entry.prompt) == name:
    #             self.entries[index] = Selection(name, state)
    #             break
    #     self._update_button_status()

    def _update_button_status(self) -> None:
        return None
        # children = self.query_children(SelectionOrderRow)
        # for child in children:
        #     child.enable_all(child.selected)
        #
        # selected_children = [x for x in children if x.selected]
        # if len(selected_children) <= 1:
        #     return
        #
        # selected_children[0].disable(SelectionOrderRow.Direction.UP)
        # selected_children[len(selected_children) - 1].disable(SelectionOrderRow.Direction.DOWN)

    def _new_index(self, event: SelectionOrderRow.Moved) -> int | None:
        index = self._nodes.index(event.control)

        if event.direction == SelectionOrderRow.Direction.UP:
            if index != 0:
                return index - 1
        else:
            if index != len(self.entries) - 1:
                return index + 1

        return None

    @on(SelectionOrderRow.Moved)
    def row_moved(self, event: SelectionOrderRow.Moved) -> None:
        assert event.control
        assert isinstance(event.control, SelectionOrderRow)
        widget: SelectionOrderRow = event.control

        new_index = self._new_index(event)
        if new_index is None:
            return

        # noinspection PyProtectedMember
        self._nodes._remove(widget)  # pylint: disable=protected-access
        # noinspection PyProtectedMember
        #self._nodes._insert(new_index, widget)  # pylint: disable=protected-access
        self._update_button_status()
        self.refresh(layout=True)

    def selected(self) -> list[Selection]:
        rows = self.query(SelectionOrderRow)
        return [row.entry for row in rows]


class TestApp(App):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.entries = [Selection('node_name', True),
                        Selection('status', False),
                        Selection('partitions', True),
                        Selection('test_1', True),
                        Selection('test_2', False),
                        Selection('test_3', True),
                        Selection('sockets', False)]

    def compose(self) -> ComposeResult:
        yield SelectionOrderList(self.entries)


if __name__ == "__main__":
    TestApp().run()
