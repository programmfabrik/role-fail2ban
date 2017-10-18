import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('jail', [
    {
        'name': u'default',
        'vars': {
            'DEFAULT':  {
                'backend': 'systemd',
                'banaction': 'shorewall',
            }
        }
    },
    {
        'name': u'sshd',
        'vars': {
            'sshd': {
                'action': 'shorewall[name=SSH, port=ssh, protocol=tcp]',
                'enabled': 'true',
                'filter': 'sshd',
                'maxretry': 6,
                'port': 'ssh',
            },
            'ssh_ddos': {
                'action': 'shorewall[name=SSH, port=ssh, protocol=tcp]',
                'enabled': 'true',
                'filter': 'sshd-ddos',
                'maxretry': 6,
                'port': 'ssh',
            }
        }
    }
])
def test_jails(host, jail):
    f = host.file('/etc/fail2ban/jail.d/{}.conf'.format(jail['name']))

    assert f.exists
    for section in jail['vars']:
        assert f.contains('[{}]'.format(section))
        for option, value in jail['vars'][section].iteritems():
            if not option == 'action':
                assert f.contains('{} = {}'.format(option, value))
