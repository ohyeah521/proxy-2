from fabric.contrib.files import exists
from fabric.api import env, local, run, warn_only

REPO_URL = 'https://github.com/lifenglifeng001/proxy.git'

env.hosts = [
        '106.186.23.144',
        '198.58.111.202',
        '66.228.35.131',
        '106.186.112.187',
        '192.81.131.122',
        '173.255.195.118',
        '64.20.37.156',
        '173.214.169.12',
        ]
env.password = 'sm2906'
env.user = 'root'


def deploy():
    proxy_folder = '/root/proxy'
    _install_requirements()
    _create_directory_structure_if_necessary(proxy_folder)
    _get_latest_source(proxy_folder)
    _run_proxy()


def _install_requirements():
    run('sudo apt-get -y --no-upgrade install python-twisted')
    run('sudo apt-get -y --no-upgrade install git')
    with warn_only():
        run("kill `ps -ef | grep proxy.py | grep -v grep | awk '{print $2}'`")


def _create_directory_structure_if_necessary(proxy_folder):
    run('mkdir -p %s' % (proxy_folder,))


def _get_latest_source(proxy_folder):
    if exists(proxy_folder + '/.git'):
        run('cd %s && git fetch' % (proxy_folder))
    else:
        run('git clone %s %s' % (REPO_URL, proxy_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (proxy_folder, current_commit))


def _run_proxy():
    run('python /root/proxy/proxy.py &')
