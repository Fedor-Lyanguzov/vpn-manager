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