# Linux AI Agent

A smart Linux assistant that converts your instructions into shell commands and executes them safely.

![MIT License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM%20LinuxAssistant-orange)

Built with Meta Llama 3.

---

## 🧩 Features

- 🔍 Converts natural language prompts into Linux shell commands
- 🧠 Uses Ollama-powered, Llama3-based local LLM `llama3-linuxassistant`
- ✅ Filters out dangerous commands before execution
- ⚙️ Runs generated commands automatically via bash
- 🧼 Cleans up temporary files after execution
- 🖥️ Designed with security and usability in mind

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yegekucuk/linux-ai-agent.git
cd linux-ai-agent
```

### 2. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Pull Llama3 and create llama3-analyzer model from the Modelfile
The `llama3-linuxassistant` model is a derivative work based on Meta's Llama 3, customized through a local `Modelfile`. The base model is pulled using `ollama pull llama3`.

```bash
ollama pull llama3:latest
ollama create llama3-linuxassistant -f Modelfile
```

### 4. Run the Assistant

```bash
python main.py
```

Then enter your prompt, like:

```bash
List all .txt files in the current directory.
```

### 5. Set up command alias to use it anywhere (optional)

Add this code snippet to the `~/.bash_aliases` file. Set your path to the project as `your_path_to_the_project`.
```bash
alias agent='source ~/your_path_to_the_project/linux-ai-agent/venv/bin/activate && python3 ~/your_path_to_the_project/linux-agi-agent/main.py && deactivate'
```

---

## ⚠️ Safety First

Before executing a command, Linux AI Agent checks for potentially dangerous keywords like:

- `rm -rf`
- `mkfs`
- `dd if=`
- `shutdown`, `poweroff`, `reboot`

These commands are **blocked** from execution to protect your system.

---

## 📦 Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

Meta Llama 3 is licensed under the [Meta Llama 3 Community License](https://github.com/meta-llama/llama3/blob/main/LICENSE), Copyright © Meta Platforms, Inc. All Rights Reserved.

This is a personal project and this project is not affiliated with or endorsed by Meta.

