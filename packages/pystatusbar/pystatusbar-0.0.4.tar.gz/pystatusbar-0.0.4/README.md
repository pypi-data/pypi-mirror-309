# statusbar

Python package that enables the easy creation of a statusbar. The creation of a statusbar utilizes pythons formatted strings to easily create custom bars that can be updated in an asyncronous manner. This project is designed to be lightweight and thus requires no additional packages. 

## Installation

```
python3 -m pip install pystatusbar
```

From source

```
git clone https://github.com/lukaswd/statusbar.git
cd statusbar
python3 -m pip install .
```

## Example Usage

``` python
import time

from pystatusbar import StatusBar

if __name__ == '__main__':
    format_start = " This is a test {WORD} bar with lines: {i}"
    format_end = " {time} "

    bar = StatusBar(format_start=format_start, format_end=format_end, i=0, WORD="")
    bar.start()
    for i in range(50):
        print(f"Test Line {i}")
        if i % 10 == 0:
            bar.update(i=i)

        if i == 25:
            bar.update(WORD="status")

        time.sleep(0.1)
    bar.stop()
```

The bar also works with sys.stdout.write and the python logging library