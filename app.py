from flask import Flask, request, jsonify, redirect, url_for, render_template
import subprocess
import os

app = Flask(__name__)

# Diccionario que mapea el nombre de la herramienta con el archivo Python correspondiente y el puerto
TOOLS = {
    'tool1': {'script': 'MapaCalor_AI_PRE.py', 'port': 8501},
    'tool2': {'script': 'MapaCalor_Transitions.py', 'port': 8502},
    'tool3': {'script': 'MapaCalor_compareEvents.py', 'port': 8503}
}


# Ruta para servir la página principal
@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de que index.html esté en la carpeta 'templates'

# Ruta para recibir la solicitud de lanzar una herramienta
@app.route('/launch', methods=['POST'])
def launch_tool():
    try:
        data = request.get_json()
        tool_name = data.get('tool')
        
        if tool_name in TOOLS:
            tool_script = TOOLS[tool_name]['script']
            port = TOOLS[tool_name]['port']
            
            # Comando para levantar Streamlit en el puerto específico
            command = f"py -3.9 -m streamlit run {tool_script} --server.port={port} --server.enableXsrfProtection false --server.headless true"
            
            # Lanza el proceso en segundo plano
            subprocess.Popen(command, shell=True)

            # Redirigir al puerto donde se está ejecutando la herramienta
            streamlit_url = f"http://127.0.0.1:{port}"
            return jsonify({'status': 'success', 'url': streamlit_url})
        else:
            return jsonify({'status': 'error', 'message': 'Herramienta no encontrada.'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
