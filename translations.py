# -*- coding: utf-8 -*-
TRANSLATIONS = {
    'zh': {
        'title': '图片颜色分析工具',
        'select_files': '选择图片文件',
        'analyze': '分析颜色',
        'tips_folder': '请将需要分析的图片放在同一个文件夹中',
        'tips_formats': '支持的格式：JPG、JPEG、PNG、GIF、BMP、WebP、TIFF、HEIC',
        'tips_notice': '注意：① 无法多次选择或追加文件！② 动态图片只截取第一帧分析！',
        'primary_colors': '主色调分布',
        'secondary_colors': '辅助色分布',
        'error_no_file': '没有上传文件',
        'error_no_selection': '没有选择文件',
        'error_processing': '分析过程中发生错误',
        'error_chart': '生成颜色图表时出错',
        'help': '使用帮助',
        'help_title': '使用帮助 - 图片颜色分析工具',
        'help_basic_title': '基本使用',
        'help_basic_1': '点击"选择图片文件"按钮选择需要分析的图片',
        'help_basic_2': '支持同时选择多张图片进行分析',
        'help_basic_3': '分析结果会显示主色调和辅助色的分布情况',
        'help_formats_title': '支持的图片格式',
        'help_formats_1': 'JPG / JPEG',
        'help_formats_2': 'PNG（支持透明背景）',
        'help_formats_3': 'GIF（仅分析第一帧）',
        'help_formats_4': 'BMP',
        'help_formats_5': 'WebP',
        'help_formats_6': 'TIFF',
        'help_formats_7': 'HEIC',
        'help_notes_title': '注意事项',
        'help_notes_1': '建议将需要分析的图片放在同一个文件夹中',
        'help_notes_2': '一次性选择所有需要分析的图片',
        'help_notes_3': '图片大小没有严格限制，但会自动调整以优化性能',
        'help_notes_4': '分析结果包括颜色值和所占比例'
    },
    'en': {
        'title': 'Image Color Analyzer',
        'select_files': 'Select Image Files',
        'analyze': 'Analyze Colors',
        'tips_folder': 'Please put all images in the same folder',
        'tips_formats': 'Supported formats: JPG, JPEG, PNG, GIF, BMP, WebP, TIFF, HEIC',
        'tips_notice': 'Note: ① Cannot select or append files multiple times! ② For animated images, only the first frame will be analyzed!',
        'primary_colors': 'Primary Colors Distribution',
        'secondary_colors': 'Secondary Colors Distribution',
        'error_no_file': 'No file uploaded',
        'error_no_selection': 'No file selected',
        'error_processing': 'Error occurred during analysis',
        'error_chart': 'Error generating color chart',
        'help': 'Help',
        'help_title': 'Help - Image Color Analyzer',
        'help_basic_title': 'Basic Usage',
        'help_basic_1': 'Click "Select Image Files" button to choose images for analysis',
        'help_basic_2': 'Support analyzing multiple images at once',
        'help_basic_3': 'Results will show distribution of primary and secondary colors',
        'help_formats_title': 'Supported Image Formats',
        'help_formats_1': 'JPG / JPEG',
        'help_formats_2': 'PNG (supports transparency)',
        'help_formats_3': 'GIF (analyzes first frame only)',
        'help_formats_4': 'BMP',
        'help_formats_5': 'WebP',
        'help_formats_6': 'TIFF',
        'help_formats_7': 'HEIC',
        'help_notes_title': 'Notes',
        'help_notes_1': 'Recommended to put all images in the same folder',
        'help_notes_2': 'Select all images at once',
        'help_notes_3': 'No strict size limit, but images will be automatically resized for optimal performance',
        'help_notes_4': 'Results include color values and their percentages'
    }
}

def get_text(key, lang='zh'):
    """获取指定语言的文本"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['zh']).get(key, '')
