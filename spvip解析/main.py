import sys
import os
import webbrowser
import requests
from lxml import etree
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QFrame, QMessageBox, QSizePolicy, QProgressBar
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FetchThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, url, retries=3):
        super().__init__()
        self.url = url
        self.retries = retries

    def run(self):
        for attempt in range(self.retries):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept-Language': 'zh-CN,zh;q=0.9'
                }
                response = requests.get(self.url, headers=headers, timeout=10)
                response.raise_for_status()
                response.encoding = 'utf-8'
                text = response.text
                logger.debug(f"接口返回数据: {text[:500]}...")

                parser = etree.HTMLParser(encoding='utf-8')
                e = etree.HTML(text, parser=parser)
                
                jiek = e.xpath('//*[@id="jk"]/option/text() | //select[@name="jk"]/option/text() | //select/option/text()')
                jiek_url = e.xpath('//*[@id="jk"]/option/@value | //select[@name="jk"]/option/@value | //select/option/@value')
                
                jiek = [item.strip() for item in jiek if item.strip()]
                jiek_url = [item.strip() for item in jiek_url if item.strip()]
                
                if len(jiek) != len(jiek_url):
                    logger.error(f"解析线路名称数量 ({len(jiek)}) 与URL数量 ({len(jiek_url)}) 不匹配")
                    raise ValueError("线路数据不完整")

                jiekdi = dict(zip(jiek, jiek_url))
                logger.debug(f"解析到的线路: {jiekdi}")
                
                if not jiekdi:
                    raise ValueError("未解析到任何线路")
                
                self.finished.emit(jiekdi)
                return
                
            except Exception as e:
                logger.error(f"尝试 {attempt + 1}/{self.retries} 失败: {str(e)}")
                if attempt + 1 == self.retries:
                    self.error.emit(f"无法获取解析线路: {str(e)}")

class DownloadThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, video_url, save_path):
        super().__init__()
        self.video_url = video_url
        self.save_path = save_path

    def run(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            # 解析页面获取视频直链
            response = requests.get(self.video_url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            parser = etree.HTMLParser(encoding='utf-8')
            e = etree.HTML(response.text, parser=parser)
            
            # 尝试提取 <video> 标签的 src 或其他可能的视频链接
            video_src = e.xpath('//video/@src | //source/@src | //a[contains(@href, ".mp4")]/@href')
            if not video_src:
                raise ValueError("未找到视频资源链接")
            
            video_url = video_src[0]
            if not video_url.startswith('http'):
                # 处理相对路径
                from urllib.parse import urljoin
                video_url = urljoin(self.video_url, video_url)
            
            logger.debug(f"提取的视频直链: {video_url}")

            # 下载视频
            response = requests.get(video_url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(self.save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = int((downloaded_size / total_size) * 100)
                            self.progress.emit(progress)
            
            self.finished.emit(f"视频已保存到: {self.save_path}")
        except Exception as e:
            logger.error(f"下载失败: {str(e)}")
            self.error.emit(f"无法下载视频: {str(e)}")

class VIPParser(QWidget):
    def __init__(self):
        super().__init__()
        self.jiekdi = {}
        self.initUI()
        self.fetchLines()

    def initUI(self):
        self.setWindowTitle('B站风格VIP视频解析工具')
        icon_path = os.path.join(os.path.dirname(__file__), 'assets/bili_icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(600, 480)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f4f4f4"))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel('VIP视频在线解析')
        title.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #00A1D6; padding: 10px;')

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        line_layout = QHBoxLayout()
        line_label = QLabel('解析线路:')
        line_label.setFont(QFont('Microsoft YaHei', 10))
        line_label.setFixedWidth(80)

        self.combo = QComboBox()
        self.combo.setFont(QFont('Microsoft YaHei', 10))
        self.combo.setMinimumHeight(35)
        self.combo.setStyleSheet('''
            QComboBox {
                background-color: white;
                border: 1px solid #dcdfe6;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
            }
        ''')

        line_layout.addWidget(line_label)
        line_layout.addWidget(self.combo)

        input_layout = QHBoxLayout()
        url_label = QLabel('视频链接:')
        url_label.setFont(QFont('Microsoft YaHei', 10))
        url_label.setFixedWidth(80)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('粘贴VIP视频链接到这里...')
        self.url_input.setFont(QFont('Microsoft YaHei', 10))
        self.url_input.setMinimumHeight(35)
        self.url_input.setStyleSheet('''
            QLineEdit {
                background-color: white;
                border: 1px solid #dcdfe6;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
        ''')

        input_layout.addWidget(url_label)
        input_layout.addWidget(self.url_input)

        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.parse_btn = QPushButton('播放 VIP 视频')
        self.parse_btn.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        self.parse_btn.setFixedWidth(150)
        self.parse_btn.setMinimumHeight(45)
        self.parse_btn.setEnabled(False)
        self.parse_btn.setStyleSheet('''
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                  stop:0 #00A1D6, stop:1 #00C0FF);
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #00B5E2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        ''')
        self.parse_btn.clicked.connect(self.parseVideo)

        self.download_btn = QPushButton('下载视频')
        self.download_btn.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        self.download_btn.setFixedWidth(150)
        self.download_btn.setMinimumHeight(45)
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet('''
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                  stop:0 #00A1D6, stop:1 #00C0FF);
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #00B5E2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        ''')
        self.download_btn.clicked.connect(self.downloadVideo)

        button_layout.addStretch()
        button_layout.addWidget(self.parse_btn)
        button_layout.addWidget(self.download_btn)
        button_layout.addStretch()

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 1px solid #dcdfe6;
                border-radius: 5px;
                text-align: center;
                background-color: white;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                  stop:0 #00A1D6, stop:1 #00C0FF);
                border-radius: 5px;
            }
        ''')
        self.progress_bar.setVisible(False)

        self.status = QLabel('正在加载解析线路...')
        self.status.setFont(QFont('Microsoft YaHei', 9))
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet('color: #999999; font-size: 12px;')

        website_layout = QHBoxLayout()
        website_label = QLabel('视频网站:')
        website_label.setFont(QFont('Microsoft YaHei', 10))
        website_label.setFixedWidth(80)

        self.website_combo = QComboBox()
        self.website_combo.setFont(QFont('Microsoft YaHei', 10))
        self.website_combo.setMinimumHeight(35)
        self.website_combo.setStyleSheet('''
            QComboBox {
                background-color: white;
                border: 1px solid #dcdfe6;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
            }
        ''')

        websites = [
            ("哔哩哔哩", "http://www.bilibili.com/"),
            ("腾讯视频", "http://v.qq.com/"),
            ("爱奇艺", "http://www.iqiyi.com/"),
            ("优酷", "http://www.youku.com/"),
            ("芒果TV", "http://www.mgtv.com/")
        ]
        for name, url in websites:
            self.website_combo.addItem(name, url)

        self.redirect_btn = QPushButton('前往')
        self.redirect_btn.setFont(QFont('Microsoft YaHei', 10))
        self.redirect_btn.setFixedWidth(80)
        self.redirect_btn.setMinimumHeight(35)
        self.redirect_btn.setStyleSheet('''
            QPushButton {
                background-color: #00A1D6;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #00B5E2;
            }
        ''')
        self.redirect_btn.clicked.connect(self.redirectToWebsite)

        website_layout.addWidget(website_label)
        website_layout.addWidget(self.website_combo)
        website_layout.addWidget(self.redirect_btn)

        main_layout.addWidget(title)
        main_layout.addWidget(line)
        main_layout.addLayout(line_layout)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status)
        main_layout.addLayout(website_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def fetchLines(self):
        self.status.setText('正在加载解析线路...')
        self.parse_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        new_api_url = 'https://www.vimon.cc/tools/vip/'  # 请替换为实际接口
        self.thread = FetchThread(new_api_url, retries=3)
        self.thread.finished.connect(self.linesFetched)
        self.thread.error.connect(self.showError)
        self.thread.start()

    def linesFetched(self, lines):
        self.jiekdi = lines
        self.combo.clear()
        self.combo.addItems(self.jiekdi.keys())
        if self.jiekdi:
            self.status.setText(f'成功加载 {len(self.jiekdi)} 条解析线路')
            self.parse_btn.setEnabled(True)
            self.download_btn.setEnabled(True)
        else:
            self.status.setText('未获取到解析线路，请检查接口或网络')

    def showError(self, error_msg):
        self.status.setText(f'加载失败: {error_msg}')
        QMessageBox.critical(self, '错误', f'无法获取解析线路:\n{error_msg}')
        logger.error(f"显示错误: {error_msg}")

    def parseVideo(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '输入错误', '请输入视频链接')
            return
        selected = self.combo.currentText()
        if selected not in self.jiekdi:
            QMessageBox.warning(self, '选择错误', '请选择有效的解析线路')
            return
        full_url = self.jiekdi[selected] + url
        try:
            webbrowser.open(full_url)
            self.status.setText(f'已打开解析页面: {selected}')
            logger.debug(f"打开解析页面: {full_url}")
        except Exception as e:
            QMessageBox.critical(self, '打开失败', f'无法打开浏览器:\n{str(e)}')
            logger.error(f"打开浏览器失败: {str(e)}")

    def downloadVideo(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '输入错误', '请输入视频链接')
            return
        selected = self.combo.currentText()
        if selected not in self.jiekdi:
            QMessageBox.warning(self, '选择错误', '请选择有效的解析线路')
            return
        full_url = self.jiekdi[selected] + url

        # 创建 sp 文件夹
        sp_dir = os.path.join(os.path.dirname(__file__), 'sp')
        if not os.path.exists(sp_dir):
            os.makedirs(sp_dir)

        # 生成文件名（视频1.mp4, 视频2.mp4, ...）
        i = 1
        while True:
            save_path = os.path.join(sp_dir, f'视频{i}.mp4')
            if not os.path.exists(save_path):
                break
            i += 1

        self.status.setText('正在解析视频地址...')
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.parse_btn.setEnabled(False)
        self.download_btn.setEnabled(False)

        # 启动下载线程
        self.download_thread =DownloadThread(full_url, save_path)
        self.download_thread.finished.connect(self.downloadFinished)
        self.download_thread.error.connect(self.downloadError)
        self.download_thread.progress.connect(self.updateProgress)
        self.download_thread.start()

    def downloadFinished(self, message):
        self.status.setText(message)
        self.progress_bar.setVisible(False)
        self.parse_btn.setEnabled(True)
        self.download_btn.setEnabled(True)
        QMessageBox.information(self, '下载完成', message)

    def downloadError(self, error_msg):
        self.status.setText(f'下载失败: {error_msg}')
        self.progress_bar.setVisible(False)
        self.parse_btn.setEnabled(True)
        self.download_btn.setEnabled(True)
        QMessageBox.critical(self, '下载失败', error_msg)

    def updateProgress(self, progress):
        self.progress_bar.setValue(progress)
        self.status.setText(f'下载进度: {progress}%')

    def redirectToWebsite(self):
        index = self.website_combo.currentIndex()
        url = self.website_combo.itemData(index)
        if url:
            try:
                webbrowser.open(url)
                self.status.setText(f'已跳转到: {self.website_combo.currentText()}')
                logger.debug(f"跳转到网站: {url}")
            except Exception as e:
                QMessageBox.critical(self, '跳转失败', f'无法打开浏览器:\n{str(e)}')
                logger.error(f"跳转网站失败: {str(e)}")
        else:
            QMessageBox.warning(self, '错误', '该网站链接无效')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont('Microsoft YaHei', 10)
    app.setFont(font)
    parser = VIPParser()
    parser.show()
    sys.exit(app.exec_())