# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from mango_ui.init import *
from mango_ui.models.models import LeftMenuModel
from .mango_div import MangoDiv
from .mango_menu_button import MangoMenuButton


class MangoMenu(QWidget):
    clicked = Signal(object)
    released = Signal(object)

    def __init__(
            self,
            parent=None,
            app_parent=None,
            duration_time=500,
            minimum_width=50,
            maximum_width=180,
            icon_path=":/icons/menu.svg",
            icon_path_close=":/icons/icon_menu_close.svg",
            toggle_text="展开",
            toggle_tooltip="展开菜单"
    ):
        super().__init__()
        self.duration_time = duration_time
        self.minimum_width = minimum_width
        self.maximum_width = maximum_width
        self.setMinimumWidth(self.minimum_width)
        self.icon_path = icon_path
        self.icon_path_close = icon_path_close
        self.parent = parent
        self._app_parent = app_parent

        self.left_menu_layout = QVBoxLayout(self)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)

        # 全局
        self.bg = QFrame()
        self.left_menu_layout.addWidget(self.bg)
        self.bg.setStyleSheet(f"background: {THEME.color.color4}; border-radius: {THEME.border_radius};")
        self._layout = QVBoxLayout(self.bg)
        self._layout.setContentsMargins(0, 0, 0, 0)

        # 上面
        self.top_frame = QFrame()
        self.top_layout = QVBoxLayout(self.top_frame)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(1)

        # 下面
        self.bottom_frame = QFrame()
        self.bottom_layout = QVBoxLayout(self.bottom_frame)
        self.bottom_layout.setContentsMargins(0, 0, 0, 8)
        self.bottom_layout.setSpacing(1)

        self._layout.addWidget(self.top_frame, 0, Qt.AlignTop)  # type: ignore
        self._layout.addWidget(self.bottom_frame, 0, Qt.AlignBottom)  # type: ignore

        self.toggle_button = MangoMenuButton(
            app_parent,
            text=toggle_text,
            tooltip_text=toggle_tooltip,
            icon_path=icon_path
        )
        self.toggle_button.clicked.connect(lambda: self.toggle_animation(True))
        self.top_layout.addWidget(self.toggle_button)

        self.div_top = MangoDiv(THEME.color.color4)
        self.top_layout.addWidget(self.div_top)

        self.div_bottom = MangoDiv(THEME.color.color4)
        self.div_bottom.hide()
        self.bottom_layout.addWidget(self.div_bottom)
        self.list_button_frame = []

    def add_menus(self, menu_model: list[LeftMenuModel]):
        for menu_obj in menu_model:
            layout = QVBoxLayout()
            self.menu = MangoMenuButton(
                self._app_parent,
                text=menu_obj.btn_text,
                btn_id=menu_obj.btn_id,
                tooltip_text=menu_obj.btn_tooltip,
                icon_path=menu_obj.btn_icon,
                is_active=menu_obj.is_active,
                url=menu_obj.url
            )
            self.menu.clicked.connect(self.btn_clicked)
            self.menu.released.connect(self.btn_released)
            layout.addWidget(self.menu)

            if menu_obj.submenus:
                button_frame = QFrame()
                button_frame.setStyleSheet("QFrame { border: none; }")
                button_frame.setContentsMargins(0, 0, 0, 0)
                button_frame.hide()
                self.list_button_frame.append({
                    'parent_btn_id': menu_obj.btn_id,
                    'frame_object': button_frame,
                    'btn_id_list': [menu.btn_id for menu in menu_obj.submenus]
                })
                v_layout = QVBoxLayout(button_frame)
                v_layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0
                v_layout.setStretch(0, 7)
                for menu in menu_obj.submenus:
                    frame_layout = QHBoxLayout()
                    but = MangoMenuButton(
                        self._app_parent,
                        text=menu.btn_text,
                        btn_id=menu.btn_id,
                        tooltip_text=menu.btn_tooltip,
                        icon_path=menu.btn_icon,
                        is_active=menu.is_active,
                    )
                    frame_layout.addWidget(but)
                    v_layout.addLayout(frame_layout)
                    but.clicked.connect(self.btn_clicked)
                    but.released.connect(self.btn_released)
                layout.addWidget(button_frame)
            if menu_obj.show_top:
                self.top_layout.addLayout(layout)
            else:
                self.div_bottom.show()
                self.bottom_layout.addLayout(layout)

    def btn_clicked(self, ):
        self.clicked.emit(self.menu)

    def btn_released(self):
        self.released.emit(self.menu)

    def toggle_animation(self, is_collect=True):
        self.animation = QPropertyAnimation(self.parent, b"minimumWidth")
        self.animation.stop()
        if self.width() == self.minimum_width:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self.maximum_width)
            self.toggle_button.set_active_toggle(True)
            self.toggle_button.set_icon(self.icon_path_close)
        elif is_collect:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self.minimum_width)
            self.toggle_button.set_active_toggle(False)
            self.toggle_button.set_icon(self.icon_path)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)  # type: ignore
        self.animation.setDuration(self.duration_time)
        self.animation.start()

    def select_only_one(self, widget: str):
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active(True)
            else:
                btn.set_active(False)

    def select_only_one_tab(self, widget: str):
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active_tab(True)
            else:
                btn.set_active_tab(False)

    def deselect_all(self):
        for btn in self.findChildren(QPushButton):
            btn.set_active(False)

    def deselect_all_tab(self):
        for btn in self.findChildren(QPushButton):
            btn.set_active_tab(False)
