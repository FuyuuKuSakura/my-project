import os
import sys
import pandas as pd
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QFileDialog, QTableWidget, 
                               QTableWidgetItem, QLabel, QSplitter, QFrame, QMessageBox, QGridLayout, QLineEdit, QStackedWidget, QDialog, QComboBox)
from PySide6.QtCore import  Qt, QTimer, QTime, QDate, QUrl, QSize
from PySide6.QtGui import QFont, QColor, QPalette, QBrush, QPixmap, QKeySequence, QDesktopServices, QAction, QShortcut, QIcon, QPainter, QPen

class SidebarButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setup_style()
    def setup_style(self):
        # Set fixed height as 50 pixels
        self.setFixedHeight(50)
        # Set style of siderbar button (light pink theme)
        button_style = """
        QPushButton {
            background: rgba(255, 240, 245, 0.7);
            border: 1.5px solid rgba(232,163,174, 0.4);
            border-radius: 10px;
            padding: 10px 20px;
            color: #c2185b;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: rgba(255, 228, 235, 0.95);
            border: 1.5px solid rgba(255, 105, 180, 0.7);
            color: #ad1457;
        }
        """
        self.setStyleSheet(button_style)

class AppButton(QWidget):
    def __init__(self, name, icon_path):
        super().__init__()
        self.name = name
        self.icon_path = icon_path
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # 居中对齐
        layout.setSpacing(8)  # 图标和文字之间的间距
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 图标按钮
        self.icon_btn = QPushButton()
        self.icon_btn.setFixedSize(76, 76)
        self.icon_btn.setIcon(QIcon(self.icon_path))
        self.icon_btn.setIconSize(QSize(70, 70))
        self.icon_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 240, 245, 0.7);
                border: 2px solid rgba(232, 163, 174, 0.4);
                border-radius: 20px;
            }
            QPushButton:hover {
                background: rgba(255, 228, 235, 0.95);
                border: 2px solid rgba(255, 105, 180, 0.7);
            }
        """)
        
        # 应用名称标签
        self.name_label = QLabel(self.name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("""
            QLabel {
                color: #c2185b;
                font-weight: bold;
                font-size: 12px;
                background: transparent;
                padding: 2px;
            }
        """)
        self.name_label.setFixedWidth(76)  # 固定宽度确保文字居中
        
        layout.addWidget(self.icon_btn)
        layout.addWidget(self.name_label)
        
        self.setFixedSize(120, 120)  # 固定整个应用按钮的大小
        self.setWindowOpacity(0.6)

    def set_click_handler(self, handler):
        """设置点击事件处理器"""
        self.icon_btn.clicked.connect(handler)

class MikiLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        
        # 设置固定样式
        self.setFixedStyle()
        
        # 设置固定位置和宽度
        self.setFixedPositionAndWidth()
        
        # 确保文本自动换行
        self.setWordWrap(True)
        
        # 设置对齐方式
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
    def setFixedStyle(self):
        """设置固定的样式"""
        self.setStyleSheet("""
            MikiLabel {
                background-color: rgba(255, 240, 245, 0.9);
                color: black;
                border: 4px solid rgba(244, 229, 134, 1);
                border-radius: 20px;
                padding: 10px;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
                font-size: 13px;
            }
        """)
        
    def setFixedPositionAndWidth(self):
        """设置固定位置和宽度"""
        # 固定位置坐标 (x, y)
        self.fixed_x = 240
        self.fixed_y = 400
        
        # 固定宽度
        self.fixed_width = 335
        
        # 应用位置和宽度
        self.setGeometry(self.fixed_x, self.fixed_y, self.fixed_width, 0)
        
    def setText(self, text):
        """重写setText方法，自动调整高度"""
        super().setText(text)
        self.adjustHeight()
        
    def adjustHeight(self):
        """根据文本内容自动调整高度"""
        # 计算理想的高度
        document = self.document()
        if document:
            ideal_height = document.size().height() + 35  # 加上padding
            self.setFixedHeight(int(ideal_height))
        else:
            # 备用方法：根据行数估算高度
            text_height = self.fontMetrics().height()
            line_count = self.text().count('\n') + 1
            estimated_height = text_height * line_count + 35
            self.setFixedHeight(estimated_height)

    def document(self):
        """获取文档对象用于计算高度"""
        try:
            return self.document()
        except:
            return None
    
    def showEvent(self, event):
        """显示事件，确保位置正确"""
        super().showEvent(event)
        self.move(self.fixed_x, self.fixed_y)
        self.setFixedWidth(self.fixed_width)
        self.adjustHeight()
        
    def updatePosition(self, x=None, y=None):
        """更新固定位置"""
        if x is not None:
            self.fixed_x = x
        if y is not None:
            self.fixed_y = y
        self.move(self.fixed_x, self.fixed_y)
        
    def updateWidth(self, width):
        """更新固定宽度"""
        self.fixed_width = width
        self.setFixedWidth(self.fixed_width)
        self.adjustHeight()

class TodoButton(QPushButton):
    def __init__(self, text='', color_code=0, parent=None):
        super().__init__(text, parent)  # 修正：移除color_code参数
        self.setFixedStyle(color_code)  # 修正：传递color_code参数
        self.setFixedSize(135, 65)
    
    def setFixedStyle(self, color_code):
        colorlist = ["yellow", "green", "blue", "white"]
        color = colorlist[color_code % 4]
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: black;
                border-radius: 20px;
                padding: 10px;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
                font-size: 13px;
            }}
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.app_buttons_visible = True  # 初始状态为显示
        self.app_buttons = []  # 存储所有应用按钮的引用
        self.current_page = "apps"  # 当前显示的页面
        self.setup_ui()
        self.todo_list = []
        self.todo_list_button = []
    
    def setup_ui(self):
        self.setWindowTitle("Home Page v0.6")
        self.setGeometry(100, 100, 1200, 700)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧边栏
        left_widget = self.create_sidebar()
        
        # 右侧内容区域 - 使用堆叠窗口
        self.right_container = QStackedWidget()
        self.right_container.setStyleSheet("""
            QStackedWidget {
                background: rgba(255,255,255,0.1)
            }
        """)
        
        self.miki_label = MikiLabel("MIKIMIKI成功将页面打开了なの", self)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_label)
        self.timer.start(5000) 

        # 预加载所有页面
        self.apps_page = self.create_apps_page()
        self.random_page = self.create_random_page()
        self.todo_page = self.create_todo_page()
        self.memo_page = self.create_memo_page()
        self.settings_page = self.create_settings_page()
        self.info_page = self.create_info_page()
        
        # 添加到堆叠窗口
        self.right_container.addWidget(self.apps_page)
        self.right_container.addWidget(self.random_page)
        self.right_container.addWidget(self.todo_page)
        self.right_container.addWidget(self.memo_page)
        self.right_container.addWidget(self.settings_page)
        self.right_container.addWidget(self.info_page)
        
        # 初始显示应用页面
        self.right_container.setCurrentWidget(self.apps_page)
        
        # 添加到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(self.right_container)
        
        # 设置分割比例
        splitter.setSizes([200, 800])
        splitter.setHandleWidth(2)
        
        main_layout.addWidget(splitter)

        self.setupBackground()

        self.shortcut_display_app = QShortcut(QKeySequence("Ctrl+A"), self)
        self.shortcut_display_app.activated.connect(self.toggle_app_buttons)
        
        # 设置快捷键 Ctrl+S 关闭应用按钮
        self.shortcut_shut_app = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_shut_app.activated.connect(self.hide_app_buttons)

    def hide_label(self):
        self.miki_label.hide()

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.3)
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)
        
        self.btn_app = SidebarButton("App")
        self.btn_app.clicked.connect(lambda: self.switch_page("apps"))
        
        self.btn_random = SidebarButton("Random")
        self.btn_random.clicked.connect(lambda: self.switch_page("random"))
        
        self.btn_todo = SidebarButton("To-do")
        self.btn_todo.clicked.connect(lambda: self.switch_page("todo"))
        
        self.btn_memo = SidebarButton("Memo")
        self.btn_memo.clicked.connect(lambda: self.switch_page("memo"))
        
        self.btn_settings = SidebarButton("Settings")
        self.btn_settings.clicked.connect(lambda: self.switch_page("settings"))

        self.btn_info = SidebarButton("Info")
        self.btn_info.clicked.connect(lambda: self.switch_page("info"))
        
        self.kawai_icon = QPushButton("なのです")
        self.kawai_icon.setFixedSize(QSize(220, 220))
        self.kawai_icon.setIcon(QIcon("/Users/fuyuuku/Projects/my-project/HomePage/icon/mikimikinano.png"))
        self.kawai_icon.setIconSize(QSize(220, 220))
        self.kawai_icon.setStyleSheet("""
            border-radius: 10px;
            color: rgba(255, 255, 255, 0)
        """)
        self.kawai_icon.clicked.connect(self.showTimeandDate)

        # 添加到布局
        layout.addWidget(self.btn_app)
        layout.addWidget(self.btn_random)
        layout.addWidget(self.btn_todo)
        layout.addWidget(self.btn_memo)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_info)
        layout.addWidget(self.kawai_icon)
        layout.addStretch()
        
        return sidebar

    def create_apps_page(self):
        """创建应用页面"""
        apps_container = QFrame()
        apps_container.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.1)
            }
        """)
        
        # 使用网格布局
        app_layout = QGridLayout(apps_container)
        app_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        app_layout.setHorizontalSpacing(20)
        app_layout.setVerticalSpacing(20)
        app_layout.setContentsMargins(20, 20, 20, 20)
        
        apps = {
            "砺儒云": "https://moodle.scnu.edu.cn/login/index.php",
            "AbdnIMS": "https://abdn.blackboard.com/?new_loc=%2Fultra%2Fcourse",
            "iTest": "https://sso.unipus.cn/sso/login?service=https%3A%2F%2Fitestcloud.unipus.cn%2Futest%2Fitest%2Flogin%3F_rp%3D%252Fitest%253Fx%253D1760636722165",
            "WeLearn": "https://welearn.sflep.com/student/index.aspx",
            "超星学习通": "https://v8.chaoxing.com/"
        }

        def create_open_url_lambda(url):
            return lambda: QDesktopServices.openUrl(QUrl(url))

        # 在网格中排列应用按钮
        row, col = 0, 0
        max_cols = 4
        
        # 清空之前的应用按钮引用
        self.app_buttons.clear()
        
        for name, url in apps.items():
            icon_path = f"/Users/fuyuuku/Projects/my-project/HomePage/icon/{name}.png"
            app_button = AppButton(name, icon_path)
            app_button.set_click_handler(create_open_url_lambda(url))
            app_button.setVisible(self.app_buttons_visible)  # 根据当前状态设置可见性
            
            # 添加到网格布局
            app_layout.addWidget(app_button, row, col, Qt.AlignCenter)
            # 保存应用按钮引用
            self.app_buttons.append(app_button)
            
            # 更新行列位置
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        return apps_container

    def create_random_page(self):
        """创建随机数页面"""
        random_container = QFrame()
        random_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 230, 240, 0.1);
                border-radius: 15px;
            }
        """)
        
        random_layout = QVBoxLayout(random_container)
        random_layout.setAlignment(Qt.AlignCenter)
        
        # 添加顶部弹性空间
        random_layout.addStretch()
        
        # 创建标题
        random_label = QLabel("是随机数なの")
        random_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 240, 245, 0);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        random_label.setFont(QFont("PingFang SC Medium", 64))
        random_label.setAlignment(Qt.AlignCenter)
        random_layout.addWidget(random_label)
        
        # 添加间距
        random_layout.addSpacing(30)
        
        # 创建输入框
        self.random_input = QLineEdit("请输入最大值なの")
        self.random_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 240, 245, 0.3);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border: 2px solid rgba(214, 75, 124, 0.4);
                border-radius: 10px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(214, 75, 124, 0.3);
            }
        """)
        self.random_input.setFont(QFont("PingFang SC Medium", 32))
        self.random_input.setAlignment(Qt.AlignCenter)
        #self.random_input.setMaximumWidth(200)
        random_layout.addWidget(self.random_input, alignment=Qt.AlignCenter)
        
        # 添加间距
        random_layout.addSpacing(20)
        
        # 创建生成按钮
        generate_button = QPushButton("生成随机数なの")
        generate_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 200, 220, 0.6);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border: 2px solid rgba(214, 75, 124, 0.3);
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 180, 210, 0.5);
                border: 2px solid rgba(214, 75, 124, 0.5);
            }
            QPushButton:pressed {
                background: rgba(255, 160, 200, 0.5);
            }
        """)
        generate_button.setFont(QFont("PingFang SC Medium", 32))
        generate_button.clicked.connect(self.generate_random_number)
        random_layout.addWidget(generate_button, alignment=Qt.AlignCenter)
        
        # 添加间距
        random_layout.addSpacing(20)
        
        # 创建显示结果的标签
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 240, 245, 0);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        self.result_label.setFont(QFont("ArialPingFang SC Medium", 32))
        self.result_label.setAlignment(Qt.AlignCenter)
        random_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        
        # 添加底部弹性空间
        random_layout.addStretch()
        
        return random_container

    def create_todo_page(self):
        """创建待办事项页面"""
        todo_container = QFrame()
        todo_container.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.1)
            }
        """)
        
        todo_layout = QVBoxLayout(todo_container)
        todo_button = QPushButton("    + 添加待办事项    ")
        todo_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 200, 220, 0.6);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border: 2px solid rgba(214, 75, 124, 0.3);
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 180, 210, 0.5);
                border: 2px solid rgba(214, 75, 124, 0.5);
            }
            QPushButton:pressed {
                background: rgba(255, 160, 200, 0.5);
            }
        """)
        todo_button.setFont(QFont("PingFang SC Medium", 24))
        todo_layout.addWidget(todo_button, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        todo_button.clicked.connect(self.open_dialog_todo)
        self.todo_list = {

        }
        
        # 创建交叉线覆盖层
        crosshair_overlay = QFrame(todo_container)
        crosshair_overlay.setStyleSheet("background: transparent; border: none;")
        crosshair_overlay.setAttribute(Qt.WA_TransparentForMouseEvents)  # 鼠标事件穿透
        crosshair_overlay.lower()  # 置于底层
        
        # 重写paintEvent来绘制交叉线
        def paint_event(event):
            painter = QPainter(crosshair_overlay)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 设置线条样式
            pen = QPen(QColor(214, 75, 124, 90))
            pen.setWidth(6)
            painter.setPen(pen)
            
            width = crosshair_overlay.width()
            height = crosshair_overlay.height()
            
            # 绘制水平中线
            center_y = height // 2
            painter.drawLine(0, center_y, width, center_y)
            
            # 绘制垂直中线
            center_x = width // 2
            painter.drawLine(center_x, 0, center_x, height)
            
            painter.end()
        
        crosshair_overlay.paintEvent = paint_event
        
        # 确保覆盖层随容器大小变化
        def resize_event(event):
            crosshair_overlay.setGeometry(0, 0, todo_container.width(), todo_container.height())
            crosshair_overlay.update()  # 触发重绘
        
        todo_container.resizeEvent = resize_event
        
        return todo_container
    
    def open_dialog_todo(self):
        """打开添加待办事项对话框"""
        todo_dialog = QDialog(self)
        todo_dialog.setWindowTitle("添加待办事项")
        todo_dialog.setFixedSize(390, 480)
        # todo_dialog_layout = QVBoxLayout(self.todo_page)
        todo_dialog.setStyleSheet("""
            QDialog {
                background: rgba(255, 240, 245, 0.6);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border: 10px solid rgba(214, 75, 124, 0.3);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        todo_dialog.setWindowOpacity(0.7)
        todo_dialog_layout = QVBoxLayout(todo_dialog)
        todo_dialog_layout.setContentsMargins(20, 20, 20, 20)
        self.todo_content_input = QLineEdit("请输入待办内容なの")
        self.todo_content_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 240, 245, 0.3);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border: 2px solid rgba(214, 75, 124, 0.4);
                border-radius: 10px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(214, 75, 124, 0.3);
            }
        """)
        self.todo_content_input.setFont(QFont("PingFang SC Medium", 32))
        self.todo_content_input.setAlignment(Qt.AlignCenter)
        todo_dialog_layout.addWidget(self.todo_content_input, alignment=Qt.AlignCenter)
        self.todo_date_input = QLineEdit("YYYY-MM-DD HH:MM")
        self.todo_date_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 240, 245, 0.3);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border: 2px solid rgba(214, 75, 124, 0.4);
                border-radius: 10px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(214, 75, 124, 0.3);
            }
        """)
        self.todo_date_input.setFont(QFont("PingFang SC Medium", 32))
        self.todo_date_input.setAlignment(Qt.AlignCenter)
        todo_dialog_layout.addWidget(self.todo_date_input, alignment=Qt.AlignCenter)
        self.todo_mode_o = QComboBox(self)
        self.todo_mode_o.addItems(['  紧急  ', '  还好  ','  宽松  ', '  不紧急  '])
        self.todo_mode_t = QComboBox(self)
        self.todo_mode_t.addItems(['  很重要  ','  重要  ','  次要  ','  无聊  '])
        combo_box_style = """
        QComboBox {
            background-color: rgba(255, 200, 220, 0.6);
            color: rgba(30, 50, 80, 1);
            font-size: 14px;
            border-radius: 10px;        
        }
        QComboBox QAbstractItemView {
            background-color: white;
            selection-background-color: white;
            }        
        """
        self.todo_mode_o.setStyleSheet(combo_box_style)
        self.todo_mode_o.setFixedWidth(100)
        self.todo_mode_t.setStyleSheet(combo_box_style)
        self.todo_mode_t.setFixedWidth(100)
        todo_dialog_layout.addWidget(self.todo_mode_o, alignment=Qt.AlignCenter)
        todo_dialog_layout.addWidget(self.todo_mode_t, alignment=Qt.AlignCenter)
        add_todo_button = QPushButton("添加待办事项なの")
        add_todo_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 200, 220, 0.6);
                color: rgba(30, 50, 80, 1);
                font-weight: bold;
                border: 2px solid rgba(214, 75, 124, 0.3);
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 180, 210, 0.5);
                border: 2px solid rgba(214, 75, 124, 0.5);
            }
            QPushButton:pressed {
                background: rgba(255, 160, 200, 0.5);
            }
        """)
        add_todo_button.setFont(QFont("PingFang SC Medium", 24))
        todo_dialog_layout.addWidget(add_todo_button, alignment=Qt.AlignCenter)
        add_todo_button.clicked.connect(self.written_todo)

        todo_dialog_layout.addSpacing(20)
        todo_dialog.exec()
    
    def create_todo_symbol(self):
        # 不再清除之前的待办按钮，只添加新的按钮
        
        # 获取待办事项页面的容器
        todo_container = self.right_container.widget(2)  # todo页面的索引是2
        
        # 只处理最后一个添加的待办事项（新添加的）
        if self.todo_list:
            todo_item = self.todo_list[-1]  # 只获取最新添加的待办事项
            task = todo_item.get("任务", "")
            mode_o = todo_item.get("要紧程度", "还好")
            mode_t = todo_item.get("重要程度", "重要")
            
            # 创建待办事项按钮
            todo_btn = TodoButton(task, len(self.todo_list_button))  # 使用当前按钮数量作为color_code
            todo_btn.setFixedStyle(len(self.todo_list_button))

            # 根据重要程度和紧急程度确定位置
            container_width = todo_container.width()
            container_height = todo_container.height()
            
            # 计算位置
            if mode_o == '紧急':
                x = random.randint(container_width * 3 // 4, container_width - 135)  # 减去按钮宽度
            elif mode_o == '还好':
                x = random.randint(container_width // 2, container_width * 3 // 4 - 135)
            elif mode_o == '宽松':
                x = random.randint(container_width // 4, container_width // 2 - 135)
            else:  # 不紧急
                x = random.randint(0, container_width // 4 - 135)

            if mode_t == '很重要':
                y = random.randint(container_height * 3 // 4, container_height - 65)  # 减去按钮高度
            elif mode_t == '重要':
                y = random.randint(container_height // 2, container_height * 3 // 4 - 65)
            elif mode_t == '次要':
                y = random.randint(container_height // 4, container_height // 2 - 65)
            else:  # 无聊
                y = random.randint(0, container_height // 4 - 65)
            
            # 设置按钮位置
            todo_btn.setParent(todo_container)
            todo_btn.move(x, y)
            todo_btn.show()
            
            # 保存按钮引用
            self.todo_list_button.append(todo_btn)

    def written_todo(self):
        misson = self.todo_content_input.text().strip()
        deadline = self.todo_date_input.text().strip()
        mode_o = self.todo_mode_o.currentText().strip()
        mode_t = self.todo_mode_t.currentText().strip()
        todo_item = {
            "任务": misson,
            "截止日期": deadline, 
            "要紧程度": mode_o,
            "重要程度": mode_t
        }
        self.todo_list.append(todo_item)
        self.create_todo_symbol()
        # 关闭对话框
        self.sender().parent().accept()  # 获取按钮的父窗口（对话框）并关闭
            

    def create_memo_page(self):
        """创建备忘录页面"""
        memo_container = QFrame()
        memo_container.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.1)
            }
        """)
        
        memo_layout = QVBoxLayout(memo_container)
        memo_label = QLabel("备忘录页面 - 开发中")
        memo_label.setFont(QFont("Arial", 24))
        memo_label.setAlignment(Qt.AlignCenter)
        memo_layout.addWidget(memo_label)
        
        return memo_container

    def create_settings_page(self):
        """创建设置页面"""
        settings_container = QFrame()
        settings_container.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.1)
            }
        """)
        
        settings_layout = QVBoxLayout(settings_container)
        settings_label = QLabel("设置页面 - 开发中")
        settings_label.setFont(QFont("Arial", 24))
        settings_label.setAlignment(Qt.AlignCenter)
        settings_layout.addWidget(settings_label)
        
        return settings_container

    def create_info_page(self):
        """创建信息页面"""
        info_container = QFrame()
        info_container.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.1)
            }
        """)
        
        info_layout = QVBoxLayout(info_container)
        info_label = QLabel("信息页面 - 开发中")
        info_label.setFont(QFont("Arial", 24))
        info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)
        
        return info_container

    def switch_page(self, page_name):
        """切换页面"""
        page_map = {
            "apps": 0,
            "random": 1,
            "todo": 2,
            "memo": 3,
            "settings": 4,
            "info": 5
        }
        
        if page_name in page_map:
            self.right_container.setCurrentIndex(page_map[page_name])
            self.current_page = page_name
            self.miki_label.hide()
            self.miki_label = MikiLabel("这里会热闹起来的なの", self)
            self.miki_label.show()
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.hide_label)
            self.timer.start(5000) 

    def toggle_app_buttons(self):
        """切换应用按钮的显示/隐藏"""
        self.app_buttons_visible = not self.app_buttons_visible
        for app_button in self.app_buttons:
            app_button.setVisible(self.app_buttons_visible)

    def hide_app_buttons(self):
        """隐藏所有应用按钮"""
        self.app_buttons_visible = False
        for app_button in self.app_buttons:
            app_button.setVisible(False)

    def generate_random_number(self):
        import random
        try:
            max_value = int(self.random_input.text())
            if max_value <= 0:
                raise ValueError("最大值必须是正整数")
            random_number = random.randint(1, max_value)
            self.miki_label.hide()
            self.result_label.setText(f"生成的随机数是: {random_number}")
            self.miki_label = MikiLabel("MIKIMIKI算出来了なの", self)
            self.miki_label.show()
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.hide_label)
            self.timer.start(5000) 
        except ValueError as e:
            self.miki_label.hide()
            self.miki_label = MikiLabel("输入错误了なの, " + str(e), self)
            self.miki_label.show()
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.hide_label)
            self.timer.start(5000) 
    
    def showTimeandDate(self):
        """显示当前时间和日期"""
        current_time = QTime.currentTime().toString("HH:mm:ss")
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.miki_label.hide()
        self.miki_label = MikiLabel("现在是，" + current_date + " " + current_time, self)
        self.miki_label.show()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_label)
        self.timer.start(5000) 

    def setupBackground(self):
        """设置背景图片"""
        self.image_path = ""
        for root, dirs, files in os.walk(os.path.expanduser("~")):
            if "IMG_9881.JPG" in files:
                self.image_path = os.path.join(root, "IMG_9881.JPG")
                break
        
        self.update_background()

    def update_background(self):
        """更新背景图片"""
        if os.path.exists(self.image_path):
            palette = QPalette()
            pixmap = QPixmap(self.image_path)
            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
            self.setPalette(palette)
            self.setWindowOpacity(0.8)
        else:
            print(f"Error: Image file not found at {self.image_path}")

    def resizeEvent(self, event):
        """重写窗口大小改变事件，实时更新背景"""
        super().resizeEvent(event)
        self.update_background()

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    window.showFullScreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()