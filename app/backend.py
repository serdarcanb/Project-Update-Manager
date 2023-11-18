from flask import Flask, request
import subprocess
import os 
from notification.discord import notification_send_message, notification_upload_message
from git import Repo
from git.exc import GitCommandError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PROJECT_NAME, PROJECT_DIRECTORY, UPLOAD_PATH, SERVICE_NAME, GITHUB_USERNAME, GITHUB_TOKEN = (
    os.getenv('PROJECT_NAME'),
    os.getenv('PROJECT_DIRECTORY'),
    os.getenv('UPLOUD_PATH'),  
    os.getenv('SERVICE_NAME'),
    os.getenv('GITHUB_USERNAME'),
    os.getenv('GITHUB_TOKEN')
)
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))


def main_backend():
    pull_result = git_pull()
    if pull_result:
        notification_send_message(f"Project {PROJECT_NAME} pulled.", CHANNEL_ID)
        run_command(PROJECT_DIRECTORY, "out.txt")
        notification_upload_message("out.txt", CHANNEL_ID)
        restart_systemd_service(SERVICE_NAME)
        notification_send_message(f"Project {PROJECT_NAME} updated.", CHANNEL_ID)
        return "Successfully updated and restarted!"
    else:
        notification_send_message("Project update failed.", CHANNEL_ID)
        return "Project update failed"

def git_pull():
    try:
        repo = Repo(PROJECT_DIRECTORY)
        repo.git.config('credential.username', GITHUB_USERNAME)
        repo.git.config('credential.helper', 'store')
        repo.git.config('credential.helper', f'!echo password={GITHUB_TOKEN}; echo')

        origin = repo.remotes.origin
        origin.fetch()

        current_branch = repo.active_branch
        old_commit = current_branch.commit
        repo.remotes.origin.pull()
        new_commit = current_branch.commit
        diff = repo.git.diff(old_commit, new_commit)
        with open('git_diff.txt', 'w') as diff_file:
            diff_file.write(diff)
   
        notification_upload_message("git_diff.txt", CHANNEL_ID)
        return True
    except GitCommandError:
        return False

def restart_systemd_service(service_name):
    try:
        subprocess.run(["systemctl", "restart", service_name], check=True, text=True, capture_output=True)
        return f"{service_name} successfully restarted."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.returncode}\n{e.stderr}"

def run_command(project_path, output_file):
    commands = [value for key, value in os.environ.items() if key.endswith("_COMMAND")]
    with open(output_file, "w") as f:
        for command in commands:
            try:
                f.write(f"Command: {command}\n") 
                result = subprocess.run(command.split(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=project_path)
                f.write(f"Output:\n{result.stdout.decode()}\n")
                f.write(f"Error:\n{result.stderr.decode()}\n")
                f.write("-" * 50 + "\n") 
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                f.write(f"Error: {e}\n")
