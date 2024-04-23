import datetime
import difflib
import hashlib
import os
import shutil


class SimpleVCS:
    def __init__(self):
        self.repo_path = None
        self.repo_dir = ".simple_vcs"

    def __post_init__(self):
        if os.path.exists(self.repo_dir):
            self.repo_path = os.path.join(os.getcwd(), self.repo_dir)    

    def init(self):
        self.repo_path = os.path.join(os.getcwd(), self.repo_dir)
        os.makedirs(self.repo_path)
        print("Initialized empty repository in", self.repo_path)

    def hash_file(self, file_path):
        with open(file_path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()

    def add(self, file_path):
        if not self.repo_path:
            print("Repository not initialized. Please run 'init' first.")
            return

        file_hash = self.hash_file(file_path)
        dest_path = os.path.join(self.repo_path, os.path.basename(file_path))

        shutil.copyfile(file_path, dest_path)
        print(f"Added {file_path} to index")

    def commit(self, message):
        if not self.repo_path:
            print("Repository not initialized. Please run 'init' first.")
            return

        commit_hash = hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest()
        commit_dir = os.path.join(self.repo_path, "commits", commit_hash)
        os.makedirs(commit_dir)

        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                dest_path = os.path.join(commit_dir, os.path.relpath(file_path, self.repo_path))

                if os.path.isfile(file_path):
                    shutil.copyfile(file_path, dest_path)

        with open(os.path.join(commit_dir, "message.txt"), "w") as f:
            f.write(message)

        print("Committed changes with hash:", commit_hash)

    def log(self):
        if not self.repo_path:
            print("Repository not initialized. Please run 'init' first.")
            return

        commit_dir = os.path.join(self.repo_path, "commits")
        commits = sorted(os.listdir(commit_dir))

        previous_commit_files = None

        for commit in commits:
            with open(os.path.join(commit_dir, commit, "message.txt"), "r") as f:
                message = f.read()

            print(f"Commit: {commit}, Message: {message}")

            if previous_commit_files:
                print("\nChanges:")
                for file in previous_commit_files:
                    prev_file_path = os.path.join(self.repo_path, file)
                    current_file_path = os.path.join(commit_dir, commit, file)

                    with open(prev_file_path, "r") as prev_file:
                        prev_lines = prev_file.readlines()

                    with open(current_file_path, "r") as current_file:
                        current_lines = current_file.readlines()

                    diff = difflib.unified_diff(prev_lines, current_lines, lineterm='')
                    print("\n".join(diff))

            print("\n--------------------------------------------------")

            previous_commit_files = os.listdir(os.path.join(commit_dir, commit))


if __name__ == "__main__":
    vcs = SimpleVCS()
    while True:
        command = input("Enter command (init/add/commit/log/exit): ").strip().lower()

        if command == "init":
            vcs.init()
        elif command.startswith('add '):
            file_path = command.replace('add ', '')
            vcs.add(file_path)
        elif command.startswith('commit -m'):
            message = command.replace('commit -m', '')
            vcs.commit(message)
        elif command == "log":
            vcs.log()
        elif command == "exit":
            break
        else:
            print("Invalid command. Please try again.")
