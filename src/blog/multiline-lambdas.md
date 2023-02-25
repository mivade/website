---
title: Multiline lambdas
date: 2018-01-15
tags:
  - python
---

Although Python has anonymous lambda functions, they lack the flexibility that
some languages such as Javascript or even modern C++ have. In Python, lambda
functions are limited to a single statement, which is often interpreted as
meaning that it can only do one thing. This is not strictly true, however,
since constructing a tuple is considered a single statement. In other words, we
can cheat a little and call two independent functions in one lambda like this:

```python
(lambda: (foo(), bar()))()
```

This is still somewhat constraining since variables cannot be defined within
the lambda expression, so cases where this trick is useful are limited. One
instance where this is particularly nice though is when defining callbacks for
a GUI. Typically when a user clicks on a button, there might be several actions
that should be triggered, such as starting an experiment, updating a GUI label,
etc. Below is a simple
[example](https://gist.github.com/mivade/e6ec2589e7160c03951f838fe5f18dac) to
illustrate this method:

```python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Multiline lambdas')

        self.label = QLabel("Click the button")

        self.button = QPushButton("Click me!")
        self.button.clicked.connect(lambda: (
            self.button.setEnabled(False),
            self.button.setText("You clicked me!"),
            self.label.setText("Woo!")
        ))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
```
