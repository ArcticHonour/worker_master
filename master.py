import requests

print("welcome back master")
ngrok_url = input("Enter the ngrok public URL (e.g., https://5827-86-5-125-59.ngrok-free.app): ")

def send_command_to_worker(url, command):
    endpoint = f"{url}/execute"
    response = requests.post(endpoint, json={'command': command})

    if response.status_code == 200:
        result = response.json().get('result', 'No result received')
        print(f"Response from worker: {result}")
    else:
        print(f"Failed to communicate with worker. Status code: {response.status_code}")

def main():
    while True:
        # Prompt the user to enter a command
        command = input("Enter the Python command to send to the worker: ")
        
        # Send the command to the worker
        send_command_to_worker(ngrok_url, command)

if __name__ == '__main__':
    main()
