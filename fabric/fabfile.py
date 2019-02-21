""" Deploy steps """

from fabric import Connection
from fabric import task


try:
    import fab_settings
except ImportError:
    print("Please create a fab_deploy.py file with your settings")
    quit()


HOST = fab_settings.HOST
USER = fab_settings.USER
PATH = fab_settings.REMOTE_PATH
GIT_URL = fab_settings.GIT_URL

@task()
def deploy_production(c):
    """ Deploy to production """
    c = Connection(host=HOST, user=USER)

    if c.run(f"test -d {PATH}", warn=True).failed:
        c.run(f"git clone {GIT_URL} {PATH}")
    else:
        c.run(f"cd {PATH} && git pull")

    restart_docker(c)


@task
def rollback(c, commit):
    """ Rolls back to a previous commit incase of problems"""
    if not c.run(f"test -d {PATH}", warn=True).failed:
        c.run(f"cd {PATH} && git checkout {commit}")
    else:
        print(f"[-] Could not checkout {commit}, '{PATH}' does not exist.")


def restart_docker(c):
    """ Restart the docker container running bookie """
    c.run(f"sudo docker-compose -f {PATH}/prod.yml down")
    c.run(f"sudo docker-compose -f {PATH}/prod.yml up -d")


