# vpn-manager
Manage WireGuard VPN peers (both server and clients)

# Development
To start developing:
```
python -m venv .venv
source .venv/Scripts/activate
pip install -e .[test,lint]
# work related commands here
deactivate
```

Tools:
```
pytest
flake8 vpn_manager
black vpn_manager
```

Test runs:
```
# package
$ python -m vpn_manager
run
# script declared in pyproject.toml
$ example
run
```

Run different merging algorithms:
```
python -m vpn_manager.cidr4_merge.cidr4_merger
python -m vpn_manager.cidr4_merge.fast
python -m vpn_manager.cidr4_merge.precise
```
