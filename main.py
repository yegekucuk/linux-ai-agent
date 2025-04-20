import ollama
import os

prompt = input()

response = ollama.generate(
        model='linuxassistant',
        prompt=prompt
    )

command = response["response"]
print(command)
try:
    os.system(f"echo '{command}' > linuxassistant.sh && chmod +x linuxassistant.sh && ./linuxassistant.sh")

finally:
    os.system("rm linuxassistant.sh")