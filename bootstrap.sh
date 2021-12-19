#!/bin/bash
apt -y install git python3 python3-pip
pip3 install ansible
ansible-pull -U https://github.com/NeoLeMarc/ansible -i hosts
