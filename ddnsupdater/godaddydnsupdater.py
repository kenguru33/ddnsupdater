from configparser import ConfigParser
from pygodaddy import GoDaddyClient
from requests import get
from smtplib import SMTP


class GoDaddyDynamicDns:
    @property
    def __publicip(self):
        return get('https://api.ipify.org').text

    @property
    def __isfullymanaged(self):
        if self.__configparser.get('global', 'fully_managed').lower() == 'yes':
            return True
        else:
            return False

    @property
    def __usetls(self):
        if self.__configparser.get('global', 'smtp_tls').lower() == 'yes':
            return True
        else:
            return False

    def __init__(self, configfile):

        self.__godaddyclient = GoDaddyClient()

        # read config
        self.__configparser = ConfigParser()
        self.__configparser.read(configfile)
        self.__updatemessage = ''
        self.__username = self.__configparser.get('global', 'username')
        self.__password = self.__configparser.get('global', 'password')
        self.__logfile = self.__configparser.get('global', 'logfile')
        self.__changedetected = False
        self.__domains = []
        for section in self.__configparser.sections():
            if section != 'global':
                self.__domains.append(section)

        # mail config
        self.__mailnotifyenabled = self.__configparser.get('global', 'mail_notify_enabled')
        self.__mailreceiver = self.__configparser.get('global', 'mail_receiver')
        self.__mailsender = self.__configparser.get('global', 'mail_sender')
        self.__mailuser = self.__configparser.get('global', 'smtp_user')
        self.__mailpassword = self.__configparser.get('global', 'smtp_password')
        self.__smtphost = self.__configparser.get('global', 'smtp_host')
        self.__smtpport = self.__configparser.get('global', 'smtp_port')

    def updatedns(self):
        self.__login()
        for domain in self.__domains:
            self.__update(domain)
        if self.__mailnotifyenabled and self.__changedetected:
            self.__mailnotify(self.__updatemessage)

    def __update(self, domain):
        hostnames = [hostname.strip() for hostname in self.__configparser.get(domain, 'hostnames').split(',')]
        godaddyhostnames = [host[1] for host in self.__godaddyclient.find_dns_records(domain)]

        # update listed hostnames
        for hostname in hostnames:
            if hostname in godaddyhostnames:
                if self.__godaddyclient.update_dns_record(hostname + '.' + domain, self.__publicip):
                    print(hostname + '.' + domain + ' updated.')
                    self.__changedetected = True
                    self.__updatemessage = self.__updatemessage + hostname + '.' + domain + ' updated. \n'
            else:
                if self.__isfullymanaged:
                    if self.__godaddyclient.update_dns_record(hostname + '.' + domain, self.__publicip):
                        print(hostname + '.' + domain + ' added.')
                        self.__changedetected = True
                        self.__updatemessage = self.__updatemessage + hostname + '.' + domain + ' added. \n'

        # delete not listed hostnames
        godaddyhostnames = [host[1] for host in self.__godaddyclient.find_dns_records(domain)]
        if self.__isfullymanaged:
            for godaddyhostname in godaddyhostnames:
                if godaddyhostname not in hostnames:
                    if self.__godaddyclient.delete_dns_record(godaddyhostname + '.' + domain):
                        print(godaddyhostname + '.' + domain + ' deleted.')
                        self.__changedetected = True
                        self.__updatemessage = self.__updatemessage + godaddyhostname + '.' + domain + ' deleted. \n'

    def __login(self):
        if not self.__godaddyclient.is_loggedin():
            self.__godaddyclient.login(self.__username, self.__password)

    def __mailnotify(self, message):
        smtpserver = SMTP(self.__smtphost, self.__smtpport)
        header = 'To:' + self.__mailreceiver + '\n' + 'From: ' + self.__mailsender + '\n' + 'Subject:Godaddy dns updater \n'
        msg = header + '\n' + 'Public ip: ' + self.__publicip + '\n\n' + message + '\n\n'
        try:
            if self.__usetls:
                smtpserver.starttls()
            smtpserver.login(self.__mailuser, self.__mailpassword)
            smtpserver.sendmail(self.__mailsender, self.__mailreceiver, msg)
            print('mail notify sent.')
        except:
            print('mail notify failed service failed!')
        finally:
            smtpserver.close()
