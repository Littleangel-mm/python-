# YOLOv8 鸟类分类项目运行说明

## 1. 环境准备

1. 安装 Python 3.8 及以上版本。
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. 数据准备与划分

1. 将所有原始图片按类别放入 `all_data/` 目录下，例如：
   ```
   all_data/
     麻雀/
       1.jpg
       2.jpg
       ...
     喜鹊/
       1.jpg
       2.jpg
       ...
   ```
2. 运行数据集划分脚本，自动生成训练集、验证集、测试集：
   ```bash
   python split_dataset.py
   ```
   运行后会生成 birds/train、birds/valid、birds/test 三个文件夹，每个文件夹下有各自的类别子文件夹。

---

## 3. 训练模型

运行训练脚本，开始模型训练并在测试集上评估：
```bash
python train_yolov8_classify.py
```
训练结果和模型权重会保存在 `runs/classify/exp/` 目录下。

---

## 4. 单张图片预测

对单张图片进行分类预测，命令如下：
```bash
python predict_yolov8_classify.py path/to/image.jpg
```
输出为该图片的类别概率和预测类别。

---

## 5. 测试集评估

对测试集整体进行评估，命令如下：
```bash
python eval_yolov8_classify.py
```
输出为模型在测试集上的准确率等指标。

---

## 6. 目录结构示例

```
birads-yolo/
  all_data/
  birds/
    train/
    valid/
    test/
  split_dataset.py
  train_yolov8_classify.py
  predict_yolov8_classify.py
  eval_yolov8_classify.py
  requirements.txt
```

---

## 7. 注意事项

- 训练脚本默认使用 yolov8n-cls.pt（nano版），如需更高精度可改为 yolov8s-cls.pt、yolov8m-cls.pt 等。
- 训练参数（如 epochs、batch size）可在 train_yolov8_classify.py 中调整。
- 预测和评估脚本中的模型路径需与实际训练结果一致。

---

如有问题，欢迎随时提问！
