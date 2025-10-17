import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QPushButton, QDialog, QVBoxLayout, QInputDialog, QLineEdit
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import random

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDateTime()  # 初始化日期时间显示

    def initDateTime(self):
        # 创建日期和时间标签
        self.date_label = QLabel(self)
        self.time_label = QLabel(self)
        
        # 样式设置
        label_style = """
            background-color: white;
            color: #b98a7c;
            font-size: 24px;
            padding: 5px;
            border-radius: 3px;
            font: Arial;
        """
        self.date_label.setStyleSheet(label_style)
        self.time_label.setStyleSheet(label_style)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.time_label.setAlignment(Qt.AlignCenter)
        
        # 创建定时器更新时钟
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)  # 每秒更新一次
        
        # 初始更新
        self.updateDateTime()
        self.updateLabelPositions()

    def updateDateTime(self):
        """更新日期和时间显示"""
        current_date = QDate.currentDate().toString('yyyy-MM-dd')
        current_time = QTime.currentTime().toString('hh:mm:ss')
        
        self.date_label.setText(current_date)
        self.time_label.setText(current_time)
        
        # 调整位置（确保在窗口调整大小时也能正确显示）
        self.updateLabelPositions()

    def updateLabelPositions(self):
        """更新标签位置到右上角"""
        label_width = 150
        label_height = 30
        margin = 5
        
        self.date_label.setGeometry(
            self.width() - label_width - margin, 
            margin, 
            label_width, 
            label_height
        )
        self.time_label.setGeometry(
            self.width() - label_width - margin, 
            margin + label_height + 10,  # 添加5px间距
            label_width, 
            label_height
        )

    def resizeEvent(self, event):
        """窗口大小改变时的事件处理"""
        self.updateLabelPositions()
        self.update_background()
        super().resizeEvent(event)

    def initUI(self):
        # 设置窗口标题和初始大小
        self.setWindowTitle('My HomePage')
        self.setGeometry(300, 300, 1440, 797)

        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        menubar.setNativeMenuBar(False)

        # 添加按钮
        self.createButtons()
        
        # 创建状态栏
        self.createStatusBar()
        
        # 设置背景图片
        self.setupBackground()

    def createButtons(self):
        """创建所有按钮"""
        button1 = QPushButton('吃什么', self)
        button1.setGeometry(20, 110, 100, 50)
        button1.clicked.connect(self.open_random_dialog)
        
        button2 = QPushButton('打开课程网站', self)
        button2.setGeometry(20, 50, 200, 50)
        button2.clicked.connect(self.open_course_selection_dialog)
        
        button3 = QPushButton('ddl', self)
        button3.setGeometry(20, 170, 80, 50)
        
        # 设置按钮样式
        button_style = """
        QPushButton {
            background-color: #f9d6db;
            color: black;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
        }
        QPushButton:hover {
            background-color: #e8a3ae;
        }
        """
        
        button1.setStyleSheet(button_style)
        button2.setStyleSheet(button_style)
        button3.setStyleSheet(button_style)

    def open_course_selection_dialog(self):
        """打开课程网站选择对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("请选择要打开的课程网站")
        dialog.setFixedSize(300, 300)  # 设置对话框大小
        layout = QVBoxLayout()

        courses = {
            "砺儒云": "https://moodle.scnu.edu.cn/login/index.php",
            "AbdnIMS": "https://abdn.blackboard.com/?new_loc=%2Fultra%2Fcourse",
            "iTest": "https://sso.unipus.cn/sso/login?service=https%3A%2F%2Fitestcloud.unipus.cn%2Futest%2Fitest%2Flogin%3F_rp%3D%252Fitest%253Fx%253D1760636722165",
            "WeLearn": "https://welearn.sflep.com/student/index.aspx",
            "超星学习通": "https://v8.chaoxing.com/"
        }

        def create_open_url_lambda(url):
            return lambda: (QDesktopServices.openUrl(QUrl(url)), dialog.accept())

        for name, url in courses.items():
            btn = QPushButton(name)
            btn.clicked.connect(create_open_url_lambda(url))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f9d6db;
                    padding: 10px;
                    margin: 2px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    color: black;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #e8a3ae;
                }
            """)
            layout.addWidget(btn)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def open_random_dialog(self):
        """打开随机数对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("吃什么")
        dialog.setFixedSize(300, 300)  # 设置对话框大小
        layout = QVBoxLayout()

        # 创建文本输入框
        input_box = QLineEdit(dialog)
        input_box.setPlaceholderText("一个数喵")

        # 创建按钮
        button = QPushButton("生成随机数", dialog)
        button.setStyleSheet("""
                QPushButton {
                    background-color: #f9d6db;
                    padding: 10px;
                    margin: 2px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    color: black;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #e8a3ae;
                }
            """)

        # 创建用于显示结果的标签
        result_label = QLabel("", dialog)
        result_label.setAlignment(Qt.AlignCenter)

        def generate_random():
            max_val_text = input_box.text()
            try:
                max_val = int(max_val_text)
                if max_val > 0:
                    random_num = random.randint(1, max_val)
                    result_label.setText(f"喵喵: {random_num}")
                else:
                    result_label.setText("一个正整数喵")
            except ValueError:
                result_label.setText("好好吃饭喵。")

        button.clicked.connect(generate_random)

        # 将控件添加到布局中
        layout.addWidget(QLabel("一个数喵:"))
        layout.addWidget(input_box)
        layout.addWidget(button)
        layout.addWidget(result_label)

        dialog.setLayout(layout)
        dialog.exec_()

    def createStatusBar(self):
        """创建状态栏"""
        self.statusBar().showMessage('贴贴成功')
        self.status_label = QLabel('贴贴成功')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.statusBar().addWidget(self.status_label, 1)

    def setupBackground(self):
        """设置背景图片"""
        self.setWindowOpacity(0.8)
        
        # 搜索图片文件
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
        else:
            print(f"Error: Image file not found at {self.image_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())