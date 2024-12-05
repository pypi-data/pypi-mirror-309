from enum import Enum, auto
from typing import overload, Optional
from os import system
import os
from abc import ABC, abstractmethod
import time
import sys
import threading

# Importul corect al modulului keydetection
from . import keydetection as kd

class MenuState(Enum):
    toRender = auto()
    rendered = auto()
    hidden = auto()

def _filter(options: dict[int, str], query: str) -> dict[int, str]:
    final = {}
    for i, name in options.items():
        if str(i).startswith(query) or name.startswith(query):
            final[i] = name
    if len(list(final.keys())) == 0:
        for i, name in options.items():
            if str(i).startswith(query) or query in name:
                final[i] = name

    return final

class CustomMenu(ABC):
    @abstractmethod
    def __init__(self, options: list[str]):
        ...

    @abstractmethod
    def render(self):
        ...

class Menu(CustomMenu):
    def __init__(self, options: list[str] | dict[int, str], /, backspace_allowed: bool = True, cancellable: bool = False):
        self.backspace_allowed = backspace_allowed
        self.cancellable = cancellable
        if isinstance(options, list):
            self.options: dict[int, str] = dict(enumerate(options))
        else:
            self.options: dict[int, str] = options

        self.state = MenuState.hidden
        self.__previous_query = None
        self.query = ""

    def _render(self, query: str) -> list[tuple[int, str]]:
        # Render the menu and filter options based on the query
        if not self.__previous_query and self.state == MenuState.rendered:
            return list(self.options.items())
        if self.state == MenuState.rendered:
            if query == self.__previous_query:
                return list(self.options.items())

        # Update the previous query and change the state
        self.__previous_query = query
        self.state = MenuState.rendered

        # Filter the options based on the query
        search_results = list(self._filter(self.options, query).items())

        # Display the search results
        system("cls || clear")
        for i, n in search_results:
            print(f"{i}. {n}")

        return search_results

    def render_loop(self):
        while self.state != MenuState.hidden:
            system("cls || clear")  # Clear the console output (cross-platform)
            time.sleep(0.005)
            options = self._render(self.query)
            # Display the filtered options
            for i, n in options:
                print(f"{i}. {n}")

            # Display the current query prompt correctly (without repeating)
            print(f"> {self.query}", end="")
            sys.stdout.flush()
            time.sleep(0.5)
        print('\n', end = '', flush = True)
        sys.stdout.flush()
        time.sleep(0.01)

    def render(self) -> Optional[tuple[int, str]]:
        if self.state == MenuState.hidden:
            self.state = MenuState.toRender

        query: str = ""
        last_pressed_key: str = ""

        thread = threading.Thread(target=self.render_loop)
        thread.start()

        while True:
            self.query = query
            options = list(self._filter(self.options, query).items())
            # Update the query based on the pressed key
            if kd.current_allowed_key:
                if kd.current_allowed_key != last_pressed_key:
                    last_pressed_key = kd.current_allowed_key
                    if last_pressed_key != "space":
                        query += last_pressed_key
                    else:
                        query += " "
                    kd.current_allowed_key = ""  # Reset current allowed key

            elif kd.current_key == "backspace" and self.backspace_allowed:
                if query:
                    query = query[:-1]  # Remove the last character
                kd.current_key = ""  # Reset backspace key after it's pressed

            elif kd.current_key == "enter":
                if options:
                    self.state = MenuState.hidden
                    sys.stdin.flush()
                    thread.join()
                    return options[0]  # Return the first option if "enter" is pressed
                kd.current_key = ""  # Reset the enter key after it's pressed

            elif kd.current_key == "esc" and self.cancellable:
                self.state = MenuState.hidden
                sys.stdin.flush()
                thread.join()
                return None  # Return None if "esc" is pressed for cancellation

            # Clear the current query line before printing the new one

    @staticmethod
    def _filter(options: dict[int, str], query: str) -> dict[int, str]:
        """Filter the options based on the query."""
        return {k: v for k, v in options.items() if
                str(k).lower().startswith(query.lower()) or v.lower().startswith(query.lower())}
