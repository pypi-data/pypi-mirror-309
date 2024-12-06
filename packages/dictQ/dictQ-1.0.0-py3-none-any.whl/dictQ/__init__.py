# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.dev@gmail.com>


"""Sophisticate Searching Algorithms"""


from time import sleep
from inspect import stack
from os.path import abspath
from pyfiglet import figlet_format
from fileinput import input as inpt
from pynput.keyboard import Key, Listener
from typing import Iterable, NoReturn, Self, List, Any
from hashtbl import tabulate, hashMap, _red, _green, _blue, _cyan, _white


__all__: List = ["searchVisualizer", "NotSortedError"]


class NotSortedError(Exception):
    pass


class searchVisualizer:
    def __init__(
        self: "searchVisualizer",
        data: Iterable,
        *,
        item: Any,
        speed: int = 1,
        control: bool = False,
        page_control: bool = False,
    ) -> None:
        self.data: List[Any] = data
        self.speed: int = speed
        self.item: Any = item
        if (control and page_control) or (not control and page_control):
            self.control: bool = False
            self.page_control: bool = page_control
            self.running: None = None
            self.keyboard_listener: None = None
        else:
            self.control: bool = control
            self.page_control: bool = page_control

    @property
    def data(self: "searchVisualizer") -> Self:
        return self

    @data.setter
    def data(self: "searchVisualizer", data: Iterable) -> None | NoReturn:
        try:
            self._data: List[Any] = list(data)
        except TypeError as e0:
            raise ValueError("Invalid data type !") from None

    @data.deleter
    def data(self: "searchVisualizer") -> NoReturn:
        raise ValueError("read-only")

    @property
    def speed(self: "searchVisualizer") -> int:
        return self._speed

    @speed.setter
    def speed(self: "searchVisualizer", speed: int) -> None | NoReturn:
        if speed < 1:
            raise ValueError("The speed must be greater than zero !")
        self._speed: int = speed

    @speed.deleter
    def speed(self: "searchVisualizer") -> NoReturn:
        raise ValueError("read-only")

    def on_press(self: "searchVisualizer", key: Any) -> bool | None:
        if key == Key.page_down:
            self.running: bool = False
            return False
        elif key == Key.page_up:
            self.running: bool = False
            self.page_control: bool = False
            return False

    def linear_search(self: "searchVisualizer") -> int | None:
        try:
            output: List[List[str]] = [
                [_blue(self._data[i]) for i in range(len(self._data))]
            ]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            print(_white("Item :"), _cyan(f"{self.item!r}"))
            print(_white("Current item :"), _cyan("?"))
            if self.control:
                while True:
                    try:
                        response: str = input(
                            _cyan(
                                "Press Enter to continue, Ctrl + D to exit control mode, or Ctrl + C to exit the program...\n"
                            )
                        )
                    except EOFError as e1:
                        self.control: bool = False
                        break
                    if not response:
                        break
            elif self.page_control:
                self.running: bool = True
                self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                self.keyboard_listener.start()
                print(
                    _cyan(
                        "Press Page Down to continue, Page Up to exit page control mode, or Ctrl + C to exit the program..."
                    )
                )
                while self.running:
                    pass
            else:
                sleep(self._speed)
            for i in range(len(self._data)):
                output[0][i] = _green(self._data[i])
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                print(_white("Item :"), _cyan(f"{self.item!r}"))
                print(_white("Current item :"), _cyan(f"{self._data[i]}"))
                if self.control:
                    while True:
                        try:
                            response: str = input()
                        except EOFError as e2:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
                if self._data[i] == self.item:
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    print(_white("Item :"), _cyan(f"{self.item!r}"))
                    print(_white("Current item :"), _cyan(f"{self._data[i]}"))
                    print(
                        _white("Found after"),
                        _cyan(f"{i}"),
                        _white("steps" if (i) > 1 else "step"),
                    )
                    break
                output[0][i] = _blue(self._data[i])
            else:
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                print(_white("Not found !"))
                return
            return i
        except KeyboardInterrupt as e3:
            print(_cyan("\nI hope you enjoyed learning :)"))

    def binary_search(self: "searchVisualizer") -> int | None | NoReturn:
        try:
            low: int = 0
            high: int = len(self._data) - 1
            try:
                sorted_data: List[Any] = sorted(self._data)
            except TypeError as e4:
                raise TypeError("Invalid list !") from None
            else:
                if sorted_data != self._data:
                    sorted_data.reverse()
                    if sorted_data != self._data:
                        raise NotSortedError("This list is not sorted !")
                    else:
                        reverse: bool = True
                else:
                    reverse: bool = False
            output: List[List[str]] = [
                [_blue(self._data[i]) for i in range(len(self._data))]
            ]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            print(_white("Item :"), _cyan(f"{self.item}"))
            print(_white("Current item :"), _cyan("?"))
            if self.control:
                while True:
                    try:
                        response: str = input(
                            _cyan(
                                "Press Enter to continue, Ctrl + D to exit control mode, or Ctrl + C to exit the program...\n"
                            )
                        )
                    except EOFError as e5:
                        self.control: bool = False
                        break
                    if not response:
                        break
            elif self.page_control:
                self.running: bool = True
                self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                self.keyboard_listener.start()
                print(
                    _cyan(
                        "Press Page Down to continue, Page Up to exit page control mode, or Ctrl + C to exit the program..."
                    )
                )
                while self.running:
                    pass
            else:
                sleep(self._speed)
            counter: int = 0
            while low <= high:
                mid: int = (low + high) // 2
                if low != high:
                    if low != mid:
                        output[0][low] = _red(self._data[low])
                    if high != mid:
                        output[0][high] = _red(self._data[high])
                output[0][mid] = _green(self._data[mid])
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                print(_white("Item :"), _cyan(f"{self.item}"))
                print(_white("Current item :"), _cyan(f"{self._data[mid]}"))
                if self.control:
                    while True:
                        try:
                            response: str = input()
                        except EOFError as e6:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
                if self._data[mid] < self.item:
                    if not reverse:
                        output[0][low] = _blue(self._data[low])
                        low: int = mid + 1
                    else:
                        output[0][high] = _blue(self._data[high])
                        high: int = mid - 1
                elif self._data[mid] > self.item:
                    if not reverse:
                        output[0][high] = _blue(self._data[high])
                        high: int = mid - 1
                    else:
                        output[0][low] = _blue(self._data[low])
                        low: int = mid + 1
                else:
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    print(_white("Item :"), _cyan(f"{self.item}"))
                    print(_white("Current item :"), _cyan(f"{self._data[mid]}"))
                    print(
                        _white("Found after"),
                        _cyan(f"{counter}"),
                        _white("steps" if (counter) > 1 else "step"),
                    )
                    break
                output[0][mid] = _blue(self._data[mid])
                counter += 1
            else:
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                print(_white("Not found !"))
                return
            return mid
        except KeyboardInterrupt as e7:
            print(_cyan("\nI hope you enjoyed learning :)"))


def interact(line_number: int, data: Any) -> None:
    """
    This is an Easter egg function.

    Interactively modifies a line in a file with the provided data.

    This function is designed to work with inline built-in Python data structures, such as variables, lists, dictionaries, and tuples. It does not support more complex data structures like those found in external libraries (e.g. NumPy arrays).

    Parameters:
    line_number (int): The line number in the file to modify, starting from 1.
    data (Any): The data to insert on the specified line. This can be any Python object that can be easily converted to a string.

    Example:
    ```python
    x = 5
    y = 6
    z = x + y
    interact(z_line_number, z)
    ```

    In the above example, the function will locate the line where the variable `z` is defined, and replace the right-hand side of the assignment with the current value of `z` (which is 11 after the computation).

    The function works by:
    1. Retrieving the caller's frame information to determine the file path and line number where `interact()` was called.
    2. Opening the file in-place and iterating through the lines.
    3. When the target line number is reached, the function replaces the right-hand side of the assignment with the provided `data` value.
    4. All other lines are printed without modification.

    This allows you to quickly update inline variable assignments in your code without manually editing the file.
    """
    caller_frame: stack = stack()[1]
    caller_path: abspath = abspath(caller_frame.filename)
    with inpt(caller_path, inplace=True) as file:
        for i, line in enumerate(file, start=1):
            if i == line_number:
                output: List = []
                for j in line:
                    if j == "=":
                        output.append("= ")
                        output.append(f"{data!r}")
                        break
                    output.append(j)
                print("".join(output))
            else:
                print(line.rstrip())


def _main() -> None:
    color_functions: hashMap = hashMap(
        [
            ["red", _red],
            ["green", _green],
            ["cyan", _cyan],
            ["blue", _blue],
            ["white", _white],
        ]
    )
    characters: List[str] = ["d", "i", "c", "t", "Q"]
    colors: List[str] = ["blue", "cyan", "green", "red", "white"]
    lines: List[List[str]] = [figlet_format(char).splitlines() for char in characters]
    max_lines: int = max(len(l) for l in lines)
    lines: List[List[str]] = [l + [""] * (max_lines - len(l)) for l in lines]
    for i in range(max_lines):
        for j, color in enumerate(colors):
            print(color_functions[color](lines[j][i]), end="")
        print()


if __name__ == "__main__":
    _main()
