"""An offline stopwatch application using only the Python standard library."""

from __future__ import annotations

import time
import tkinter as tk
from collections.abc import Callable
from datetime import datetime


class Stopwatch:
    """Track elapsed time while supporting pause and reset operations."""

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._elapsed = 0.0
        self._started_at: float | None = None

    @property
    def running(self) -> bool:
        return self._started_at is not None

    @property
    def elapsed(self) -> float:
        if self._started_at is None:
            return self._elapsed
        return self._elapsed + self._clock() - self._started_at

    def start(self) -> None:
        if not self.running:
            self._started_at = self._clock()

    def pause(self) -> None:
        if self._started_at is not None:
            self._elapsed += self._clock() - self._started_at
            self._started_at = None

    def reset(self) -> None:
        self._elapsed = 0.0
        self._started_at = self._clock() if self.running else None


def format_elapsed(seconds: float) -> str:
    """Format seconds as HH:MM:SS.cc."""
    centiseconds = max(0, int(seconds * 100))
    hours, remainder = divmod(centiseconds, 360_000)
    minutes, remainder = divmod(remainder, 6_000)
    whole_seconds, fraction = divmod(remainder, 100)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d}.{fraction:02d}"


def format_current_time(moment: datetime) -> str:
    """Format a local date and time for display."""
    return moment.strftime("%Y-%m-%d %H:%M:%S")


class StopwatchApp:
    """Display the local time and control a Stopwatch in a Tkinter window."""

    UPDATE_INTERVAL_MS = 10

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.stopwatch = Stopwatch()
        self.current_time_text = tk.StringVar()
        self.time_text = tk.StringVar(value=format_elapsed(0))
        self.toggle_text = tk.StringVar(value="시작")

        root.title("스톱워치")
        root.resizable(False, False)
        root.configure(padx=24, pady=20)

        tk.Label(root, text="현재 시간", font=("맑은 고딕", 11)).grid(
            row=0, column=0, columnspan=2
        )
        tk.Label(
            root,
            textvariable=self.current_time_text,
            font=("Consolas", 16),
        ).grid(row=1, column=0, columnspan=2, pady=(2, 18))

        tk.Label(root, text="스톱워치", font=("맑은 고딕", 11)).grid(
            row=2, column=0, columnspan=2
        )
        tk.Label(
            root,
            textvariable=self.time_text,
            font=("Consolas", 32, "bold"),
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=(2, 18))

        tk.Button(
            root,
            textvariable=self.toggle_text,
            command=self.toggle,
            width=10,
        ).grid(row=4, column=0, padx=5)
        tk.Button(root, text="초기화", command=self.reset, width=10).grid(
            row=4, column=1, padx=5
        )

        root.bind("<space>", lambda _event: self.toggle())
        root.bind("r", lambda _event: self.reset())
        self._refresh()

    def toggle(self) -> None:
        if self.stopwatch.running:
            self.stopwatch.pause()
            self.toggle_text.set("계속")
        else:
            self.stopwatch.start()
            self.toggle_text.set("일시정지")

    def reset(self) -> None:
        self.stopwatch.reset()
        self.time_text.set(format_elapsed(0))

    def _refresh(self) -> None:
        self.current_time_text.set(format_current_time(datetime.now()))
        self.time_text.set(format_elapsed(self.stopwatch.elapsed))
        self.root.after(self.UPDATE_INTERVAL_MS, self._refresh)


def main() -> None:
    root = tk.Tk()
    StopwatchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()