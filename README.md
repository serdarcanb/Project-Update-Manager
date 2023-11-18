# Project Update Manager

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/release)
[![Docker](https://img.shields.io/badge/docker-supported-brightgreen.svg)](https://www.docker.com/)

<p align="center">
  <img src="images/project_update_manager.png" alt="Project Update Manager">
</p>

## Overview

The Project Update Manager is a flexible tool written in Python using Flask, designed to streamline the process of updating projects on a Linux environment. By utilizing the `/update-project` endpoint with a POST request and a specified `SAFE_TOKEN`, the system triggers the update process. All commands are provided through the `.env` file, offering a high degree of customization for different projects.

## Features

- **Automated Builds**: The system automatically fetches updates, performs builds, and restarts the associated service upon receiving a valid request.

- **Configuration via .env**: Project-specific configurations are stored in the `.env` file, providing a simple and centralized way to manage settings.

- **Integration with Discord Bot**: Receive notifications on Discord by integrating a bot. The system can send build outputs and Git diff results to a specified channel.

## How It Works

1. **Endpoint**: Send a POST request to the `/update-project` endpoint with the appropriate `SAFE_TOKEN`.

2. **Command Execution**: Commands for updating and building are specified in the `.env` file. The system executes these commands on the Linux environment.

3. **Service Restart**: After a successful build, the associated service is restarted, ensuring the changes take effect.

4. **Discord Integration**: Optionally, integrate with a Discord bot to receive notifications. Build outputs and Git diff results can be sent to a designated Discord channel.

## Usage

Clone the repository:

   git clone https://github.com/serdarcanb/Project-Update-Manager.git
   cd Project-Update-Manager

Set up the .env file with your project-specific configurations.

Start the Flask application:
    pip install -r requirements.txt
    python main.py

Make a POST request to the /update-project endpoint with the SAFE_TOKEN to trigger the update process.

Docker Usage: Build and run the Docker container:

    docker build -t project-update-manager .
    docker run -p 8080:8080 -d project-update-manager

updateder.service Usage: Create and start the updateder.service systemd service:

    sudo cp updateder.service /etc/systemd/system/
    sudo systemctl start updateder.service

To enable auto-start on boot:

    sudo systemctl enable updateder.service

## Configuration Example (.env)

    # Web App
    WEB_APP_HOST = '0.0.0.0' 
    WEB_APP_PORT = 8080

    #Github
    PROJECT_URL = "https://github.com/my-org/my-repo.git"
    PROJECT_DIRECTORY = '/root/projectfile'
    UPLOUD_PATH = 'out.txt'
    GITHUB_USERNAME = 'github-username'
    GITHUB_TOKEN = 'github-token'
    PROJECT_NAME = "my-repo"
    SERVICE_NAME = "service_name.service"

    # Security
    SAFE_TOKEN = "Random safe token"
    DISCORD_TOKEN= "bot_token"
    DISCORD_CHANNEL_NAME= "channel_name"
    CHANNEL_ID= "channel_id"


    #command
    1_COMMAND = "npm install"
    TEST_COMMAND = "echo donee"
## Contributions
Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

