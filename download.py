import tempfile
import os
import shutil
import urllib.request
import tarfile
import json
import argparse

def get_latest_tag(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        return data.get("tag_name")

def main():
    parser = argparse.ArgumentParser(description="Greet someone.")
    parser.add_argument("--owner", "-o", default="", type=str, help="The owner of the repository")
    parser.add_argument("--repo", "-r", default="", type=str, help="Target repository")
    parser.add_argument("--file", "-f", default="", type=str, help="The target file")
    parser.add_argument("--version", "-v", default="v3", type=str, help="The version the linux architecture")
    args = parser.parse_args()

    if args.owner == "" or args.repo == "" or args.file == "":
        return

    temp_dir = tempfile.gettempdir()

    print(f"System temporary directory: {temp_dir}")

    my_temp_dir = os.path.join(temp_dir, "my_temp_dir")
    os.makedirs(my_temp_dir, exist_ok=True)
    print(f"Created subdirectory: {my_temp_dir}")

    tag_name = get_latest_tag("domaingts", "tutorial")
    print(f"Get tag name: {tag_name}")

    tuto = f"https://github.com/{args.owner}/{args.repo}/releases/download/{tag_name}/{args.file}-linux-amd64-{args.version}.tar.gz"

    my_file_path = os.path.join(my_temp_dir, f"{args.file}.tar.gz")

    with urllib.request.urlopen(tuto) as response, open(my_file_path, 'wb') as out_file:
        out_file.write(response.read())

    print(f"Downloaded to {my_file_path}")

    if tarfile.is_tarfile(my_file_path):
        with tarfile.open(my_file_path, "r:gz") as tar:
            tar.extractall(path=my_temp_dir)
        print(f"Extracted to: {my_file_path}")

    shutil.rmtree(my_temp_dir)
    print("Cleaned up temporary files and folder.")

main()
