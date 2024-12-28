from setuptools import setup, find_packages
# Convert requirements.txt to UTF-8
with open("requirements.txt", "rb") as source_file:
    content = source_file.read()

with open("requirements.txt", "w", encoding="utf-8") as target_file:
    target_file.write(content.decode("utf-16"))  # Adjust 'utf-16' if another encoding is used


# Explicitly handle UTF-8 encoding when reading requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    required = f.read().splitlines()

setup(
    name="LibraryManagementSystem",
    version="0.1",
    packages=find_packages(),
    install_requires=required,  # Use cleaned dependency list
)

# Safely read requirements.txt with UTF-8 encoding
with open("requirements.txt", "r", encoding="latin-1") as f:
    required = f.read().splitlines()

setup(
    name="LibraryManagementSystem",
    version="0.1",
    packages=find_packages(),
    install_requires=required,  # Use cleaned dependency list
)

print("hii done")