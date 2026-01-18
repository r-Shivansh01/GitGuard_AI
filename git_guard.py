import sys
import os
import string
import math
import logging

# Hide TensorFlow startup logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import numpy as np
import tensorflow as tf

# --- 1. LOAD THE BRAIN ---
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'git_guard_model.h5')

try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    # If model fails, we fail safely (allow commit but warn user)
    print(f"⚠️ Warning: Git Guard AI is inactive. (Model not found)")
    sys.exit(0) 

# --- 2. THE TRANSLATOR ---
def calculate_entropy(text):
    if not text: return 0
    entropy = 0
    for x in range(256):
        p_x = float(text.count(chr(x))) / len(text)
        if p_x > 0: entropy += - p_x * math.log(p_x, 2)
    return entropy

def extract_features(text):
    length = len(text)
    if length == 0: return [0, 0, 0, 0]
    return [
        sum(c.isdigit() for c in text)/length,
        sum(c in string.punctuation for c in text)/length,
        sum(c.isupper() for c in text)/length,
        calculate_entropy(text)
    ]

# --- 3. THE SCANNER ---
def scan_file(filepath):
    # 1. Skip the guard script itself
    if "git_guard.py" in filepath: return True
    
    # 2. Skip the training script (It naturally contains fake secrets!)
    if "train_local.py" in filepath: return True

    print(f"🔍 Scanning {filepath}...", end=" ")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        max_score = 0
        suspicious_line = ""

        for line in lines:
            clean_line = line.strip()
            
            # --- NEW RULES ---
            if len(clean_line) < 8: continue       # Skip short lines
            if clean_line.startswith('#'): continue # Skip comments!
            # -----------------
            
            features = extract_features(line)
            score = model.predict([features], verbose=0)[0][0]
            
            if score > max_score:
                max_score = score
                suspicious_line = line

        # THRESHOLD: 0.50
        if max_score > 0.50: 
            print("🚨 UNSAFE!")
            print(f"   Line: '{suspicious_line.strip()}'")
            print(f"   Danger Score: {max_score:.4f}")
            return False 
        
        print("✅ Safe")
        return True
        
    except Exception as e:
        print(f"⚠️ Skipped")
        return True

# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    files_to_check = sys.argv[1:]
    if not files_to_check: sys.exit(0)

    print("\n--- 🛡️ GIT GUARD AI SCANNING ---")
    all_safe = True
    for file in files_to_check:
        if not scan_file(file):
            all_safe = False

    if not all_safe:
        print("\n🚫 BLOCKING COMMIT: Secrets detected!")
        sys.exit(1)
    else:
        print("\n✅ All Clear.")
        sys.exit(0)