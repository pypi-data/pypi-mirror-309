import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFrame, QWidget
from PySide6.QtCore import QPropertyAnimation


def animate_frame(frame, duration=300):
    """
    从上往下展开或收起 QFrame 的动画效果。

    :param frame: 要显示的 QFrame
    :param duration: 动画持续时间（毫秒）
    """
    if frame.isVisible():
        animation = QPropertyAnimation(frame, b"maximumHeight")
        animation.setDuration(duration)
        animation.setStartValue(frame.sizeHint().height())  # 动画开始时的高度
        animation.setEndValue(0)  # 动画结束时的高度
        animation.start()
        animation.finished.connect(frame.hide)  # 动画结束后隐藏框架
    else:
        frame.setMaximumHeight(0)  # 设置初始高度为0
        frame.show()  # 显示框架
        animation = QPropertyAnimation(frame, b"maximumHeight")
        animation.setDuration(duration)
        animation.setStartValue(0)  # 动画开始时的高度
        animation.setEndValue(frame.sizeHint().height())  # 动画结束时的高度
        animation.start()  # 启动动画


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("动画测试")
        self.setGeometry(100, 100, 300, 400)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        # 创建一个按钮来触发动画
        toggle_button = QPushButton("切换菜单", self)
        toggle_button.clicked.connect(self.toggle_menu)
        layout.addWidget(toggle_button)

        # 创建一个 QFrame
        self.menu_frame = QFrame(self)
        self.menu_frame.setStyleSheet("background-color: lightgray;")
        self.menu_frame.setContentsMargins(0, 0, 0, 0)
        self.menu_frame.setMaximumHeight(0)  # 初始高度为0
        self.menu_frame.hide()  # 初始隐藏

        # 在 QFrame 中添加一些内容
        menu_layout = QVBoxLayout(self.menu_frame)
        for i in range(5):
            menu_button = QPushButton(f"菜单项 {i + 1}", self.menu_frame)
            menu_layout.addWidget(menu_button)

        layout.addWidget(self.menu_frame)

    def toggle_menu(self):
        animate_frame(self.menu_frame)  # 调用动画显示函数


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
