resource "libvirt_volume" "kubernetes-worker" {
  count          = length(var.kubernetes_worker_ips)
  name           = "kubernetes-client-${count.index}"
  base_volume_id = libvirt_volume.os_image_ubuntu.id
  pool           = libvirt_pool.kubernetes.name
  size           = var.kubernetes_worker_disk_size
  format         = "qcow2"
}

resource "libvirt_cloudinit_disk" "worker-init" {
  count     = length(var.kubernetes_worker_ips)
  name      = "worker-init-${count.index}.iso"
  user_data = data.template_file.worker_user_data[count.index].rendered
  pool      = libvirt_pool.kubernetes.name
}

data "template_file" "worker_user_data" {
  count    = length(var.kubernetes_worker_ips)
  template = file("${path.cwd}/templates/cloud_initclient.cfg")
  vars = {
    HOSTNAME = upper(format(
      "%v-%v",
      var.kubernetes_worker_name,
      count.index
    )),
    KUBERNETES_SERVER_JOIN_IP    = element(var.kubernetes_server_ips, 0),
    KUBERNETES_IP                = "${element(var.kubernetes_worker_ips, count.index)}",
    KUBERNETES_NODE_PUBLIC_KEY   = file(var.kubernetes_node_public_key_path),
    KUBERNETES_NODE_SSH_USERNAME = var.kubernetes_node_ssh_username,
    KUBERNETES_JOIN_TOKEN        = var.kubernetes_join_token,
  }
}

# Creare masina
resource "libvirt_domain" "domain-kubernetes-worker" {
  count  = length(var.kubernetes_worker_ips)
  name   = "${var.kubernetes_worker_name}-${count.index}"
  memory = var.kubernetes_worker_memory
  vcpu   = var.kubernetes_worker_vcpu

  cloudinit = libvirt_cloudinit_disk.worker-init[count.index].id

  network_interface {
    network_id     = libvirt_network.kubernetes_network.id
    hostname       = "${var.kubernetes_worker_name}-${count.index}"
    addresses      = ["${element(var.kubernetes_worker_ips, count.index)}"]
    wait_for_lease = true
  }

  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }

  console {
    type        = "pty"
    target_type = "virtio"
    target_port = "1"
  }

  disk {
    volume_id = libvirt_volume.kubernetes-worker[count.index].id
  }

  graphics {
    type        = "spice"
    listen_type = "address"
    autoport    = true
  }

  provisioner "remote-exec" {
    connection {
      host  = self.network_interface.0.addresses.0
      type  = "ssh"
      user  = var.kubernetes_node_ssh_username
      agent = true
    }
    inline = [
      "cloud-init status --wait > /dev/null 2>&1",
    ]
  }
}
