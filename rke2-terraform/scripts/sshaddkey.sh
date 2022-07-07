#!/bin/bash

NAME=${1:-kubernetes_key}

# Calea fisierului destinatie in care sunt salvate cheile
DEST=${2:-/home/para/Desktop/K8sClusterManagementSys/rke2-terraform/keys/}

PASS=${3:-blank}

# Fisierul pentru cheia privata
PRIK=$DEST$NAME

# Adaugarea cheii private la agentul SSH
/usr/bin/expect <<EOD
spawn ssh-add $PRIK
match_max 100000
expect -exact "Enter passphrase for $PRIK: "
send -- "$PASS\r"
expect eof
EOD
