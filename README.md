# Starting The Project
Start Virtual Environment

pip3 install requirements.txt

# Start Server
python3 server.py

# Start Client
python3 client.py

## To kill server process and restart
kill -9 $(ps -A | grep python | awk '{print $1}')