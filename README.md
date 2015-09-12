# Dynamic dns updater for godaddy dns records.

 - Fully manage multiple domains
 - Send notify mails on dns record changes.

**usage: gddnsupdate \<configfile\>**


### Config file example:

##### GoDaddyDDns Configuration

    [global]

    # godadday username
    username: <your user name>

    # godaddy password
    password: <your password>

    # log file where output from every run is written
    logfile: /var/log/ddns.log

    # enable notify by mail
    mail_notify_enabled: yes

    # mail server to use for sending error and update notify messages
    smtp_host: <your smtp server>

    # smtp user
    smtp_user: <your smtp user>

    #smtp password
    smtp_password: <your smtp password>

    # smtp port
    smtp_port: 587

    # use secure smtp
    smtp_tls: yes

    # where to send the notify email
    mail_receiver: <receiver mail address>

    # sender address
    mail_sender: root@localhost

    # fully manged - be careful. This will delete all recrods that are not listed under the domain.
    fully_managed: yes

    [domain1.org]
    hostnames: @, ssh, vpn

    [domain2.com]
    hostnames: @, ssh



**TIPS:**

- The updater program supports only A records. To be able to fully mange your domains you must remove all cname an replace them with A records.
- Set the TTL to 600.






