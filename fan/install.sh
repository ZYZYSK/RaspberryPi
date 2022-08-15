# /usr/bin/bash
if [ -e /etc/systemd/system/fan_controller.service  ]; then
    sudo rm -rf /etc/systemd/system/fan_controller.service
fi
if [ -e /opt/fan/fan_controller.py ]; then
    sudo rm -rf /opt/fan
fi

sudo mkdir -p /opt/fan
sudo cp ./fan_controller.py /opt/fan/fan_controller.py
sudo cp ./settings.json /opt/fan/settings.json
sudo cp ./fan_controller.service /etc/systemd/system/fan_controller.service

# sudo chmod 0777 /opt/fan
sudo chmod 0755 /opt/fan/fan_controller.py
# sudo chmod 0666 /opt/fan/settings.json
sudo systemctl enable fan_controller.service --now