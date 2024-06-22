# DJI Tello Drone Control Project

This project allows you to control a DJI Tello drone using voice commands. Follow the steps below to set up and run the project.

## Prerequisites

- DJI Tello drone
- Laptop with WiFi capability
- Python 3.6 or higher

## Installation

### 1. Create a Virtual Environment

To isolate the project dependencies, create a virtual environment:

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

On Windows

```bash
./venv/Scripts/activate
```

On macOS and Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required dependencies using the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the application by running:

```bash
python app.py
```

### 5. Connecting to the DJI Tello Drone

- Open your laptop's WiFi settings.
- Search for the DJI Tello drone in the available networks.
- Connect to the drone's network. The drone needs network connectivity to analyze and execute the commands.

### 6. Voice Commands

Voice Commands
Once connected, you can use the following voice commands to control the drone:

- 'TAKEOFF' - to get the drone up and running from standstill.
- 'UP' - for increasing altitude.
- 'DOWN' - for decreasing altitude.
- 'HOVER' - the drone will stabilize the altitude levels.
- 'LEFT' - to move left.
- 'RIGHT' - to move right.
- 'FLIP' - for a cool backflip.
- 'LAND' - to land the drone safely.


### 7. Troubleshooting

Ensure the drone is fully charged.
Make sure your laptop's WiFi is turned on and connected to the drone's network.
Verify that you have activated the virtual environment before running the application.
Check the console output for any errors and resolve them as indicated.


### 8. Contributing

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.




