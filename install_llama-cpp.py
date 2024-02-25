import os
import requests
import subprocess
import sys
import zipfile

REPO_LLAMA_CPP = 'https://github.com/ggerganov/llama.cpp.git'
REPO_LLAMA_RELEASES = 'https://api.github.com/repos/ggerganov/llama.cpp/releases'
TORCH_VERSIONS = [
    {
        'url': 'https://download.pytorch.org/whl/cu121',
        'label': 'CUDA 12.1 for Windows'
    },
    {
        'url': 'https://download.pytorch.org/whl/cu118',
        'label': 'CUDA 11.8 for Linux and Windows' 
    },
    {
        'url': 'https://download.pytorch.org/whl/rocm5.7',
        'label': 'ROCm 5.7 for Linux'
    },
    {
        'url': 'https://download.pytorch.org/whl/cpu',
        'label': 'CPU only on Linux'
    },
    {
        'url': '',
        'label': 'Everything else'
    }
]

def show_choices(list_of_choices, message):
    print(message)
    for i, choice in enumerate(list_of_choices):
        print(f'{i+1}. {choice}')
    selection = -1
    while True:
        try:
            selection = int(input('Enter the number of your selection: '))
            if selection < 1 or selection > len(list_of_choices):
                raise ValueError
            break
        except ValueError:
            print("Invalid selection. Please enter a number between 1 and", len(list_of_choices))
    return selection

def main():
    # Introduction
    print("\nTo quantize with llama.cpp optimally (without having to install compilers on your device),")
    print("Python scripts and precompiled binaries are needed. The following steps will be taken.\n")
    print("1. Download the latest llama.cpp source code into the current directory.")
    print("2. Install the correct precompiled torch version.")
    print("3. Download the precompiled llama.cpp binary and extract into the llama.cpp folder.")
    print("4. Install the required Python packages.")
    input("\nPress any key to continue...\n\n")

    # Download the llama.cpp repository
    if os.path.exists('llama.cpp'):
        print("Updating the llama.cpp repository...")
        subprocess.run(['git', '-C', 'llama.cpp', 'pull'])
    else:
        print("Downloading the llama.cpp repository...")
        subprocess.run(['git', 'clone', REPO_LLAMA_CPP])

    # Download releases list
    response = requests.get(REPO_LLAMA_RELEASES)
    releases = response.json()
    latest_release = releases[0]
    assets = latest_release['assets']

    # Ask the user for the asset they would like to download
    print()
    list_of_assets = [asset['name'] for asset in assets]
    selection = show_choices(list_of_assets, "\nSelect the precompiled llama.cpp binaries to download: ")
    asset_url = assets[selection-1]['browser_download_url']
    print("Downloading", asset_url)
    response = requests.get(asset_url)
    with open('llama-cpp.zip', 'wb') as f:
        f.write(response.content)
        
    # Unzip the file into the llama.cpp folder
    with zipfile.ZipFile('llama-cpp.zip', 'r') as zip_ref:
        zip_ref.extractall('llama.cpp')
    print("\nllama.cpp binaries have been downloaded and extracted into the llama.cpp folder.\n")

    # Delete the zip now that it is extracted
    if os.path.exists('llama-cpp.zip'):
        os.remove('llama-cpp.zip')

    # Install the required Python packages
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'llama.cpp/requirements.txt'])
    print("\nPython packages have been installed.\n")

    # Install the correct precompiled torch version
    subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', 'torch', 'torchvision', 'torchaudio'])
    label_list = [version['label'] for version in TORCH_VERSIONS]
    selection = show_choices(label_list, "Select the version of PyTorch to install: ")
    if TORCH_VERSIONS[selection-1]['url'] == '':
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'torch', 'torchvision', 'torchaudio'])
    else:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'torch', 'torchvision', 'torchaudio', '--index-url', TORCH_VERSIONS[selection-1]['url']])

    print("\n\nllama.cpp has been installed successfully. You can now quantize your models.")

if __name__ == '__main__':
    main()
