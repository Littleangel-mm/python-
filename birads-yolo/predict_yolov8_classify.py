from ultralytics import YOLO
import sys

# 加载训练好的模型
model = YOLO('runs/classify/exp/weights/best.pt')  # 路径根据实际训练结果调整

# 预测单张图片
img_path = sys.argv[1]  # 用法：python predict_yolov8_classify.py path/to/image.jpg
results = model(img_path)

# 输出概率和类别
probs = results[0].probs
print('类别概率:', probs.data.cpu().numpy())
print('预测类别:', results[0].names[probs.top1]) 