"""
DeepSeek OCR Flask 應用程式
使用 AlphaXiv API 進行 PDF OCR 處理
"""

import os
import sys
import logging
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# 將 src 目錄加入 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ocr_service import OCRService
from utils.file_validator import FileValidator

# 載入環境變數
load_dotenv()

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化 Flask 應用
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# 設定
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# 取得專案根目錄（src 的父目錄）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 設定上傳和輸出目錄為專案根目錄下的子目錄
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, os.getenv('UPLOAD_FOLDER', 'uploads'))
app.config['OUTPUT_FOLDER'] = os.path.join(project_root, 'outputs')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 16 * 1024 * 1024))

# 建立必要目錄
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 初始化服務
ocr_service = OCRService()


@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    處理檔案上傳和 OCR 處理
    """
    try:
        # 檢查是否有檔案
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '未選擇檔案'
            }), 400

        file = request.files['file']

        # 檢查檔案名稱
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '未選擇檔案'
            }), 400

        # 驗證檔案
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        is_valid, error_msg = FileValidator.validate_upload(file.filename, file_size)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400

        # 儲存上傳的檔案
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        logger.info(f"檔案已上傳: {upload_path}")

        # 處理 OCR
        result = ocr_service.process_document(
            upload_path,
            output_dir=app.config['OUTPUT_FOLDER']
        )

        # 清理上傳的檔案
        try:
            os.remove(upload_path)
        except Exception as e:
            logger.warning(f"無法刪除暫存檔案: {e}")

        if result['success']:
            return jsonify({
                'success': True,
                'markdown_content': result['markdown_content'],
                'output_file': os.path.basename(result['output_file']),
                'metadata': result['metadata']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', '處理失敗')
            }), 500

    except Exception as e:
        logger.error(f"上傳處理錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'伺服器錯誤: {str(e)}'
        }), 500


@app.route('/download/<filename>')
def download_file(filename):
    """
    下載處理後的 Markdown 檔案
    """
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))

        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': '檔案不存在'
            }), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/markdown'
        )

    except Exception as e:
        logger.error(f"下載錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'下載失敗: {str(e)}'
        }), 500


@app.route('/health')
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'service': 'DeepSeek OCR'
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """檔案過大錯誤處理"""
    return jsonify({
        'success': False,
        'error': '檔案過大，請上傳小於 16 MB 的檔案'
    }), 413


@app.errorhandler(500)
def internal_server_error(error):
    """內部伺服器錯誤處理"""
    logger.error(f"內部錯誤: {error}")
    return jsonify({
        'success': False,
        'error': '伺服器內部錯誤'
    }), 500


if __name__ == '__main__':
    # 預設使用 5001 端口（5000 在 macOS 上常被 AirPlay Receiver 佔用）
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV') == 'development'

    logger.info(f"啟動 Flask 應用於 port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
