from fabric.api import run, sudo
from fabric.contrib.files import exists, contains, append
from fabric.utils import abort

#utility functions
def abort_with_message(message):
    abort(message)   

def basic_install_check(message, config_loc, mongod_bin_loc, data_dir_loc):
    #check existence of config file
    if not exists(config_loc):
         abort_with_message(message + 'config file not found')
    #TODO should we the contents of the config file?

    #check existence of binaries
    if not exists(mongod_bin_loc):
        abort_with_message(message + 'mongod binary not found')
    #TODO should we check other binaries?

    #check existence of data dir
    if not exists(data_dir_loc):
        abort_with_message(message + 'mongod data directory not found')

def basic_running_check(message, log_loc, lock_file_loc):
    #confirm log exists
    if not exists(log_loc):
        abort_with_message(message + 'mongod log not found')

    #confirm lockfile exists
    if not contains(lock_file_loc, '[0123456789]', escape=False):
        abort_with_message(message + 'mongod lock not found')

def basic_stopped_check(message, lock_file_loc):
    #confirm that lockfile doesnt exist
    if contains(lock_file_loc, '[0123456789]', escape=False):
        abort_with_message(message + 'mongod lock not empty')



#systems
class system_operator(object):

    def __init__(self):
        pass

    def install(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def check_installed(self):
        pass

    def check_started(self):
        pass

    def check_stopped(self):
        pass


class debian_operator(system_operator):
    def __init__(self):
        self.name = 'debian'
        self.locations = {}
        self.locations['config_loc'] = '/etc/mongod.conf'
        self.locations['mongod_bin_loc'] = '/usr/bin/mongod'
        self.locations['data_dir_loc'] = '/var/lib/mongodb'
        self.locations['log_loc'] = '/var/lib/mongodb/mongodb.log'
        self.locations['lock_file_loc'] = '/var/lib/mongodb/mongod.lock'
        self.locations['pid_file_loc'] = '/var/run/mongod.pid'

    def install(self):
        sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
        sudo('echo deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen > /etc/apt/sources.list.d/mongodb.list')
        sudo('apt-get update')
        sudo('apt-get -y install mongodb-org')

    def start(self):
        sudo('service mongod start')

    def stop(self):
        sudo('service mongod stop')

    def restart(self):
        sudo('service mongod restart')

    def check_installed(self):
        basemsg = 'check_installed failed: '
        basic_install_check(basemsg,
                            self.locations['config_loc'], 
                            self.locations['mongod_bin_loc'],
                            self.locations['data_dir_loc'])

    def check_started(self):
        basemsg = 'check_started failed: '
        basic_running_check(basemsg,
                            self.locations['log_loc'],
                            self.locations['lock_file_loc'])

        #confirm pidfile exists
        if not exists(self.locations['pid_file_loc']):
            abort_with_message(basemsg + 'mongod pidfile not found')

    def check_stopped(self):
        basemsg = 'check_mongod_stopped failed: '
        basic_stopped_check(basemsg,
                            self.locations['lock_file_loc'])


class ubuntu_operator(system_operator):
    def __init__(self):
        self.name = 'ubuntu'
        self.locations = {}
        self.locations['config_loc'] = '/etc/mongod.conf'
        self.locations['mongod_bin_loc'] = '/usr/bin/mongod'
        self.locations['data_dir_loc'] = '/var/lib/mongodb'
        self.locations['log_loc'] = '/var/log/mongodb/mongod.log'
        self.locations['lock_file_loc'] = '/var/lib/mongodb/mongod.lock'

    def install(self):
        sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com --recv 7F0CEB10')
        sudo('echo deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen > /etc/apt/sources.list.d/mongodb.list')
        sudo('apt-get update')
        sudo('apt-get -y install mongodb-org')

    def start(self):
        sudo('service mongod start')

    def stop(self):
        sudo('service mongod stop')

    def restart(self):
        sudo('service mongod restart')

    def check_installed(self):
        basemsg = 'check_installed failed: '
        basic_install_check(basemsg,
                            self.locations['config_loc'], 
                            self.locations['mongod_bin_loc'],
                            self.locations['data_dir_loc'])

    def check_started(self):
        basemsg = 'check_mongod_started failed: '
        basic_running_check(basemsg,
                            self.locations['log_loc'],
                            self.locations['lock_file_loc'])

    def check_stopped(self):
        basemsg = 'check_mongod_stopped failed: '
        basic_stopped_check(basemsg,
                            self.locations['lock_file_loc'])

class rhel_operator(system_operator):
    def __init__(self):
        self.name = 'rhel'
        self.locations = {}
        self.locations['config_loc'] = '/etc/mongod.conf'
        self.locations['mongod_bin_loc'] = '/usr/bin/mongod'
        self.locations['data_dir_loc'] = '/var/lib/mongo'
        self.locations['log_loc'] = '/var/log/mongodb/mongod.log'
        self.locations['lock_file_loc'] = '/var/lib/mongo/mongod.lock'
        self.locations['pid_file_loc'] = '/var/run/mongodb/mongod.pid'

    def install(self):
        repo = '[mongodb]\nname=MongoDB Repository\nbaseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/\ngpgcheck=0\nenabled=1\n'
        append('/etc/yum.repos.d/mongodb.repo', repo)
        sudo('yum -y install mongodb-org')

    def start(self):
        sudo('service mongod start')

    def stop(self):
        sudo('service mongod stop')

    def restart(self):
        sudo('service mongod restart')

    def check_installed(self):
        basemsg = 'check_installed failed: '
        basic_install_check(basemsg,
                            self.locations['config_loc'], 
                            self.locations['mongod_bin_loc'],
                            self.locations['data_dir_loc'])

    def check_started(self):
        basemsg = 'check_mongod_started failed: '
        basic_running_check(basemsg,
                            self.locations['log_loc'],
                            self.locations['lock_file_loc'])

        #confirm pidfile exists
        if not exists(self.locations['pid_file_loc']):
            abort_with_message(basemsg + 'mongod pidfile not found')

    def check_stopped(self):
        basemsg = 'check_mongod_stopped failed: '
        basic_stopped_check(basemsg,
                            self.locations['lock_file_loc'])
