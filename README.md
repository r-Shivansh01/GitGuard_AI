# 🛡️ GitGuard AI: Neural Network Secret Scanner

**GitGuard AI** is an intelligent security tool that integrates directly into your Git workflow. It uses a **Deep Learning model (TensorFlow)** to scan your code commits for accidentally leaked secrets—such as API keys, passwords, and access tokens—before they ever leave your computer.

Unlike traditional security tools that rely on rigid "Regular Expressions" (Regex), GitGuard uses **Shannon Entropy** and statistical feature extraction to detect *any* high-entropy string, even if it has never seen that specific format before.

---

## 🚀 Key Features

* **🧠 AI-Powered Detection:** Runs a pre-trained Neural Network on every line of code you commit.
* **📊 Shannon Entropy Analysis:** Mathematically calculates the "chaos" of a string to distinguish between safe code (predictable) and secrets (random).
* **🚫 Automated Blocking:** Hooks into `git commit` to block the process immediately if a threat is detected.
* **🔒 Local Execution:** The model runs 100% offline on your machine. Your data never touches the cloud.
* **⚡ Lightweight:** Optimized model loads in milliseconds.

---

## 🛠️ Installation Guide

Follow these steps to set up GitGuard AI on your local machine.

### Prerequisites
* **Python 3.9+** installed.
* **Git** installed and initialized in your project.

### Step 1: Clone the Repository
Download the project code and the pre-trained brain (`.h5` file).
```bash
git clone [https://github.com/r-Shivansh01/GitGuard_AI.git](https://github.com/r-Shivansh01/GitGuard_AI.git)
cd GitGuard_AI
```
### Step 2: Install Dependencies
GitGuard relies on TensorFlow for the brain and NumPy for the math.

```bash

# Windows
py -m pip install tensorflow numpy pandas

# Mac/Linux
pip3 install tensorflow numpy pandas
Note: If you encounter version errors, try installing specific versions: pip install tensorflow==2.15.0 numpy<2
```

### Step 3: Activate the Guard (The Git Hook)
This step wires the Python script into your Git system so it runs automatically.
```
For Windows (PowerShell):

PowerShell

# Copy the hook file into your hidden .git folder
Copy-Item hooks/pre-commit .git/hooks/pre-commit
For Mac/Linux:
```
```bash

cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## ⚙️ How It Works (The Science)
GitGuard does not "read" code like a human. It converts text into mathematical vectors based on 4 key features:

Digit Density: How many numbers are in the string? (password123 vs password)

Symbol Density: Frequency of characters like !@#$%.

Uppercase Ratio: Secrets often use random capitalization (aB3dE vs print).

Shannon Entropy: A measure of unpredictability.

print('hello') → Low Entropy (Safe)

x8!2kaPv9@ → High Entropy (Dangerous)

The Neural Network (3-layer Dense Model) processes these 4 numbers and outputs a Danger Score between 0.0 and 1.0. If the score exceeds 0.5, the commit is blocked.

## 🧪 Testing the Guard
Once installed, you can verify it works by trying to commit a "fake" secret.

Create a file named test_secret.py.

Add a line that looks like a high-security key:

Python

aws_key = "AKIA_8291_RANDOM_SECRET_KEY_!!!2"
Try to commit it :

```bash

git add test_secret.py
git commit -m "Testing the guard"
Expected Output:

Plaintext

🛡️  Git Guard is scanning...
🔍 Scanning test_secret.py... 
🚨 UNSAFE!
   Line: 'aws_key = "AKIA_8291_RANDOM_SECRET_KEY_!!!2"'
   Danger Score: 0.9821

🚫 BLOCKING COMMIT: Secrets detected!
```

## 🔧 Troubleshooting
1. "Pip not recognized" Ensure Python is added to your system PATH, or try running commands with python -m pip instead of just pip.

2. The Hook isn't triggering Make sure the file inside .git/hooks/pre-commit has no file extension (it should not be .txt or .py).

3. "TensorFlow version mismatch" If you see an error about the model file format, simply run the local trainer to rebuild the brain for your specific computer:


```bash
py train_local.py
```

## 👨‍💻 Author
Shivansh Rao.

https://github.com/r-Shivansh01

Project built with Python, TensorFlow, and Git Hooks.
