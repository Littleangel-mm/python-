from PIL import Image
import os

class ImageTools:
    def ensure_dir(self, directory):
        """确保目录存在，如果不存在则创建"""
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def resize_images(self, input_folder, output_folder, target_size=(720, 1080)):
        """调整图片尺寸"""
        self.ensure_dir(output_folder)
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(valid_extensions):
                try:
                    img_path = os.path.join(input_folder, filename)
                    img = Image.open(img_path)
                    
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    img_width, img_height = img.size
                    ratio = min(target_size[0] / img_width, target_size[1] / img_height)
                    new_size = (int(img_width * ratio), int(img_height * ratio))
                    
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                    new_img = Image.new('RGB', target_size, (255, 255, 255))
                    
                    offset = ((target_size[0] - new_size[0]) // 2, 
                             (target_size[1] - new_size[1]) // 2)
                    new_img.paste(img, offset)
                    
                    output_path = os.path.join(output_folder, filename)
                    new_img.save(output_path, quality=95)
                    print(f"✅ 尺寸调整完成: {filename}")
                except Exception as e:
                    print(f"❌ 处理失败 {filename}: {e}")
    
    def compress_images(self, input_folder, output_folder, quality=85):
        """压缩图片"""
        self.ensure_dir(output_folder)
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
        
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(valid_extensions):
                try:
                    img_path = os.path.join(input_folder, filename)
                    img = Image.open(img_path)
                    
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    output_path = os.path.join(output_folder, filename)
                    img.save(output_path, quality=quality, optimize=True)
                    print(f"✅ 压缩完成: {filename}")
                except Exception as e:
                    print(f"❌ 压缩失败 {filename}: {e}")
    
    def create_scroll_gif(self, output_path, chinese_text, english_names, font_path="msyh.ttc"):
        """创建滚动GIF"""
        width, height = 700, 300
        line_height = 45
        scroll_area_top = 30
        scroll_speed = 2.5
        total_text_height = len(english_names) * line_height
        scroll_range = total_text_height + height
        frame_count = int(scroll_range / scroll_speed)
        frame_duration = 80
        
        frames = []
        font_large = ImageFont.truetype(font_path, 80)
        font_small = ImageFont.truetype(font_path, 30)
        
        for i in range(frame_count):
            img = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(img)
            draw.text((30, 50), chinese_text, font=font_large, fill="black")
            
            y_offset = scroll_area_top - (i * scroll_speed)
            for j, name in enumerate(english_names):
                y = y_offset + j * line_height
                if -line_height < y < height:
                    draw.text((360, y), name, font=font_small, fill="black")
            
            frames.append(img.convert("P", palette=Image.ADAPTIVE))
        
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_duration,
            loop=0,
            optimize=True
        )
        print(f"✅ GIF生成完成：{output_path}")

def convert_to_png(self, folder_path, output_folder):
        """将任意格式图片转换为PNG格式"""
        self.ensure_dir(output_folder)
        count = 1
        valid_extensions = ('.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
        
        for file in os.listdir(folder_path):
            if file.lower().endswith(valid_extensions):
                try:
                    img_path = os.path.join(folder_path, file)
                    with Image.open(img_path) as img:
                        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                            # 保持透明通道
                            png_img = img.convert('RGBA')
                        else:
                            # 转换为RGB
                            png_img = img.convert('RGB')
                        
                        # 使用原文件名，仅改变扩展名
                        base_name = os.path.splitext(file)[0]
                        png_name = f'{base_name}.png'
                        png_path = os.path.join(output_folder, png_name)
                        
                        # 如果文件已存在，添加数字后缀
                        while os.path.exists(png_path):
                            png_name = f'{base_name}_{count}.png'
                            png_path = os.path.join(output_folder, png_name)
                            count += 1
                        
                        png_img.save(png_path, 'PNG')
                        print(f"✅ 格式转换完成: {file} → {png_name}")
                except Exception as e:
                    print(f"❌ 转换失败 {file}: {e}")