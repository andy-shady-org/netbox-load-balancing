# NetBox Load Balancing Plugin
[Netbox](https://github.com/netbox-community/netbox) plugin for Load Balancing related objects documentation.

<div align="center">
<a href="https://pypi.org/project/netbox-load-balancing/"><img src="https://img.shields.io/pypi/v/netbox-load-balancing" alt="PyPi"/></a>
<a href="https://github.com/andy-shady-org/netbox-load-balancing/stargazers"><img src="https://img.shields.io/github/stars/andy-shady-org/netbox-load-balancing?style=flat" alt="Stars Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-load-balancing/network/members"><img src="https://img.shields.io/github/forks/andy-shady-org/netbox-load-balancing?style=flat" alt="Forks Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-load-balancing/issues"><img src="https://img.shields.io/github/issues/andy-shady-org/netbox-load-balancing" alt="Issues Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-load-balancing/pulls"><img src="https://img.shields.io/github/issues-pr/andy-shady-org/netbox-load-balancing" alt="Pull Requests Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-load-balancing/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/andy-shady-org/netbox-load-balancing?color=2b9348"></a>
<a href="https://github.com/andy-shady-org/netbox-load-balancing/blob/master/LICENSE"><img src="https://img.shields.io/github/license/andy-shady-org/netbox-load-balancing?color=2b9348" alt="License Badge"/></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style Black"/></a>
<a href="https://pepy.tech/project/netbox-load-balancing"><img alt="Downloads" src="https://static.pepy.tech/badge/netbox-load-balancing"></a>
<a href="https://pepy.tech/project/netbox-load-balancing"><img alt="Downloads/Week" src="https://static.pepy.tech/badge/netbox-load-balancing/month"></a>
<a href="https://pepy.tech/project/netbox-load-balancing"><img alt="Downloads/Month" src="https://static.pepy.tech/badge/netbox-load-balancing/week"></a>
</div>


## Features

This plugin is based on the OpenStack modelling of [LBaaS](https://docs.openstack.org/mitaka/networking-guide/config-lbaas.html)

This plugin provides following Models:

* Services
* Virtual Pools
* Virtual IPs
* Listeners
* Health Monitors
* Pools
* Members

## Compatibility

|            |           |
|------------|-----------|
| NetBox 4.2 | \>= 1.0.1 |

## Installation

The plugin is available as a Python package in pypi and can be installed with pip  

```
pip install netbox-load-balancing
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_load_balancing']
```
Restart NetBox and add `netbox-load-balancing` to your local_requirements.txt

Perform database migrations:
```bash
cd /opt/netbox
source venv/bin/activate
python ./netbox/manage.py migrate netbox_load_balancing
python ./netbox/manage.py reindex netbox_load_balancing
```

Full documentation on using plugins with NetBox: [Using Plugins - NetBox Documentation](https://netbox.readthedocs.io/en/stable/plugins/)


## Configuration

The following options are available:
* `service_ext_page`: String (default left) Service related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `pool_ext_page`: String (default left) Pool related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `member_ext_page`: String (default left) Member related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `monitor_ext_page`: String (default left) Health Monitor related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `top_level_menu`: Boolean (default True) Display plugin menu at the top level. The following values are available: True, False.


## Contribute

Contributions are always welcome! Please see the [Contribution Guidelines](CONTRIBUTING.md)


## Documentation

For further information, please refer to the full documentation: [Using NetBox Load Balancer](docs/using_netbox_load_balancing.md)


## Credits

- Thanks to Peter Eckel for providing some lovely examples which I've happily borrowed, and for providing excellent guidance.
- Thanks to Gustavo Martinez for assisting with the high level modeling
