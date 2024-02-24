import argparse
import os
from huggingface_hub import hf_hub_download, snapshot_download

BASE_MODEL_DIR = "models"

def download(repo, file=""):

    # If the model dir doesn't exist, create it
    if not os.path.exists("models"):
        os.makedirs("models")

    if file != "":
        # Split the repo on the / to get the owner and model name
        repo_split = repo.split("/")
        owner = repo_split[0]
        model = repo_split[1]
        dest_path = os.path.join(BASE_MODEL_DIR, owner, model)
    else:
        dest_path = os.path.join(BASE_MODEL_DIR, owner)

    try:
        if file == "":
            snapshot_download(repo_id=repo, local_dir=dest_path)
        else:
            hf_hub_download(repo_id=repo, filename=file, local_dir=dest_path)
    except Exception as e:
        print(f"Error: {e}")
        exit()

def quatize_gguf(model):
    pass

def setup_args():
    args = argparse.ArgumentParser(description="Quantasarus", epilog="Quantasarus is a tool for quantizing HuggingFace models")
    args.add_argument("--repo", type=str, help="The HuggingFace repository to download from", required=True)
    args.add_argument("--file", type=str, help="The file to download from the repository", default="")
    return args.parse_args()

def validate_args(args):
    arg_values = {
        "repo": args.repo,
        "file": args.file
    }
    return arg_values

def main():
    args = setup_args()
    arg_values = validate_args(args)
    downloaded = download(arg_values["repo"], arg_values["file"])

if __name__ == "__main__":
    main()


