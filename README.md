# Ansible Role fail2ban

This role installs and configures fail2ban.

## Example play

```yaml
- hosts: all
  roles:
    - blunix.role-fail2ban
  vars:
    fail2ban_enabled: yes
    fail2ban_default_bantime: 3600
    fail2ban_default_maxretry: 5
    fail2ban_default_destemail: monitoring-example@example.com
    fail2ban_jails:
      - name: default
        vars:
          DEFAULT:
            ignoreip: '8.8.4.4'
            backend: auto
            banaction: iptables-multiport
      - name: sshd
        vars:
          sshd:
            enabled: 'true'
            filter: sshd
            maxretry: 6
            port: ssh
          sshd_ddos:
            action:
              - 'shorewall[name=SSH, port=ssh, protocol=tcp]'
            enabled: 'true'
            filter: 'sshd-ddos'
            maxretry: 6
            port: ssh
    fail2ban_actions:
      - name: 'iptables-ipset-proto4'
        vars:
          INCLUDES:
            before: iptables-blocktype.conf
          Definition:
            actionstart:
              - 'ipset --create fail2ban-<name> iphash'
              - 'iptables -I INPUT -p <protocol> -m multiport --dports <port> -m set --match-set fail2ban-<name> src -j <blocktype>'
            actionstop:
              - 'iptables -D INPUT -p <protocol> -m multiport --dports <port> -m set --match-set fail2ban-<name> src -j <blocktype>'
              - 'ipset --flush fail2ban-<name>'
              - 'ipset --destroy fail2ban-<name>'
            actionban:
              - 'ipset --test fail2ban-<name> <ip> ||  ipset --add fail2ban-<name> <ip>'
            actionunban:
              - 'ipset --test fail2ban-<name> <ip> && ipset --del fail2ban-<name> <ip>'
          Init:
            name: default
            port: ssh
            protocol: tcp
    fail2ban_filters:
      download:
        - name: apache-common-latest
          url: "https://raw.githubusercontent.com/fail2ban/fail2ban/0.10/config/filter.d/apache-common.conf"
      custom:
        - name: nginx-noscript
          vars:
            Definition:
              failregex: |
                  <HOST>.*(GET|POST).*(\.php|\.asp|\.exe|\.pl|\.cgi|\.scgi).*
        - name: nginx-reqlimit
          vars:
            Definition:
              failregex: |
                  limiting requests, excess:.* by zone.*client: <HOST>
          # From https://github.com/fail2ban/fail2ban/blob/0.8/config/filter.d/apache-common.conf
        - name: apache-common-latest
          vars:
            INCLUDES:
              after: apache-common-latest.local
            DEFAULT:
              _apache_error_client: |
                  \[[^]]*\] \[(:?error|\S+:\S+)\]( \[pid \d+(:\S+ \d+)?\])? \[client <HOST>(:\d{1,5})?\]
          # From https://github.com/fail2ban/fail2ban/blob/0.8/config/filter.d/apache-auth.conf
        - name: apache-auth-latest
          vars:
            INCLUDES:
              before: apache-common-latest.conf
            Definition:
              ignoreregex: ''
              failregex: |
                  ^%(_apache_error_client)s (AH01797: )?client denied by server configuration: (uri )?\S*(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01617: )?user .*? authentication failure for "\S*": Password Mismatch(, referer: \S+)?$
                              ^%(_apache_error_client)s (AH01618: )?user .*? not found(: )?\S*(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01614: )?client used wrong authentication scheme: \S*(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH\d+: )?Authorization of user \S+ to access \S* failed, reason: .*$
                              ^%(_apache_error_client)s (AH0179[24]: )?(Digest: )?user .*?: password mismatch: \S*(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH0179[01]: |Digest: )user `.*?' in realm `.+' (not found|denied by provider): \S*(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01631: )?user .*?: authorization failure for "\S*":(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01775: )?(Digest: )?invalid nonce .* received - length is not \S+(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01788: )?(Digest: )?realm mismatch - got `.*?' but expected `.+'(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01789: )?(Digest: )?unknown algorithm `.*?' received: \S*(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01793: )?invalid qop `.*?' received: \S*(, referer: \S+)?\s*$
                              ^%(_apache_error_client)s (AH01777: )?(Digest: )?invalid nonce .*? received - user attempted time travel(, referer: \S+)?\s*$
          # From http://www.fail2ban.org/wiki/index.php/HOWTO_fail2ban_with_OpenVPN
        - name: openvpn
          vars:
            Definition:
              ignoreregex: ''
              failregex: |
                  ^ TLS Error: incoming packet authentication failed from \[AF_INET\]<HOST>:\d+$
                              ^ <HOST>:\d+ Connection reset, restarting
                              ^ <HOST>:\d+ TLS Auth Error
                              ^ <HOST>:\d+ TLS Error: TLS handshake failed$
                              ^ <HOST>:\d+ VERIFY ERROR
```

# License

Apache-2.0

# Author Information

All changes from 2019-05-31 onwards:

```
Programmfabrik GmbH,
Schwedter Str. 9b,
10119 Berlin
```

All changes until 2019-05-30 by:

Service and support for orchestrated hosting environments,
continuous integration/deployment/delivery and various Linux
and open-source technology stacks are available from:

```
Blunix GmbH - Consulting for Linux Hosting 24/7
Glogauer Straße 21
10999 Berlin - Germany

Web: www.blunix.org
Email: service[at]blunix.org
Phone: (+49) 30 / 12 08 39 90
```
