 A simple network dashboard for local network and port scanning made in Python.

<p align="center">
<img src="res/appicon.png" alt="appicon" width="350"/>
</p>

<strong>
<p style="text-align:center;">net-dashboard</p>
</strong>

 ## Prerequisites
 - Docker
 - Python 3.12 or later and `pip` (if not using docker)
 - `sudo` / root privileges

 ## Run with Docker (recommended)

 Run the app using Docker Compose. Because the scanners require root privileges, run the compose command with `sudo` so the container runs as root:

 ```bash
 sudo docker compose up -d --build
 ```
 To stop, use 
 ```bash
 sudo docker compose down
 ```
 And to check the log output
 ```bash
 sudo docker logs -f
 ```
## Run using prebuilt .tar file

First, download the ```net-dashboard.tar``` file from the Releases page. Then in a command window, go to the location of the downloaded tar file and run
```bash
docker load -i net-dashboard.tar
docker -it net-dashboard
```

You can access the dashboard on ```localhost:5000``` or on ```DEVICE_IP:5000```

 ## Run locally (no Docker)

 Install Python dependencies and run the backend directly. Scapy requires root privileges for scanning, so run with `sudo`:

 ```bash
 python3 -m pip install -r requirements.txt
 sudo python3 backend/app.py
 ```

 ## Notes
 - If you are on Windows, running docker normally is fine and sudo isn't required.
 - You can change the port on what the app runs on by changing it in app.py.


