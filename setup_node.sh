if [ -z "$1" ]; then
  echo "Usage: $0 <node_number>"
  exit 1
fi

sudo hostnamectl set-hostname jetson-agx-$1

sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.1.10$1/24
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"

sudo ufw allow 50051


