import re
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CalculatorWindow(QMainWindow):
    """A small calculator supporting the four basic arithmetic operations."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Calculator")
        self.setFixedSize(320, 420)
        self._build_ui()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setMinimumHeight(70)
        self.display.setStyleSheet("font-size: 28px; padding: 8px;")
        layout.addWidget(self.display)

        button_grid = QGridLayout()
        layout.addLayout(button_grid)

        buttons = [
            ("AC", 0, 0), ("⌫", 0, 1), ("±", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("−", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("%", 4, 2), ("=", 4, 3),
        ]

        for text, row, column in buttons:
            button = QPushButton(text)
            button.setMinimumHeight(55)
            button.setStyleSheet("font-size: 20px;")
            button.clicked.connect(lambda checked=False, value=text: self.handle_button(value))
            column_span = 1
            button_grid.addWidget(button, row, column, 1, column_span)

    def handle_button(self, value):
        """Update the display when a calculator button is clicked."""
        if value == "AC":
            self.display.setText("0")
        elif value == "⌫":
            self.backspace()
        elif value == "±":
            self.toggle_sign()
        elif value == "%":
            self.calculate_percentage()
        elif value == "=":
            self.calculate_result()
        else:
            self.append_value(value)

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts for the calculator."""
        key = event.key()
        text = event.text()

        if text.isdigit():
            self.append_value(text)
        elif text in {"+", "."}:
            self.append_value(text)
        elif text == "-":
            self.append_value("−")
        elif text == "*":
            self.append_value("×")
        elif text == "/":
            self.append_value("÷")
        elif text == "=":
            self.calculate_result()
        elif key in {Qt.Key.Key_Return, Qt.Key.Key_Enter}:
            self.calculate_result()
        elif key == Qt.Key.Key_Backspace:
            self.backspace()
        elif key == Qt.Key.Key_Escape:
            self.display.setText("0")
        else:
            super().keyPressEvent(event)
            return

        event.accept()

    def append_value(self, value):
        current_text = self.display.text()

        if value == ".":
            self.append_decimal(current_text)
        elif current_text == "Error" or current_text == "0":
            self.display.setText(value)
        else:
            self.display.setText(current_text + value)

    def backspace(self):
        """Remove the last entered character from the display."""
        current_text = self.display.text()
        if current_text == "Error" or len(current_text) <= 1:
            self.display.setText("0")
        else:
            self.display.setText(current_text[:-1])

    def toggle_sign(self):
        """Toggle the sign of the number currently being entered."""
        current_text = self.display.text()
        if current_text == "Error" or current_text == "0":
            self.display.setText("0")
            return

        last_operator = max(current_text.rfind(operator) for operator in "+−×÷")
        expression_start = current_text[:last_operator + 1]
        current_number = current_text[last_operator + 1:]

        if current_number.startswith("-"):
            self.display.setText(expression_start + current_number[1:])
        else:
            self.display.setText(expression_start + "-" + current_number)

    def calculate_percentage(self):
        """Convert the number currently being entered into a percentage."""
        current_text = self.display.text()
        if current_text == "Error":
            self.display.setText("0")
            return

        last_operator = max(current_text.rfind(operator) for operator in "+−×÷")
        expression_start = current_text[:last_operator + 1]
        current_number = current_text[last_operator + 1:]

        try:
            percentage = float(current_number) / 100
            self.display.setText(expression_start + str(percentage))
        except ValueError:
            self.display.setText("Error")

    def append_decimal(self, current_text):
        """Add a decimal point only when the current number does not contain one."""
        if current_text == "Error" or current_text == "0":
            self.display.setText("0.")
            return

        current_number = re.split(r"[+−×÷]", current_text)[-1]
        if "." not in current_number:
            self.display.setText(current_text + ("0." if not current_number else "."))

    def calculate_result(self):
        expression = self.display.text().replace("×", "*").replace("÷", "/").replace("−", "-")

        # Only digits, spaces and the four operators are allowed before evaluation.
        if not re.fullmatch(r"[0-9.+*/ \-]+", expression):
            self.display.setText("Error")
            return

        try:
            result = eval(expression, {"__builtins__": {}}, {})
            self.display.setText(str(result))
        except (ArithmeticError, SyntaxError):
            self.display.setText("Error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())
