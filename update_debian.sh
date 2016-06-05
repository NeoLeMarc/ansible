ansible debian -i hosts -u root -f 20 -m apt -a update_cache=yes -v
ansible debian -i hosts -u root -f 20 -m apt -a upgrade=dist -v
ansible debian -i hosts -u root -f 20 -a "apt-get autoremove -y"
