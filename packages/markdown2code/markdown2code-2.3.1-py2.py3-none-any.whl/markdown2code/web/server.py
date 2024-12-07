from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
from ..converter import MarkdownConverter
from ..config import Config

def create_app(output_dir='uploads'):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = output_dir
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Ensure output directory exists
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/convert', methods=['POST'])
    def convert():
        try:
            if 'markdown_content' in request.form:
                # Save markdown content to project.md
                project_md_path = os.path.join(app.config['UPLOAD_FOLDER'], 'project.md')
                with open(project_md_path, 'w', encoding='utf-8') as f:
                    f.write(request.form['markdown_content'])
            elif 'file' in request.files:
                file = request.files['file']
                if file.filename:
                    # Save uploaded file as project.md
                    project_md_path = os.path.join(app.config['UPLOAD_FOLDER'], 'project.md')
                    file.save(project_md_path)
            else:
                return jsonify({'error': 'No content provided'}), 400

            # Convert markdown to code files
            config = Config()
            converter = MarkdownConverter(project_md_path, app.config['UPLOAD_FOLDER'], config)
            preview_info = converter.preview()
            
            # Convert with force=True to allow overwriting
            created_files = converter.convert(force=True)

            return jsonify({
                'message': 'Conversion successful',
                'created_files': created_files,
                'preview_info': preview_info
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app

def run_server(host='localhost', port=5000, output_dir='uploads'):
    """Run the markdown2code web server"""
    app = create_app(output_dir=output_dir)
    app.run(host=host, port=port, debug=True)
