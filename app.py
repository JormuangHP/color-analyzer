from flask import Flask, render_template, request, jsonify
from color_analyzer import ColorAnalyzer
from translations import get_text

app = Flask(__name__)
app.secret_key = '5ba9bde4d1f3f911095249565141623b'  # 请替换为你生成的密钥

@app.route('/')
def index():
    lang = request.args.get('lang', 'zh')
    return render_template('index.html', 
                           lang=lang, 
                           get_text=lambda key: get_text(key, lang))

@app.route('/help')
def help_page():
    lang = request.args.get('lang', 'zh')
    return render_template('help.html', 
                           lang=lang, 
                           get_text=lambda key: get_text(key, lang))

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'files[]' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    files = request.files.getlist('files[]')
    if not files:
        return jsonify({'error': '没有选择文件'}), 400
    
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff', 'heic'}
    for file in files:
        if not file.filename.lower().split('.')[-1] in allowed_extensions:
            return jsonify({'error': f'不支持的文件格式: {file.filename}'}), 400
    
    analyzer = ColorAnalyzer(n_colors=5)
    
    try:
        primary_colors, primary_percentages, secondary_colors, secondary_percentages = \
            analyzer.get_colors(files)
        
        # 对主色调数据进行排序
        primary_pairs = [(i, primary_percentages[i]) for i in range(len(primary_colors))]
        primary_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # 对辅助色数据进行排序
        secondary_pairs = [(i, secondary_percentages[i]) for i in range(len(secondary_colors))]
        secondary_pairs.sort(key=lambda x: x[1], reverse=True)
        
        try:
            plot_base64 = analyzer.plot_colors_to_base64(
                primary_colors, primary_percentages,
                secondary_colors, secondary_percentages
            )
        except Exception as e:
            print(f"生成图表时出错: {str(e)}")
            return jsonify({'error': '生成图表时出错'}), 500
        
        # 格式化返回数据
        result = {
            'primary_colors': [
                {
                    'rgb': [int(c) for c in primary_colors[idx]],
                    'percentage': percentage * 100
                }
                for idx, percentage in primary_pairs
            ],
            'secondary_colors': [
                {
                    'rgb': [int(c) for c in secondary_colors[idx]],
                    'percentage': percentage * 100
                }
                for idx, percentage in secondary_pairs
            ],
            'plot': plot_base64
        }
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"分析过程中出错: {str(e)}")
        return jsonify({'error': '分析过程中出错'}), 500

if __name__ == '__main__':
    app.run(debug=True)