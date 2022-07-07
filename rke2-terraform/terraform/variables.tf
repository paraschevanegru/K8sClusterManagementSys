### Configuratii comune celor doua tipuri de noduri ###

variable "os_image" {
  description = "Sursa imaginii sistemului de operare folosit de Kubernetes"
  default = "http://cloud-images-archive.ubuntu.com/releases/focal/release-20220530/ubuntu-20.04-server-cloudimg-amd64-disk-kvm.img"
}
variable "kubernetes_pool_path" {
  description = "Calea catre libvirt pool"
  default = "/tmp/terraform-provider-libvirt-pool-kubernetes"
}

variable "kubernetes_node_private_key_path"{
  description = "Calea catre cheia privata"
  default = "/home/user/keys/your_private_key"
}
variable "kubernetes_node_public_key_path"{
  description = "Calea catre cheia publica"
  default = "/home/user/keys/your_public_key"
}
variable "kubernetes_node_ssh_username"{
  description = "Username-ul SSH username de pe masina virtuala"
  default = "kubernetes"
}

variable "kubernetes_join_token"{
  description = "Token"
  default = "secrettoken"
}

### Configurarea serverului Kubernetes ###
variable "kubernetes_server_name" {
  description = "Numele serverului Kubernetes"
  default = "k8s-server"
}
variable "kubernetes_server_ips" {
  description = "Lista IP-urilor utilizate de serverul Kubernetes"
  type    = list(string)
  default = ["10.18.3.10", "10.18.3.11", "10.18.3.12"]
}
variable "kubernetes_server_enable_client" {
  description = "Activarea clientului pe serverul Kubernetes"
  type = bool
  default = false
}
variable "kubernetes_server_vcpu" {
  description = "vcpu atribuit serverului Kubernetes"
  default = 1
}
variable "kubernetes_server_memory" {
  description = "Memoria atribuita serverului Kubernetes"
  default = "512"
}
variable "kubernetes_server_disk_size" {
  description = "Dimensiunea disk-ului atribuita serverului Kubernetes"
  default = "4294965097" #4gb
}


### Configurarea nodurilor Kubernetes de tip Worker ###
variable "kubernetes_worker_name" {
  description = "Numele nodului Kubernetes de tip Worker"
  default = "k8s-worker"
}
variable "kubernetes_worker_ips" {
  description = "Lista IP-urilor utilizate de nodurile Kubernetes de tip Worker"
  type    = list(string)
  default = ["10.18.3.20", "10.18.3.21"]
}
variable "kubernetes_worker_vcpu" {
  description = "vcpu atribuit nodurilor Kubernetes de tip Worker"
  default = 2
}
variable "kubernetes_worker_memory" {
  description = "Memoria atribuita pentru Nomad client"
  default = "1024"
}
variable "kubernetes_worker_disk_size" {
  description = "Dimensiunea disk-ului atribuita pentru Nomad client"
  default = "6442447645" #6gb
}