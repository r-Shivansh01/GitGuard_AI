import os
import string
import random
import math
import numpy as np
import tensorflow as tf
import pandas as pd

# 1. GENERATE DATA
print("⚙️  Generating data...")
def generate_secret(length=20):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(chars) for _ in range(length))

safe_data = [
    "print('hello world')", "return True", "if x > 10:", "import numpy as np",
    "user_id = 5", "file_name.txt", "data['key']", "for i in range(10):",
    "def my_function():", "list.append(item)", "width = 100%", 
    "console.log('debug')", "background-color: #FFF", "var x = 10;"
]

unsafe_data = [generate_secret(random.randint(15, 30)) for _ in range(100)]
data = [[item, 0] for item in safe_data * 8] + [[item, 1] for item in unsafe_data]
df = pd.DataFrame(data, columns=["text", "label"]).sample(frac=1).reset_index(drop=True)

# 2. EXTRACT FEATURES
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

X = np.array([extract_features(t) for t in df['text']])
y = np.array(df['label'])

# 3. TRAIN
print("🧠 Training local brain...")
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=50, verbose=0)

# 4. SAVE
model.save('git_guard_model.h5')
print("✅ Success! New compatible model saved as 'git_guard_model.h5'")