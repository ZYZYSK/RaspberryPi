# Fan Controller
## Install
```sh
git clone https://github.com/ZYZYSK/RaspberryPi.git
cd fan
chmod 755 install.sh
./install.sh
```

## Settings
`/opt/fan/settings.json`

## Uninstall
```sh
sudo rm -rf /etc/systemd/system/fan_controller.service
sudo rm -rf /opt/fan
```