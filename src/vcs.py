import datetime
import difflib
import hashlib
import os
import shutil

from diff import get_the_difference


class SimpleVCS:
    def __init__(self):
        self.repo_path = None
        self.repo_dir = ".simple_vcs"
        self.current_branch = "master"
        self.branches = {"master": "master"}

    def __post_init__(self):
        if os.path.exists(self.repo_dir):
            self.repo_path = os.path.join(os.getcwd(), self.repo_dir)    

    def init(self):
        self.repo_path = os.path.join(os.getcwd(), self.repo_dir)
        os.makedirs(self.repo_path, exist_ok=True)
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

    def get_list_commit(self):
        commit_dir = os.path.join(self.repo_path, "commits")
        commits = os.listdir(commit_dir)

        return commits.sort(key=lambda x: os.path.getmtime(x))

    def commit(self, message):
        if not self.repo_path:
            print("Repository not initialized. Please run 'init' first.")
            return

        commit_hash = hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest()
        commit_dir = os.path.join(self.repo_path, "commits", commit_hash)
        os.makedirs(commit_dir)

        added_files = [f for f in os.listdir(self.repo_path) if os.path.isfile(os.path.join(self.repo_path, f))]

        for file_name in added_files:
            file_path = os.path.join(self.repo_path, file_name)
            dest_path = os.path.join(commit_dir, file_name)
            shutil.copyfile(file_path, dest_path)

        with open(os.path.join(commit_dir, "message.txt"), "w") as f:
            f.write(message)

        with open(os.path.join(self.repo_path ,"history/commits.txt"), "w") as f:
            f.write(f'commit_hash \n')

        print(f"Committed changes to branch '{self.current_branch}' with hash:", commit_hash)

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
            commit_list = vcs.get_list_commit()
            print(get_the_difference(file_path_1=commit_list[-1]+'example.csv',
                                     file_path_2=commit_list[-2]+'example.csv'))
        elif command == "log":
            vcs.log()
        elif command == "exit":
            break
        else:
            print("Invalid command. Please try again.")
