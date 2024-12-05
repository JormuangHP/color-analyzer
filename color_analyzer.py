import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io
import base64

def set_matplotlib_chinese_font():
    """设置 Matplotlib 中文字体"""
    try:
        # 优先使用思源黑体
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK', 'WenQuanYi Micro Hei']
        plt.rcParams['axes.unicode_minus'] = False
        print("Font set to Noto Sans CJK")  # 调试信息
    except Exception as e:
        # 备选字体
        chinese_fonts = ['Noto Sans CJK SC', 'Noto Sans CJK', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei']
        for font in chinese_fonts:
            try:
                if font in fm.findSystemFonts():
                    plt.rcParams['font.sans-serif'] = [font]
                    plt.rcParams['axes.unicode_minus'] = False
                    print(f"Using font: {font}")  # 调试信息
                    break
            except Exception as e:
                print(f"Error with font {font}: {str(e)}")  # 调试信息

class ColorAnalyzer:
    def __init__(self, n_colors=5):
        self.n_colors = n_colors
        self.primary_kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        self.secondary_kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        
    def process_image(self, image):
        """处理上传的图片文件对象"""
        try:
            img = Image.open(image)
            
            # 处理动图（如GIF），只取第一帧
            if hasattr(img, 'n_frames') and img.n_frames > 1:
                img.seek(0)
            
            # 转换颜色模式
            if img.mode in ['RGBA', 'LA']:
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img, mask=img.split()[1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整图片大小
            img.thumbnail((300, 300))
            
            return np.array(img)
            
        except Exception as e:
            raise ValueError(f"图片处理失败: {str(e)}")

    def get_colors(self, images):
        """分析多张图片的主色调和辅助色"""
        all_pixels = []
        error_files = []
        
        for image in images:
            try:
                img_array = self.process_image(image)
                pixels = img_array.reshape(-1, 3)
                valid_pixels = pixels[
                    (pixels.min(axis=1) > 10) &
                    (pixels.max(axis=1) < 245)
                ]
                if len(valid_pixels) > 0:
                    all_pixels.append(valid_pixels)
            except Exception as e:
                error_files.append(image.filename)
        
        if not all_pixels:
            raise ValueError("没有有效的图片可以分析")
        
        all_pixels = np.vstack(all_pixels)
        
        # 获取主色调
        self.primary_kmeans.fit(all_pixels)
        primary_colors = self.primary_kmeans.cluster_centers_.astype(float)
        
        primary_labels = self.primary_kmeans.labels_
        primary_counts = Counter(primary_labels)
        total_primary = sum(primary_counts.values())
        primary_percentages = {i: primary_counts[i]/total_primary 
                             for i in range(self.n_colors)}
        
        # 获取辅助色
        distances = np.zeros((len(all_pixels), len(primary_colors)))
        for i, center in enumerate(primary_colors):
            distances[:, i] = np.sqrt(np.sum((all_pixels - center) ** 2, axis=1))
        
        mask = distances.min(axis=1) > np.percentile(distances.min(axis=1), 40)
        secondary_pixels = all_pixels[mask]
        
        if len(secondary_pixels) > 0:
            self.secondary_kmeans.fit(secondary_pixels)
            secondary_colors = self.secondary_kmeans.cluster_centers_.astype(float)
            
            secondary_labels = self.secondary_kmeans.labels_
            secondary_counts = Counter(secondary_labels)
            total_secondary = sum(secondary_counts.values())
            secondary_percentages = {i: secondary_counts[i]/total_secondary 
                                  for i in range(self.n_colors)}
        else:
            secondary_colors = np.zeros((self.n_colors, 3))
            secondary_percentages = {i: 0 for i in range(self.n_colors)}
        
        return primary_colors, primary_percentages, secondary_colors, secondary_percentages
    
    def plot_colors_to_base64(self, primary_colors, primary_percentages, 
                             secondary_colors, secondary_percentages):
        """生成颜色分布图并转换为base64字符串"""
        import matplotlib
        matplotlib.use('Agg')
        
        # 设置中文字体
        set_matplotlib_chinese_font()
        
        # 创建新图形
        plt.clf()  # 清除当前图形
        
        # 创建图形和子图
        fig = plt.figure(figsize=(12, 4))
        ax1 = plt.subplot(211)  # 2行1列第1个
        ax2 = plt.subplot(212)  # 2行1列第2个
        
        try:
            # 绘制主色调
            current_height = 0
            sorted_primary = sorted(primary_percentages.items(), key=lambda x: x[1], reverse=True)
            for color_idx, percentage in sorted_primary:
                rgb = [c/255.0 for c in primary_colors[color_idx]]  # 确保RGB值在0-1之间
                ax1.barh(0, percentage, left=current_height, color=rgb, edgecolor='white')
                current_height += percentage
            
            ax1.set_xlim(0, 1)
            ax1.set_ylim(-0.5, 0.5)
            ax1.axis('off')
            ax1.set_title('主色调分布', pad=10)
            
            # 绘制辅助色
            current_height = 0
            sorted_secondary = sorted(secondary_percentages.items(), key=lambda x: x[1], reverse=True)
            for color_idx, percentage in sorted_secondary:
                rgb = [c/255.0 for c in secondary_colors[color_idx]]  # 确保RGB值在0-1之间
                ax2.barh(0, percentage, left=current_height, color=rgb, edgecolor='white')
                current_height += percentage
            
            ax2.set_xlim(0, 1)
            ax2.set_ylim(-0.5, 0.5)
            ax2.axis('off')
            ax2.set_title('辅助色分布', pad=10)
            
            # 调整布局
            plt.tight_layout(pad=2.0)
            
            # 保存图形
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, 
                       facecolor='white', edgecolor='none')
            plt.close(fig)
            
            # 获取图形数据
            buf.seek(0)
            return base64.b64encode(buf.getvalue()).decode('utf-8')
            
        finally:
            plt.close('all')  # 确保所有图形都被关闭
