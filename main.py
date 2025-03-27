import os
import rotatescreen
from screeninfo import get_monitors
from enum import Enum

import threading
import pystray
from PIL import Image
import io

from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

class MonitorPosition(Enum):
    LANDSCAPE = "landscape" 
    PORTRAIT = "portrait" 
    LANDSCAPE_FLIPPED = "landscape_flipped" 
    PORTRAIT_FLIPPED = "portrait_flipped" 


POSITION_TO_ANGLE = {
    MonitorPosition.LANDSCAPE.value: 0,
    MonitorPosition.PORTRAIT.value: 90,
    MonitorPosition.LANDSCAPE_FLIPPED.value: 180,
    MonitorPosition.PORTRAIT_FLIPPED.value: 270
}


def create_tray_icon():
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    with open(icon_path, "rb") as f:
        image_data = f.read()
    icon_image = Image.open(io.BytesIO(image_data))
    
    def on_exit(icon, item):
        icon.stop()
        os._exit(0)
    
    menu = pystray.Menu(pystray.MenuItem("Sair", on_exit))
    tray_icon = pystray.Icon("Auto Rotate", icon_image, "Auto Rotate - SC", menu)
    tray_icon.run()

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

        if not data or 'monitor' not in data or 'position' not in data:
            return jsonify({
                'error': 'Dados inválidos. É necessário fornecer monitor e position'
            }), 400

        monitor_number = data['monitor']
        position = data['position']

        if position not in [pos.value for pos in MonitorPosition]:
            return jsonify({
                'error': 'Posição inválida. Posições válidas são: landscape, portrait, landscape_flipped, portrait_flipped'
            }), 400
        
        screens = rotatescreen.get_displays()
        
        if monitor_number < 0 or monitor_number >= len(screens):
            return jsonify({
                'error': f'Monitor {monitor_number} não encontrado. Total de monitores: {len(screens)}'
            }), 400

        screen = screens[monitor_number]  
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
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()
    
    app.run(host='0.0.0.0', port=5410, debug=False)