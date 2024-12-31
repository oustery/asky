# AskY: Your Console AI Assistant

AskY is a simple and efficient command-line AI assistant designed to answer your questions. Powered by the Gemini API, AskY provides quick and accurate responses directly from your terminal.

---

## Features
- **AI Question Answering**: Instantly get answers to your queries by running a single command.
- **Easy API Key Configuration**: Set your Gemini API key effortlessly with a command-line argument.
- **Lightweight and Fast**: No GUI needed; everything works directly in the terminal.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/asky.git
   cd asky
   ```

2. Ensure you have Python installed (>= 3.7).

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Set Your API Key
To configure the Gemini API key, use the `--set-api-key` argument:
```bash
python asky.py --set-api-key YOUR_GEMINI_API_KEY
```
This stores your API key securely for future use.

### 2. Ask a Question
Run the following command to ask a question:
```bash
python asky.py "Your question here"
```
For example:
```bash
python asky.py "What is the capital of France?"
```

### 3. Help Menu
To see the available options, use:
```bash
python asky.py --help
```

---

## Example Output
Input:
```bash
python asky.py "What is the speed of light?"
```
Output:
```plaintext
The speed of light is approximately 299,792 kilometers per second (km/s).
```

---

## Configuration
- API Key: The API key is securely stored in a local configuration file (e.g., `config.json`).

---

## Contributing
Feel free to submit issues and pull requests! Contributions are welcome to improve functionality, performance, and usability.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Gemini API for powering the AI capabilities.
- The open-source community for inspiration and support.
