import subprocess
import platform


def log_success_decorator(func):
    def warp_func(*args, **kwargs):
        start = 'echo "' + func.__name__ + '" Start'
        done = 'echo "' + func.__name__ + '" Done'
        subprocess.call(start, shell=True)
        res = func()
        subprocess.call(done, shell=True)
        return res

    return warp_func


@log_success_decorator
def update_requirements():
    subprocess.call('pip freeze > requirements.txt', shell=True)


@log_success_decorator
def docker_build():
    subprocess.call('docker build -t dufflaa/jungo-car-app:1 .', shell=True)
    subprocess.call('docker image prune -f', shell=True)


@log_success_decorator
def push_container():
    subprocess.call('docker push dufflaa/jungo-car-app:1', shell=True)


@log_success_decorator
def docker_stop_rm():
    if platform.system() == 'Windows':
        res = subprocess.call('docker ps -a | findstr "app"', shell=True)
    else:
        res = subprocess.call('docker ps -a | grep "app"', shell=True)

    if res == 0:
        return
    subprocess.call('docker stop app', shell=True)
    subprocess.call('docker rm app', shell=True)


@log_success_decorator
def docker_run_only_one():
    # subprocess.call('docker run -d --rm --name app dufflaa/jungo-car-app:1', shell=True) # run one time
    subprocess.call('docker run -d --rm --name app dufflaa/jungo-car-app:1 tail -f /dev/null',
                    shell=True)  # run and keep container


@log_success_decorator
def docker_run_keep_container():
    # subprocess.call('docker run -d --rm --name app dufflaa/jungo-car-app:1', shell=True) # run one time
    subprocess.call('docker run -d --rm --name app dufflaa/jungo-car-app:1 tail -f /dev/null',
                    shell=True)  # run and keep container


@log_success_decorator
def docker_build_run():
    update_requirements()
    docker_build()
    # push_container()
    docker_stop_rm()
    docker_run_keep_container()


docker_build_run()
