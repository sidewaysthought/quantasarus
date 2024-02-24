import argparse
from huggingface_hub import hf_hub_download

def download(model):
    pass

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

if __name__ == "__main__":
    main()


