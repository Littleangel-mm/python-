from ultralytics import YOLO
import os

# 配置参数
DATA_DIR = 'birds'  # 数据集根目录
MODEL_NAME = 'yolov8n-cls.pt'  # 可更换为 yolov8s-cls.pt、yolov8m-cls.pt 等
EPOCHS = 1
IMG_SIZE = 224
BATCH_SIZE = 32
LR = 0.01
PROJECT = 'runs/classify'
EXP_NAME = 'result_exp'

# 创建模型
print(f'加载模型: {MODEL_NAME}')
model = YOLO(MODEL_NAME)

# 训练模型
print('开始训练...')
results = model.train(
    data=DATA_DIR,
    epochs=EPOCHS,
    imgsz=IMG_SIZE,
    batch=BATCH_SIZE,
    lr0=LR,
    workers=4,
    project=PROJECT,
    name=EXP_NAME,
    val=True
)

print('\n训练完成，主要结果如下:')
print(results)

# 模型权重保存路径
weights_dir = os.path.join(PROJECT, EXP_NAME, 'weights')
best_model_path = os.path.join(weights_dir, 'best.pt')
last_model_path = os.path.join(weights_dir, 'last.pt')

if os.path.exists(best_model_path):
    print(f'最佳模型已保存: {best_model_path}')
    # 重新加载最佳模型用于评估
    model = YOLO(best_model_path)
else:
    print('未找到最佳模型权重文件，使用当前模型。')

# 在测试集上评估
print('\n开始在测试集上评估...')
metrics = model.val(data=f'{DATA_DIR}/test')
print('测试集评估结果:')
print(metrics)

# 可选：输出更详细的评估指标
if hasattr(metrics, 'results_dict'):
    print('\n详细评估指标:')
    for k, v in metrics.results_dict.items():
        print(f'{k}: {v}')

print('\n全部流程结束！')
 