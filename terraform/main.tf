locals {
  ubuntu_base_source = "/home/nikit/vms/images/focal-server-cloudimg-amd64-disk-kvm.img"
  pools_path_prefix  = "/opt/alluvium/demo"
  pools_disks        = "alluvium-demo-disks"
  pools_images       = "alluvium-demo-images"
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
  vms = {
    ubuntu = {
      net-1-r = {
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
        hostfwd = [
        ]
      }
      net-1-c = {
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
        hostfwd = [
        ]
      }
      net-2-r = {
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
        hostfwd = [
        ]
      }
      net-2-c = {
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
        hostfwd = [
        ]
      }
      net-3-c = {
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
        hostfwd = [
        ]
      }
    }
  }
}
