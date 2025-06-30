# Feuille de style Qt pour J.A.R.V.I.S.
STYLE = """
QMainWindow {
    background-color: #2C3E50;
    color: #ecf0f1;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
}

QLabel {
    color: #ecf0f1;
    font-weight: bold;
}

QPushButton {
    background-color: #3498DB;
    border-radius: 5px;
    padding: 8px;
    color: white;
}

QPushButton:hover {
    background-color: #2980B9;
}

QTextEdit {
    background-color: #34495E;
    border: 1px solid #2980B9;
    color: #ecf0f1;
    padding: 5px;
    border-radius: 5px;
}

QScrollBar:vertical {
    background: #2C3E50;
    width: 12px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: #3498DB;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}
"""
