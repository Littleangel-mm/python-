import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from ultralytics import YOLO

# YOLOv8 best.pt 模型路径
MODEL_PATH = 'runs/classify/result_exp/weights/best.pt'
# MODEL_PATH = 'runs/classify/result_exp/weights/last.pt'  # 根据实际训练结果调整
# MODEL_PATH = 'yolov8n-cls.pt'  


IMG_SIZE = 224

# 加载YOLOv8模型
model = YOLO(MODEL_PATH)

# 获取类别名（从模型属性获取）
class_names = list(model.model.names.values()) if hasattr(model.model, 'names') else [str(i) for i in range(model.model.nc)]

class Predictor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('鸟类图片分类预测（YOLOv8）')
        self.setFixedSize(420, 600)
        self.setStyleSheet("background-color: #f7f7fa;")

        # 顶部标题
        self.title_label = QLabel('鸟类图片分类预测')
        self.title_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #2d4059; margin-top: 20px; margin-bottom: 10px;")

        # 图片显示
        self.img_label = QLabel('请选择图片')
        self.img_label.setFixedSize(300, 300)
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setStyleSheet("border: 2px dashed #a3a3a3; background: #fff; color: #a3a3a3; font-size: 16px;")

        # 选择图片按钮
        self.btn = QPushButton('选择图片')
        self.btn.setFont(QFont('Arial', 14))
        self.btn.setStyleSheet(
            "QPushButton {background-color: #30a7e3; color: white; border-radius: 8px; padding: 10px 20px;}"
            "QPushButton:hover {background-color: #1976d2;}"
        )
        self.btn.clicked.connect(self.open_image)

        # 预测结果
        self.result_label = QLabel('')
        self.result_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #e94f37; margin-top: 20px;")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.img_label, alignment=Qt.AlignCenter)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.result_label)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)
        self.center()

    def center(self):
        # 窗口居中
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_image(self):
        file, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Image files (*.jpg *.jpeg *.png)')
        if file:
            pixmap = QPixmap(file).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.img_label.setPixmap(pixmap)
            pred, prob = self.predict(file)
            self.result_label.setText(f'预测类别: <span style=\"color:#1976d2\">{pred}</span><br>概率: <span style=\"color:#43aa8b\">{prob:.4f}</span>')

    def predict(self, img_path):
        # YOLOv8 分类推理
        results = model(img_path)
        probs = results[0].probs
        pred_idx = int(probs.top1)
        pred_class = class_names[pred_idx] if class_names else str(pred_idx)
        prob = float(probs.data[pred_idx])
        return pred_class, prob

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Predictor()
    window.show()
    sys.exit(app.exec_()) 