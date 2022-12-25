#export ANSIBLE_DEBUG=1
ansible debian_servers -i hosts -u root -f 20 -m apt -a update_cache=yes -v
ansible debian_servers -i hosts -u root -f 20 -m apt -a upgrade=dist -v
ansible debian_servers -i hosts -u root -f 20 -a "apt-get autoremove -y"

# Re-deploy vaultwarden
ansible-playbook -i hosts --limit=dockerserver tasks/bitwarden/vaultwarden.yml
