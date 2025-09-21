# alluvium-demo

## Network Topology and VMs

Create:

```sh
cd ./terraform
terraform apply
```

Destroy:

```sh
terraform destroy
```

> Update terraform variables if necessary.

## VM Network configuration

> To ssh on vms use `ubuntu` user with default password as `ubuntu`.

- `alluvium-demo-1-r`: `net-1` - `10.97.1.1/24`, `net-3` - `10.97.3.2/24`
- `alluvium-demo-1-c`: `net-1` - `10.97.1.2/24`
- `alluvium-demo-2-r`: `net-2` - `10.97.2.1/24`, `net-3` - `10.97.3.3/24`
- `alluvium-demo-2-c`: `net-2` - `10.97.2.2/24`
- `alluvium-demo-3-c`: `net-3` - `10.97.3.4/24`

> Check packets (without ARP and STP): `sudo tcpdump -i ens5 not arp and not llc`

### `alluvium-demo-1-c`

```sh
sudo ip a add 10.97.1.2/24 dev ens4
sudo ip link set ens4 up
```

```sh
sudo ip route add default via 10.97.1.1 metric 0
```

### `alluvium-demo-1-r`

```sh
sudo ip a add 10.97.1.1/24 dev ens4
sudo ip link set ens4 up

sudo ip a add 10.97.3.2/24 dev ens5
sudo ip link set ens5 up
```

```sh
sudo sysctl -w net.ipv4.ip_forward=1
# echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
```

```sh
sudo iptables -t nat -A POSTROUTING -o ens5 -j MASQUERADE
```

### `alluvium-demo-2-c`

```sh
sudo ip a add 10.97.2.2/24 dev ens4
sudo ip link set ens4 up
```

```sh
sudo ip route add default via 10.97.2.1 metric 0
```

### `alluvium-demo-2-r`

```sh
sudo ip a add 10.97.2.1/24 dev ens4
sudo ip link set ens4 up

sudo ip a add 10.97.3.3/24 dev ens5
sudo ip link set ens5 up
```

```sh
sudo sysctl -w net.ipv4.ip_forward=1
# echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
```

```sh
sudo iptables -t nat -A POSTROUTING -o ens5 -j MASQUERADE
```

### `alluvium-demo-3-c`

```sh
sudo ip a add 10.97.3.4/24 dev ens4
sudo ip link set ens4 up
```

## Script installation

Can be done with `scp`.

Peers: `alluvium-demo-1-c`, `alluvium-demo-2-c` - over nat.

Tracker: `alluvium-demo-3-c` - uses public ip.

## Conclusion about linux masquerade default behavior

- It is **not endpoint-independent** (cone).
- It is also **not pure symmetric** in the strict RFC sense.
- Behavior:
  - If the **inside host sends first**, conntrack reuses the same external port for the new destination.
  - If the **outside peer sends first**, conntrack has no state and will later allocate a new port → mapping divergence.

This means:

- Hole punching can work if **both peers send outbound to each other nearly simultaneously** (so each NAT has state when the inbound arrives).
- If one side is late, Linux NAT will break the mapping.
