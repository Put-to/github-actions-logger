  # GitHub Webhook Event Receiver
This project is designed to receive GitHub webhooks for specific events (Push, Pull Request, and Merge), store the events in MongoDB, and display the latest updates on the frontend. The project uses Flask for the backend, MongoDB for storing events, and basic HTML/CSS/JavaScript for the frontend.


## Features
- Receives webhook events for:
  - Push events: Triggered when commits are pushed to a branch.
  - Pull Request events: Triggered when a pull request is opened or updated.
  - Merge events: Triggered when a pull request is merged.
- Stores events in MongoDB.
- Frontend polls the latest events every 15 seconds and displays them in a user-friendly format.

## Prerequisites
To run this project, you need to have the following installed:
- Python 3.x
- Flask (Python web framework)
- MongoDB (Database)
- Docker (Optional, for running MongoDB in a container)
- GitHub account (to configure webhooks)

# Getting Started

- ## Clone the Repositories. You need to have two repositories:

  - Webhook Receiver (this repo): Handles receiving webhooks from GitHub.
  - Action Repo: A sample GitHub repository where events like Push, Pull Request, and Merge actions will trigger webhooks.

```
git clone https://github.com/put-to/webhook-repo.git
cd webhook-repo
```

- ## Set up MongoDB: You can run MongoDB locally or use Docker to set it up.

Run MongoDB in Docker
To start MongoDB in a Docker container:
```
docker run -d -p 27017:27017 --name mongodb mongo:latest
```
Create a MongoDB Database
Once MongoDB is running, create a database called webhook_events
```
docker exec -it mongodb mongosh
use webhook_events
```
- ## Set Up Python Environment
Install the required Python packages
```
pip install -r requirements.txt
```
- ## Configure Flask App
In the app/extensions.py file, configure the MongoDB connection:
```
from flask_pymongo import PyMongo

# MongoDB URI
mongo = PyMongo(uri="mongodb://localhost:27017/webhook_events")
```
- ## Run the Flask App
Run the Flask app to start receiving webhooks:
```
python run.py
```
The app will be running on http://localhost:5000.

- ## Set Up ngrok (For Local Development)
To receive webhooks from GitHub on your local machine, use ngrok to expose your local server to the internet:

- Download and install ngrok from ngrok's website.
- Start ngrok with the following command:
- ```
  ngrok http 5000
  ```
- You will get a forwarding URL like http://<your-ngrok-id>.ngrok.io. Copy this URL

- ## Set Up GitHub Webhook
- Go to the settings of your Action Repo.
- Navigate to Webhooks > Add webhook.
- Set the webhook URL to:
- ```
  http://<your-ngrok-id>.ngrok.io/webhook/receiver
  ```
- Choose to trigger the webhook for:
  - Push events
  - Pull requests
- Save the webhook.

- ## View Events in the Frontend
Access the frontend to see the latest events:
```
http://localhost:5000/latest_events
```

## File Structure

```
webhook-repo/
├── app
│   ├── __init__.py         # Initializes Flask app
│   ├── extensions.py       # MongoDB setup
│   └── webhook
│       ├── __init__.py
│       └── routes.py       # Webhook routes to handle GitHub events
├── requirements.txt        # Python dependencies
├── run.py                  # Flask app entry point
├── .gitignore              # Git ignored files
├── README.md               # Project documentation
└── templates/
    └── index.html          # Frontend page for viewing events
```
## Endpoints
- /webhook/receiver (POST): Receives webhooks from GitHub for Push, Pull Request, and Merge events.
- /latest_events (GET): Fetches the latest events stored in MongoDB and displays them on the frontend.

## Example Event Formats
### Push Event:
```
"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
```
### Pull Request Event:
```
"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC
```
### Merge Event:
```
"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC
```

