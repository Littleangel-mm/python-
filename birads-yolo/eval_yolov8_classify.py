from ultralytics import YOLO

DATA_DIR = 'birds'
model = YOLO('runs/classify/exp/weights/best.pt')  # 路径根据实际训练结果调整

metrics = model.val(data=f'{DATA_DIR}/test')
print(metrics) 