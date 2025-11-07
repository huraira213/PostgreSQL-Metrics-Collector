# debug_paths.py
import os

print("Current Working Directory:", os.getcwd())
print("Files in this directory:")
for file in os.listdir('.'):
    print(f" - {file}")