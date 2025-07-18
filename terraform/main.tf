module "vm" {
  source = "git@github.com:klephron/alluvium-terraform-selfhosted.git"

  pools = {
    images = {
      alluvium-demo-images = {
        path = "/opt/alluvium/demo/images"
      },
    }
    disks = {
      alluvium-demo-disks = {
        path = "/opt/alluvium/demo/disks"
      }
    }
  }
  vms = {
    ubuntu = {
      client-sender = {
        pools = {
          images = "alluvium-demo-images"
          disks  = "alluvium-demo-disks"
        }
        base = {
          source = "/home/nikit/vms/images/focal-server-cloudimg-amd64-disk-kvm.img"
        }
        vcpu      = 2
        memory    = 2048
        disk_size = 30
        hostfwd   = []
      }
      client-receiver = {
        pools = {
          images = "alluvium-demo-images"
          disks  = "alluvium-demo-disks"
        }
        base = {
          source = "/home/nikit/vms/images/focal-server-cloudimg-amd64-disk-kvm.img"
        }
        vcpu      = 2
        memory    = 2048
        disk_size = 30
        hostfwd   = []
      }
      tracker = {
        pools = {
          images = "alluvium-demo-images"
          disks  = "alluvium-demo-disks"
        }
        base = {
          source = "/home/nikit/vms/images/focal-server-cloudimg-amd64-disk-kvm.img"
        }
        vcpu      = 2
        memory    = 2048
        disk_size = 30
        hostfwd = [
          {
            from = 9999
            to   = 9999
          }
        ]
      }
    }
  }
}
