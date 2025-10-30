import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QSystemTrayIcon, 
                               QStyle, QMessageBox, QVBoxLayout, QLabel)
from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QCursor, QAction, QPainter, QMouseEvent, QEnterEvent
import math


class FloatingImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # 窗口设置
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |      # 始终置顶
            Qt.FramelessWindowHint |       # 无边框
            Qt.ToolTip                        # 工具窗口，不在任务栏显示
        )
        
        # 初始化变量
        self.dragging = False
        self.drag_position = QPoint()
        self.opacity = 0.8
        self.follow_mouse = False
        self.rotation_angle = 0
        
        # 创建布局和标签
        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # 设置初始大小和位置
        self.setGeometry(100, 100, 200, 200)
        
        # 鼠标追踪定时器（用于图片转向）
        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self.update_rotation)
        self.mouse_timer.start(50)  # 每50ms更新一次
        
        # 动画效果
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        
        # 设置初始透明度
        self.setWindowOpacity(self.opacity)

    def load_image(self, image_path):
        """加载图片并调整大小"""
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # 调整图片大小，保持宽高比
            scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.adjustSize()  # 调整窗口大小以适应图片
            
            # 添加阴影效果（可选）
            self.image_label.setStyleSheet("""
                QLabel {
                    background: transparent;
                    border: none;
                }
            """)
            return True
        return False

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
            # 点击时短暂提高不透明度
            self.animate_opacity(1.0, 0.3)

    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
            
            # 恢复原始透明度
            self.animate_opacity(self.opacity, 0.3)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            self.open_external_program()
            event.accept()

    def contextMenuEvent(self, event):
        """右键菜单事件"""
        menu = QMenu(self)
        
        # 设计选项
        design_action = menu.addAction("设计选项")
        design_action.triggered.connect(self.show_design_options)
        
        # 透明度调节
        opacity_menu = menu.addMenu("透明度")
        opacity_actions = [
            ("30%", 0.3), ("50%", 0.5), ("70%", 0.7), 
            ("80%", 0.8), ("90%", 0.9), ("100%", 1.0)
        ]
        
        for text, value in opacity_actions:
            action = opacity_menu.addAction(text)
            action.triggered.connect(lambda checked, v=value: self.set_opacity(v))
        
        # 鼠标跟随开关
        follow_action = menu.addAction("开启鼠标跟随" if not self.follow_mouse else "关闭鼠标跟随")
        follow_action.triggered.connect(self.toggle_mouse_follow)
        
        # 旋转开关
        rotate_action = menu.addAction("开启旋转" if not self.mouse_timer.isActive() else "关闭旋转")
        rotate_action.triggered.connect(self.toggle_rotation)
        
        menu.addSeparator()
        
        # 退出选项
        exit_action = menu.addAction("退出")
        exit_action.triggered.connect(self.close_application)
        
        menu.exec(event.globalPos())

    def update_rotation(self):
        """更新图片朝向鼠标位置（简易版转向）"""
        if self.follow_mouse:
            # 计算鼠标相对于图片中心的角度
            widget_center = self.geometry().center()
            mouse_pos = QCursor.pos()
            
            dx = mouse_pos.x() - widget_center.x()
            dy = mouse_pos.y() - widget_center.y()
            
            # 计算角度（弧度）
            angle_rad = math.atan2(dy, dx)
            angle_deg = math.degrees(angle_rad)
            
            # 平滑旋转（使用线性插值）
            target_angle = angle_deg
            current_angle = self.rotation_angle
            
            # 角度差值处理（跨越360度的情况）
            angle_diff = (target_angle - current_angle) % 360
            if angle_diff > 180:
                angle_diff -= 360
            
            # 平滑过渡
            self.rotation_angle = current_angle + angle_diff * 0.1
            
            # 应用旋转（这里使用简单的CSS变换）
            self.apply_rotation()

    def apply_rotation(self):
        """应用旋转效果到图片"""
        pixmap = self.image_label.pixmap()
        if pixmap:
            # 创建变换后的pixmap
            transformed_pixmap = pixmap.transformed(
                pixmap.transformed().rotate(self.rotation_angle),
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(transformed_pixmap)

    def animate_opacity(self, target_opacity, duration=300):
        """透明度动画"""
        self.animation.stop()
        self.animation.setStartValue(self.windowOpacity())
        self.animation.setEndValue(target_opacity)
        self.animation.setDuration(duration)
        self.animation.start()

    def set_opacity(self, opacity):
        """设置透明度"""
        self.opacity = opacity
        self.animate_opacity(opacity)

    def toggle_mouse_follow(self):
        """切换鼠标跟随模式"""
        self.follow_mouse = not self.follow_mouse

    def toggle_rotation(self):
        """切换旋转功能"""
        if self.mouse_timer.isActive():
            self.mouse_timer.stop()
        else:
            self.mouse_timer.start(5)

    def show_design_options(self):
        """显示设计选项对话框 - 暴露设计选项函数
        
        功能说明：
        这里可以添加各种设计选项，例如：
        - 更换图片
        - 调整大小
        - 修改形状
        - 添加边框
        - 颜色调整
        - 动画效果设置
        """
        QMessageBox.information(self, "设计选项", 
                               "设计选项功能已暴露\n"
                               "可在此处实现：\n"
                               "- 图片更换功能\n"
                               "- 尺寸调整\n"
                               "- 样式修改\n"
                               "- 动画设置")

    def open_external_program(self):
        """打开外部程序 - 暴露打开程序函数
        
        功能说明：
        这里可以实现打开其他应用程序的功能
        例如：
        - 打开计算器
        - 启动浏览器
        - 运行特定软件
        - 执行系统命令
        """
        QMessageBox.information(self, "打开程序", 
                               "打开外部程序功能已暴露\n"
                               "可在此处实现：\n"
                               "- 系统程序调用\n"
                               "- 自定义应用启动\n"
                               "- 文件打开操作")

    def close_application(self):
        """关闭应用程序"""
        self.mouse_timer.stop()
        self.close()


class FloatingImageApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.widget = FloatingImageWidget()
        
        # 系统托盘图标
        self.setup_tray_icon()

    def setup_tray_icon(self):
        """设置系统托盘图标"""
        self.tray_icon = QSystemTrayIcon(self.widget)
        self.tray_icon.setIcon(self.widget.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # 托盘菜单
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("显示/隐藏")
        show_action.triggered.connect(self.toggle_visibility)
        
        change_image_action = tray_menu.addAction("更换图片")
        change_image_action.triggered.connect(self.change_image)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def toggle_visibility(self):
        """切换显示/隐藏"""
        if self.widget.isVisible():
            self.widget.hide()
        else:
            self.widget.show()

    def change_image(self):
        """更换图片对话框"""
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self.widget, 
            "选择图片", 
            "", 
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.widget.load_image(file_path)

    def tray_icon_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_visibility()

    def quit_application(self):
        """退出应用程序"""
        self.widget.close()
        self.app.quit()

    def run(self, image_path=None):
        """运行应用程序"""
        if image_path and self.widget.load_image(image_path):
            print(f"成功加载图片: {image_path}")
        else:
            # 如果没有提供图片，使用默认图片或提示用户
            print("请通过托盘菜单更换图片")
        
        self.widget.show()
        return self.app.exec()


def main():
    """主函数"""
    app = FloatingImageApp()
    
    # 如果通过命令行参数提供了图片路径
    image_path = "/Users/fuyuuku/Projects/my-project/HomePage/icon/mikimikinano.png"
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    sys.exit(app.run(image_path))


if __name__ == "__main__":
    main()