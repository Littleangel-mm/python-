import os
import shutil
import random

SOURCE_DIR = 'all_data'
TARGET_DIR = 'birds'
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

random.seed(42)

for split in ['train', 'valid', 'test']:
    split_dir = os.path.join(TARGET_DIR, split)
    os.makedirs(split_dir, exist_ok=True)

for class_name in os.listdir(SOURCE_DIR):
    class_dir = os.path.join(SOURCE_DIR, class_name)
    if not os.path.isdir(class_dir):
        continue

    images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(images)

    n_total = len(images)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    n_test = n_total - n_train - n_val

    splits = {
        'train': images[:n_train],
        'valid': images[n_train:n_train + n_val],
        'test': images[n_train + n_val:]
    }

    for split, split_images in splits.items():
        split_class_dir = os.path.join(TARGET_DIR, split, class_name)
        os.makedirs(split_class_dir, exist_ok=True)
        for img in split_images:
            src_path = os.path.join(class_dir, img)
            dst_path = os.path.join(split_class_dir, img)
            shutil.copy2(src_path, dst_path)

print('数据集划分完成！') 