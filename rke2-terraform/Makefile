.PHONY: tf-init tf-plan tf-apply tf-destroy

TF = terraform
TFVAR = -var-file=../terraform.tfvars
GET_IP = $(shell cat terraform.tfvars | hclq get --raw 'kubernetes_server_ips[0]')
COMMAND = ssh kubernetes@$(GET_IP) cat /etc/rancher/rke2/rke2.yaml 

# Verificarea versiunii terraform
check-terraform:
	./scripts/version_check.sh

# Initializare director de lucru si actualizarea modulelor
tf-init-upgrade:
	${TF} -chdir=./terraform init -upgrade

# Initializare director de lucru
tf-init:
	${TF} -chdir=./terraform init

# Creare plan de executie
tf-plan:
	${TF} -chdir=./terraform plan ${TFVAR}

# Creare infrastructura
tf-apply:
	${TF} -chdir=./terraform apply ${TFVAR} -auto-approve

# Distrugere infrastructura
tf-destroy:
	${TF} -chdir=./terraform destroy ${TFVAR} -auto-approve

# Crearea fisierului de configurare Kubernetes
create-k8s-file:
	ssh-keygen -R "$(GET_IP)" && ${COMMAND} | sed 's/127.0.0.1/$(GET_IP)/' > k8s.yaml

# Generare preche chei
generate-keypair:
	./scripts/generate_keypair.sh

# Adaugare cheie privata la agentul SSH, pentru implementarea autentificarii unice cu SSH
add-keypair:
	./scripts/sshaddkey.sh