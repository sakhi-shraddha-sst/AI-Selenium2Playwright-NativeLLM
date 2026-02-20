from flask import Flask, render_template, request, jsonify, send_file
from tools.converter import Selenium2PlaywrightConverter
import os
import io

app = Flask(__name__, 
            template_folder='ui/templates',
            static_folder='ui/static')

converter = Selenium2PlaywrightConverter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    source_code = data.get('source_code', '')
    
    if not source_code:
        return jsonify({"status": "failure", "error": "No source code provided"}), 400
    
    result = converter.convert(source_code)
    return jsonify(result)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    code = data.get('code', '')
    filename = data.get('filename', 'converted_test.spec.ts')
    
    buffer = io.BytesIO()
    buffer.write(code.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(port=5001, debug=True)
