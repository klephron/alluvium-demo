variable "vms_base_source" {
  type        = string
  default     = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
  description = "Base image source for defined vms"
}

variable "pools_path_prefix" {
  type        = string
  default     = "/opt/alluvium/demo"
  description = "Path prefix for images and disks pools"
}

variable "pools_disks" {
  type        = string
  default     = "alluvium-demo-disks"
  description = "Pool name for disks"
}

variable "pools_images" {
  type        = string
  default     = "alluvium-demo-images"
  description = "Pool name for images"
}

variable "net_1" {
  type        = string
  default     = "alluvium-net-1"
  description = "Name for alluvium network 1"
}

variable "net_2" {
  type        = string
  default     = "alluvium-net-2"
  description = "Name for alluvium network 2"
}

variable "net_3" {
  type        = string
  default     = "alluvium-net-3"
  description = "Name for alluvium network 3"
}
