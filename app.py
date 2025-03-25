from flask import Flask, request, jsonify
from enum import Enum

app = Flask(__name__)

class MonitorPosition(Enum):
    LANDSCAPE = "landscape" # Paisagem normal
    PORTRAIT = "portrait" # Retrato normal
    LANDSCAPE_FLIPPED = "landscape_flipped" # Paisagem virado
    PORTRAIT_FLIPPED = "portrait_flipped" # Retrato virado

@app.route('/monitor', methods=['POST'])
def configure_monitor():
    try:
        data = request.get_json()

        print(data)
        
        # Validar os dados recebidos
        if not data or 'monitor' not in data or 'position' not in data:
            return jsonify({
                'error': 'Dados inválidos. É necessário fornecer monitor e position'
            }), 400

        monitor_number = data['monitor']
        position = data['position']

        # Validar se a posição é válida
        if position not in [pos.value for pos in MonitorPosition]:
            return jsonify({
                'error': 'Posição inválida. Posições válidas são: landscape, portrait, landscape_flipped, portrait_flipped'
            }), 400

        # Aqui você pode adicionar a lógica para configurar o monitor
        # Por enquanto, apenas retornamos os dados recebidos
        return jsonify({
            'status': 'success',
            'message': f'Monitor {monitor_number} configurado para posição {position}',
            'data': {
                'monitor': monitor_number,
                'position': position
            }
        })

    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar requisição: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 