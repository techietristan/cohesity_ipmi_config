# Cohesity Node IPMI Configuration Script
### This is an experimental Python script for configuring IPMI network settings for C5000 series Cohesity nodes.



# Installation
Ensure you have Git and Python 3 installed. From a terminal, run the following commands:
```
git --version
python3 --version
```
## Windows 10, 11
If the above commands do not return a version number (or return Python 2), install Git and Python 3 using winget:
```
winget install -e --id Git.Git
winget install -e --id Python.Python.3.11
```
**Note**: Python 3 may be aliased to `python` or `py` on your system. In that case, replace `python3` in the commands below with the appropriate command for your system.

# Usage
From a terminal, clone the repository and `cd` into its directory:
```
> git clone https://github.com/techietristan/cohesity_ipmi_config.git
> cd cohesity_ipmi_config
```
Install any modules required by the script:
```
pip3 install -r requirements.txt
```
Run the script with the ```--help``` flag to display the required parameters:
```
> python3 . --help
usage: . [-h] -g GATEWAY -m NETMASK -n NODE_HOSTNAME -i NODE_IP [-v]

A configuration utility for Cohesity IPMIs

options:
  -h, --help            show this help message and exit
  -g, --gateway GATEWAY
                        Specify the default gateway to configure.
  -m, --netmask NETMASK
                        Specify the subnet mask to configure.
  -n, --node_hostname NODE_HOSTNAME
                        Specify the first node hostname.
  -i, --node_ip NODE_IP
                        Specify the first node IP address.
  -v, --verify          Attempt to ping each node sequentially.
```
The default IP address of C5000 series nodes is ```192.168.1.1```. Set the static IP of the NIC you're using to connect to the nodes' IPMI ports to something in the ```192.168.1.0/24``` subnet other than the default node IP, for example ```192.168.1.2```.

To configure nodes sequentially, begin with the first (lowest) hostname and IP address. For example:
```
python3 . -n node_hostname123a -i 192.168.1.123 -m 24 -g 192.168.1.1
```
The above command is equivalent to:
```
python3 . --node_hostname node_hostname123a --node_ip 192.168.1.123 --netmask 255.255.255.0 --gateway 192.168.1.1
```
Note: the subnet mask can be entered in dotted decimal format or CIDR notation. This means that ```--netmask 255.255.255.224``` and ```--netmask 27``` are equivalent.

After ```node_hostname123a``` is configured, the script will automatically increment the hostname and IP address (in this example they would be incremented to ```node_hostname123b``` and ```192.168.1.124```) and prompt you to connect to the next node.