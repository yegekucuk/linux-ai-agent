import ollama
import os

# Function to check if given command is dangerous
def is_dangerous(command:str) -> bool:
    # List of keywords identifying dangerous commands
    dangerous_keywords = ["rm -rf", ":(){", "mkfs", "dd if=", "shutdown", "reboot", "poweroff"]
    # Return True if the command contains one of the keywords in the list.
    if any(danger in command for danger in dangerous_keywords):
        return True
    else:
        return False

def main():
    # Get the prompt
    prompt = input()
    # Take the command from the AI ​​model, the command in the model's response is extracted and cleaned
    response = ollama.generate(
            model='llama3-linuxassistant',
            prompt=prompt
        )
    command = response["response"]
    command = command.strip().strip("```").replace("bash", "").strip()
    print(command)
    
    try:
        # Raise an error if the command is dangerous
        if is_dangerous(command):
            raise ValueError("Dangerous commands are not run.")
        # Run the command
        os.system(f"echo '{command}' > linuxassistant.sh && chmod +x linuxassistant.sh && ./linuxassistant.sh")
    except ValueError as ve:
        # Print dangerous command warning
        print(ve)
    finally:
        # Delete the temporary created bash file
        os.system("rm linuxassistant.sh")

if __name__ == '__main__':
    main()