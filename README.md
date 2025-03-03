# bs_mon
### A small python utility to indicate CPU and memory use on an Blinkstick Nano

### clone the repo
```
mkdir ~/projects
cd ~/projects
git clone https://github.com/AllenAustin/bs_mon.git
```

### Create a virtual environment in ~/.virtualenvs/bs_mon and install requirements.txt into the virtual environment
```
python -m venv ~/.virtualenvs/bs_mon
source ~/.virtualenvs/bs_mon/bin/activate
pip install -r ~/projects/bs_mon/requirements.txt
deactivate
```

### Copy the unit file to /etc/systemd/system
```
sudo cp ~/projects/bs_mon/bsmon.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable bsmon
sudo systemctl start bsmon`
```
