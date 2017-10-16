import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_fail2ban_local(host):
    f = host.file('/etc/fail2ban/fail2ban.local')

    assert f.exists
    assert f.contains('loglevel = 2')
    assert f.contains('banaction = shorewall')
    assert f.contains('maxretry = 5')
    assert f.contains('logtarget = /var/log/fail2ban.log')
    assert f.contains('bantime = 600')
    assert f.contains('destemail = monitoring-example@example.com')
