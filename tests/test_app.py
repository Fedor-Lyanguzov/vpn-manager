from vpn_manager import *

def test_format_static_peer():
    sp = StaticPeer('sample-public-key', '127.0.0.1', '12345')
    peer_section = format_static_peer(sp, '0.0.0.0/0')
    assert peer_section == '[Peer]\nPublicKey = sample-public-key\nAllowedIPs = 0.0.0.0/0\nEndpoint = 127.0.0.1:12345\nPersistentKeepAlive = 30'
