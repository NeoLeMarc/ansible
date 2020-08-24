#!/bin/bash
apt -y install git python3 python3-pip
pip3 install ansible
ansible-pull -U https://citadel.noetech.net/stash/scm/an/ansible.git -i hosts_pull
