# Postodon
A python-based bot for Mastodon

# Development

Below are the steps required to get started in working on Postodon

## Requirements

- Python
- Docker

### Python 

**Minimum required version: 3.12**

#### macOS: 

1. **Install Homebrew** (if you haven’t already):
   Open the Terminal and run the following command:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. **Install Python**:
    ```bash
    brew install python
    ```

#### Windows:

1. Download Python:
    a. Go to the [official Python website](https://www.python.org/downloads/windows/).
    b. Download the latest Python installer (e.g., python-3.x.x.exe).
2. Install Python
    a. Open the downloaded installer from your Downloads folder
    b. Check the box **"Add Python to PATH"**
    c. Click **Install Now**


**Linux: Most distributions come with Python preinstalled.**


### Docker

Install Docker Desktop from the official website 

[Windows](https://docs.docker.com/desktop/install/windows-install/)

[macOS](https://docs.docker.com/desktop/install/mac-install/)

[Ubuntu](https://docs.docker.com/engine/install/ubuntu/), [Debian](https://docs.docker.com/engine/install/debian/), [Fedora](https://docs.docker.com/engine/install/fedora/), [CentOS](https://docs.docker.com/engine/install/centos/)

## Running
Set up your `.env` file with the following values:
```
flask_secret_key="MYSUPERSECRETKEY"
domain="127.0.0.1"
port=5001
env=debug
interval=86400
```

## Running via Python

`python src/app.py`

## Running via Docker

1. `docker build -t postodon:latest .`

2. `docker run -p 5001:5001 --env-file ./.env postodon:latest`

# Production

This project is still in a very basic alpha phase. There *will* be pitfalls and errors and things *will* break. 

# Colour palette

This is the basic colour palette being used at the moment. Anyone is free to come up with a better one. Eventually I'll make it possible to specify the colour palette via the .env file.

https://coolors.co/37b7c3-982649-05668d-679436-a5be00

