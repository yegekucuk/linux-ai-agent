import ollama
import os
import argparse

# Function to check if given command is dangerous
def is_dangerous(command:str) -> bool:
    # Set lower case to avoid manupilating
    command = command.lower()
    # List of keywords identifying dangerous commands
    dangerous_keywords = [
        # These commands are banned
        "exec", "kill", "pkill", "shutdown", "reboot", "poweroff", "halt",
        # Prevent deletion of the system
        "rm -rf /", "rm -rf ~", "rm -rf /home", "--no-preserve-root", "rm *", "rm .*", "unlink",
        # Format & Partition Tools
        "mkfs", "parted", "fdisk", "cfdisk", "sgdisk", "sfdisk",
        # Disk Overwrite
        "dd", "wipefs", 
        # Fork Bomb
        ":(){", ":(){ :|:& };:", 
        # Shutdown & Reboot Commands
        "init 0", "init 6", 
        # Dangerous Permission Changes
        "chmod -r",
        # Firewall & Network Tampering
        "iptables -f", "iptables --flush", "ufw disable", "ufw reset", 
        "firewalld stop", "nft flush",
        # Infinite Loops
        "while true; do", "for ((;;)); do", "yes |",          
        # Secure Deletion Tools
        "shred", "wipe", "srm", "scrub"
    ]
    # Return True if any dangerous keyword is found in the input command
    return any(danger in command for danger in dangerous_keywords)

def main():
    # Argument Parsing
    parser = argparse.ArgumentParser(description="Linux Assistant Agent")
    parser.add_argument('--model', default='gemma', choices=['gemma', 'llama'], help='Choose your model: gemma or llama')
    args = parser.parse_args()
    model_name = f"{args.model}3-linuxassistant"

    # Get the prompt
    prompt = input("Type your prompt: ")
    # Exit the program with certain prompts
    if prompt in ['q',"quit","bye"]:
        exit(0)
    # Take the command from the AI ​​model, the command in the model's response is extracted and cleaned
    response = ollama.generate(
            model=model_name,
            prompt=prompt
        )
    command = response["response"]
    command = command.strip().strip("```").replace("bash", "").strip()
    print(f"\nCommand:\n{command}\n")
    try:
        # Raise an error if the command is dangerous
        if is_dangerous(command):
            raise ValueError("Dangerous commands are not run.")
        # Ask for validation
        validation:str = None
        while validation not in ["y", "", "yes", "n", "no"]:
            validation = str(input("Run the command? (Y/n): "))
            validation = validation.strip().lower()
        if validation in ["y", "", "yes"]:
            # Run the command
            os.system(f"echo '{command}' > linuxassistant.sh && chmod +x linuxassistant.sh && ./linuxassistant.sh")
            print("Successful.")
        else:
            raise ValueError("Permission denied.")
    except ValueError as ve:
        # Print the error
        print(ve)
    finally:
        # Check if linuxassistant.sh exists
        if os.path.exists("linuxassistant.sh"):
            # Remove the file
            os.remove("linuxassistant.sh")

if __name__ == '__main__':
    main()
