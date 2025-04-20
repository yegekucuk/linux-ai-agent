import ollama
import os

def is_dangerous(command:str) -> bool:
    dangerous_keywords = ["rm -rf", ":(){", "mkfs", "dd if=", "shutdown", "reboot", "poweroff"]
    if any(danger in command for danger in dangerous_keywords):
        return True
    else:
        return False

def main():
    prompt = input()

    response = ollama.generate(
            model='linuxassistant',
            prompt=prompt
        )

    command = response["response"]
    command = command.strip().strip("```").replace("bash", "").strip()
    print(command)
    try:
        if is_dangerous(command):
            raise ValueError("Dangerous commands are not run.")
        os.system(f"echo '{command}' > linuxassistant.sh && chmod +x linuxassistant.sh && ./linuxassistant.sh")
    
    except ValueError as ve:
        print(ve)

    finally:
        os.system("rm linuxassistant.sh")

if __name__ == '__main__':
    main()