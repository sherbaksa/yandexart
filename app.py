from flask import Flask, render_template, request, jsonify, send_from_directory
from image_generator import generate_image_from_prompt
import os

app = Flask(__name__)

# Конфигурация
app.config['GENERATED_FOLDER'] = 'static/generated'
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint для генерации изображения"""
    try:
        data = request.get_json()
        style = data.get('style', '')
        description = data.get('description', '')

        if not style or not description:
            return jsonify({
                'success': False,
                'error': 'Необходимо указать стиль и описание'
            }), 400

        # Генерируем изображение
        image_path = generate_image_from_prompt(style, description)

        if image_path:
            # Возвращаем относительный путь для веб-приложения
            web_path = image_path.replace('static/', '')
            return jsonify({
                'success': True,
                'image_url': f'/{web_path}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Не удалось сгенерировать изображение'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/static/generated/<filename>')
def generated_file(filename):
    """Отдача сгенерированных изображений"""
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)