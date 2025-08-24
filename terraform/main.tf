locals {
  ubuntu_base_source = "/home/nikit/vms/images/focal-server-cloudimg-amd64-disk-kvm.img"
  pools_path_prefix  = "/opt/alluvium/demo"
  pools_disks        = "alluvium-demo-disks"
  pools_images       = "alluvium-demo-images"
  net_1              = "alluvium-net-1"
  net_2              = "alluvium-net-2"
  net_3              = "alluvium-net-3"
}

module "vm" {
  source = "git@github.com:klephron/alluvium-terraform-selfhosted.git"

  pools = {
    images = {
      "${local.pools_images}" = {
        path = "${local.pools_path_prefix}/images"
      },
    }
    disks = {
      "${local.pools_disks}" = {
        path = "${local.pools_path_prefix}/disks"
      }
    }
  }
  bridges = {
    "${local.net_1}" = {
      bridge = "br-alluvium-1"
    }
    "${local.net_2}" = {
      bridge = "br-alluvium-2"
    }
    "${local.net_3}" = {
      bridge = "br-alluvium-3"
    }
  }
  vms = {
    alluvium-demo-1-r = {
      pools = {
        images = local.pools_images
        disks  = local.pools_disks
      }
      base = {
        source = local.ubuntu_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        local.net_1,
        local.net_3
      ]
    }
    alluvium-demo-1-c = {
      pools = {
        images = local.pools_images
        disks  = local.pools_disks
      }
      base = {
        source = local.ubuntu_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        local.net_1
      ]
    }
    alluvium-demo-2-r = {
      pools = {
        images = local.pools_images
        disks  = local.pools_disks
      }
      base = {
        source = local.ubuntu_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        local.net_2,
        local.net_3
      ]
    }
    alluvium-demo-2-c = {
      pools = {
        images = local.pools_images
        disks  = local.pools_disks
      }
      base = {
        source = local.ubuntu_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        local.net_2
      ]
    }
    alluvium-demo-3-c = {
      pools = {
        images = local.pools_images
        disks  = local.pools_disks
      }
      base = {
        source = local.ubuntu_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        local.net_3
      ]
    }
  }
}
