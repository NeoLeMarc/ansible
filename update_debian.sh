ansible debian -i hosts -u root -f 1 -m apt -a update_cache=yes -v
ansible debian -i hosts -u root -f 1 -m apt -a upgrade=dist -v
