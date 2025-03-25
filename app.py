from flask import Flask, request, jsonify, render_template
from enum import Enum
import rotatescreen
from screeninfo import get_monitors

app = Flask(__name__)

class MonitorPosition(Enum):
    LANDSCAPE = "landscape" # Paisagem normal
    PORTRAIT = "portrait" # Retrato normal
    LANDSCAPE_FLIPPED = "landscape_flipped" # Paisagem virado
    PORTRAIT_FLIPPED = "portrait_flipped" # Retrato virado

# Mapeamento de posições para ângulos
POSITION_TO_ANGLE = {
    MonitorPosition.LANDSCAPE.value: 0,
    MonitorPosition.PORTRAIT.value: 90,
    MonitorPosition.LANDSCAPE_FLIPPED.value: 180,
    MonitorPosition.PORTRAIT_FLIPPED.value: 270
}

def get_monitor_info():
    system_monitors = get_monitors()
    
    monitors_info = []
    for idx, monitor in enumerate(system_monitors):
        monitor_info = {
            'id': idx,
            'name': monitor.name if monitor.name else f'Monitor {idx}',
            'width': monitor.width,
            'height': monitor.height,
            'width_mm': monitor.width_mm,
            'height_mm': monitor.height_mm,
            'is_primary': monitor.is_primary,
            'resolution': f'{monitor.width}x{monitor.height}',
            'aspect_ratio': f'{monitor.width/monitor.height:.2f}:1'
        }
        monitors_info.append(monitor_info)
    
    return monitors_info

@app.route('/', methods=['GET'])
def home():
    monitors_info = get_monitor_info()
    return render_template('index.html',
                         monitors=monitors_info,
                         positions=[pos.value for pos in MonitorPosition])

@app.route('/monitors', methods=['GET'])
def get_monitors_info():
    try:
        monitors_info = get_monitor_info()
        return jsonify({
            'status': 'success',
            'data': monitors_info
        })
    except Exception as e:
        return jsonify({
            'error': f'Erro ao obter informações dos monitores: {str(e)}'
        }), 500

@app.route('/monitor', methods=['POST'])
def configure_monitor():
    try:
        data = request.get_json()
        
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

        # Configurar a rotação do monitor
        screens = rotatescreen.get_displays()  # Pega todos os monitores
        
        # Verificar se o número do monitor é válido
        if monitor_number < 0 or monitor_number >= len(screens):
            return jsonify({
                'error': f'Monitor {monitor_number} não encontrado. Total de monitores: {len(screens)}'
            }), 400

        screen = screens[monitor_number]  # Seleciona o monitor específico
        angle = POSITION_TO_ANGLE[position]
        screen.rotate_to(angle)

        return jsonify({
            'status': 'success',
            'message': f'Monitor {monitor_number} configurado para posição {position}',
            'data': {
                'monitor': monitor_number,
                'position': position,
                'total_monitors': len(screens)
            }
        })

    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar requisição: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True) 