locals {
}

module "selfhosted" {
  source = "git@github.com:klephron/alluvium-terraform-selfhosted.git"

  pools = {
    images = {
      "${var.pools_images}" = {
        path = "${var.pools_path_prefix}/images"
      },
    }
    disks = {
      "${var.pools_disks}" = {
        path = "${var.pools_path_prefix}/disks"
      }
    }
  }
  bridges = {
    "${var.net_1}" = {
      bridge = "br-alluvium-1"
    }
    "${var.net_2}" = {
      bridge = "br-alluvium-2"
    }
    "${var.net_3}" = {
      bridge = "br-alluvium-3"
    }
  }
  vms = {
    alluvium-demo-1-r = {
      pools = {
        images = var.pools_images
        disks  = var.pools_disks
      }
      base = {
        source = var.vms_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        var.net_1,
        var.net_3
      ]
    }
    alluvium-demo-1-c = {
      pools = {
        images = var.pools_images
        disks  = var.pools_disks
      }
      base = {
        source = var.vms_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        var.net_1
      ]
    }
    alluvium-demo-2-r = {
      pools = {
        images = var.pools_images
        disks  = var.pools_disks
      }
      base = {
        source = var.vms_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        var.net_2,
        var.net_3
      ]
    }
    alluvium-demo-2-c = {
      pools = {
        images = var.pools_images
        disks  = var.pools_disks
      }
      base = {
        source = var.vms_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        var.net_2
      ]
    }
    alluvium-demo-3-c = {
      pools = {
        images = var.pools_images
        disks  = var.pools_disks
      }
      base = {
        source = var.vms_base_source
      }
      vcpu      = 1
      memory    = 1024
      disk_size = 30
      bridges = [
        var.net_3
      ]
    }
  }
}
