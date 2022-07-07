#!/bin/bash
# Generarea unei perechi de chei ( privata si publica)

NAME=${1:-kubernetes_key}

# Calea fisierului destinatie in care sunt salvate cheile
DEST=${2:-/home/para/Desktop/K8sClusterManagementSys/rke2-terraform/keys}

PASS=${3:-blank}

# Fisierele pentru cheia publica si privata
PRIK=$DEST$NAME
PUBK=$DEST$NAME.pub

# Daca acestea exista, evita suprascrierea lor
if [ -f "$PRIK" ] || [ -f "$PUBK" ]; then
	echo "O cheie cu acelasi nume exista!"
	ssh-add $PRIK
	exit 0
fi

ssh-keygen -t ed25519 -C "k8s" -f $DEST$NAME -P $PASS
ssh-add $PRIK
