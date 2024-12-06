import sys
import time
import shutil
import threading

import _string

class StatusBar:
    def __init__(self, format_start: str, format_end: str, allow_threading: bool = False, **kwargs) -> None:
        # This has to be at the front to avoid AttributeError when calling __del__
        self._allow_threading = allow_threading
        if self._allow_threading and not self._has_time:
            self._allow_threading = False

        self._format_start = format_start
        self._format_end = format_end

        fields = self._get_fields(format_start) + self._get_fields(format_end)
            
        missing_kwargs = [field for field in fields if field != "time" and field not in kwargs and field != None]
        if missing_kwargs:
            raise ValueError(f"Missing fields in kwargs: {', '.join(missing_kwargs)}")
        
        missing_format = [field for field in kwargs.keys() if field not in fields]
        if missing_format:
            raise ValueError(f"Missing fields in format: {', '.join(missing_format)}")

        self._fields = kwargs
        self._has_time = "time" in fields

        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._lock = False

        self._new_line = False

    def _get_fields(self, format):
        return [field_name for _, field_name, _, _ in _string.formatter_parser(format)]
    
    def _worker(self):
        self._thread_interrupt = False

        last = self._start_time
        while not self._thread_interrupt:
            if time.time() - last >= 1:
                self.update()
                time.sleep(0.1)
                last = time.time()
    
    def update(self, **kwargs) -> None:
        self._fields.update(kwargs)

        while self._lock:
            time.sleep(0.000001)

        self._lock = True

        # Set cursor to the beginning of the line and delete the current line 
        self._original_stdout.write(f"\r\x1b[2K")

        self._print_status_bar(new_line=False)
        self._lock = False

    def start(self) -> None:
        self._start_time = time.time()
        sys.stdout = self
        sys.stderr = self

        # Save current position
        self._original_stdout.write(f"\x1b7")

        self._print_status_bar(new_line=False)

        if self._allow_threading:
            self._thread = threading.Thread(target=self._worker)
            self._thread.start()

    def stop(self)  -> None:
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

    def write(self, text):
        if text == "\n" and not self._new_line:
            self._new_line = True
            return

        while self._lock:
            time.sleep(0.000001)

        self._lock = True

        # Set cursor to the beginning of the line and delete the current line
        self._original_stdout.write(f"\r\x1b[2K")
        # Restore position
        self._original_stdout.write(f"\x1b8")
        # Erase from cursor to end of line
        self._original_stdout.write(f"\x1b[0K")

        # Write the new line if needed
        if self._new_line:
            self._original_stdout.write("\n")
            # Reset new line
            self._new_line = False
        
        # Write the text
        self._original_stdout.write(text)
        # Save current position
        self._original_stdout.write(f"\x1b7")

        self._print_status_bar()

        self._lock = False

    def flush(self):
        self._original_stdout.flush()
        self._original_stderr.flush()

    def fileno(self):
        return self.original_stdout.fileno()

    def _print_status_bar(self, new_line=True):
        terminal_width = shutil.get_terminal_size().columns

        if self._has_time:
            minutes, seconds = divmod(time.time() - self._start_time, 60)
            hours, minutes = divmod(minutes, 60)
            
            if hours > 0:
                self._fields["time"] = f"{hours:02}:{minutes:02}:{seconds:02.1f}"
            elif minutes > 0:
                self._fields["time"] = f"{minutes:02}:{seconds:02.1f}"
            else:
                self._fields["time"] = f"{seconds:02.1f}s"

        space_width = terminal_width - len((self._format_start + self._format_end).format(**self._fields))
        self._original_stdout.write((("\n" if new_line else "")  + self._format_start + " " * (space_width if space_width > -1 else 0) + self._format_end).format(**self._fields))
        self.flush()

    def __del__(self):
        if self._allow_threading:
            self._thread_interrupt = True
            self._thread.join()