import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    assert host.package('fail2ban').is_installed


def test_service(Service):
    s = Service('fail2ban')
    assert s.is_enabled
    assert s.is_running
