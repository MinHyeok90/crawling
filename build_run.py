import subprocess


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
    # if platform.system() == 'Windows':
    #     res = subprocess.call('docker ps -a | findstr "app"', shell=True)
    # else:
    #     res = subprocess.call('docker ps -a | grep "app"', shell=True)

    subprocess.call('docker stop app', shell=True)
    subprocess.call('docker rm app', shell=True)


@log_success_decorator
def docker_run_only_one():
    # run one time
    subprocess.call('docker run -t -d  --name app dufflaa/jungo-car-app:1', shell=True)


@log_success_decorator
def docker_run_keep_container():
    # run and keep container
    subprocess.call('docker run -t -d --name app dufflaa/jungo-car-app:1 tail -f /dev/null', shell=True)


@log_success_decorator
def docker_cp_private_files():
    subprocess.call('docker cp my_key app:/app/my_key', shell=True)
    subprocess.call('docker cp my_chat_room app:/app/my_chat_room', shell=True)


@log_success_decorator
# Deprecated
def docker_additional_job():
    subprocess.call('docker exec app pip uninstall python-telegram-bot -y', shell=True)
    subprocess.call('docker exec app pip install python-telegram-bot', shell=True)
    subprocess.call('docker exec -d app python jungo_car_service.py', shell=True)


def show_log_for_success():
    print("\n")
    print("============= Log after Container Run =============")
    subprocess.call('docker logs app', shell=True)


@log_success_decorator
def docker_build_run():
    update_requirements()
    docker_build()
    # push_container()
    docker_stop_rm()
    docker_run_only_one()
    # docker_run_keep_container()
    docker_cp_private_files()
    # docker_additional_job()
    show_log_for_success()


def test():
    show_log_for_success()

# test()
docker_build_run()
