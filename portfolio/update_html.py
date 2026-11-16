import os
import re

dir_path = "c:/Users/amokr/Documents/portfolio"

def process_files():
    for filename in os.listdir(dir_path):
        if filename.endswith(".html"):
            filepath = os.path.join(dir_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace expressions
            content = re.sub(r"Rosa\s+Amokrane", "ROSA", content, flags=re.IGNORECASE)
            content = re.sub(r"ROSA_AMOKRANE", "ROSA", content, flags=re.IGNORECASE)
            content = re.sub(r"rosa-amokrane", "rosa", content, flags=re.IGNORECASE)
            # Remove any orphan "amokrane" left
            content = re.sub(r"\s*amokrane", "", content, flags=re.IGNORECASE)
            
            # Remove img tags
            content = re.sub(r"<img[^>]*>", "", content, flags=re.IGNORECASE)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    process_files()
    print("Replacements done for HTML files.")
