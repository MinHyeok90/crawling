import subprocess
import sys
import os
import json


def log_success_decorator(func):
    def warp_func(*args, **kwargs):
        start = 'echo "' + func.__name__ + '" Start'
        done = 'echo "' + func.__name__ + '" Done'
        subprocess.call(start, shell=True)
        res = func(*args, **kwargs)
        subprocess.call(done, shell=True)
        return res

    return warp_func

@log_success_decorator
def get_env(mode):
    BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "app/_conf/settings/")
    if mode == "production":
        file_title = 'production.json'
    else:
        file_title = 'development.json'
    with open(os.path.join(BASE_DIR, file_title), encoding='UTF-8-sig') as env_contents:
        env = json.load(env_contents)
    return env

@log_success_decorator
def env_overwriter(env):
    with open(os.path.join(BASE_DIR, 'current_env_mode.json'), 'w+', encoding='UTF-8-sig') as current_env:
        current_env.write(json.dumps(env, ensure_ascii=False))


@log_success_decorator
def update_requirements():
    subprocess.call('pip3 freeze > requirements.txt', shell=True)


@log_success_decorator
def docker_build(image_name):
    subprocess.call('docker build -t ' + image_name + ' .', shell=True)
    subprocess.call('docker image prune -f', shell=True)


@log_success_decorator
def push_container(image_name):
    subprocess.call('docker push ' + image_name, shell=True)


@log_success_decorator
def docker_stop_rm(container_name):
    # if platform.system() == 'Windows':
    #     res = subprocess.call('docker ps -a | findstr "app"', shell=True)
    # else:
    #     res = subprocess.call('docker ps -a | grep "app"', shell=True)

    subprocess.call('docker stop ' + container_name, shell=True)
    subprocess.call('docker rm ' + container_name, shell=True)


@log_success_decorator
def docker_run_only_one(container_name, image_name):
    # run one time
    subprocess.call(
        'docker run -t -d -e TZ=Asia/Seoul --name ' + container_name + ' ' + image_name, shell=True)


@log_success_decorator
def docker_run_keep_container(container_name, image_name):
    # run and keep container
    subprocess.call(
        'docker run -t -d -e TZ=Asia/Seoul --name ' + container_name + ' ' + image_name + ' tail -f /dev/null', shell=True)


@log_success_decorator
def docker_cp_private_files(container_name):
    subprocess.call(
        'docker cp /var/keys/my_key ' + container_name + ':/root/app/notifier/my_key', shell=True)
    subprocess.call(
        'docker cp /var/keys/my_chat_room ' + container_name + ':/root/app/notifier/my_chat_room', shell=True)


@log_success_decorator
# Deprecated
def docker_additional_job():
    subprocess.call(
        'docker exec app pip uninstall python-telegram-bot -y', shell=True)
    subprocess.call(
        'docker exec app pip install python-telegram-bot', shell=True)
    subprocess.call(
        'docker exec -d app python jungo_car_service.py', shell=True)


def show_log_for_success(container_name):
    print("\n")
    print("============= Log after Container Run =============")
    try:
        subprocess.call('docker logs --follow ' + container_name, shell=True)
    except:
        print("Good Lock!")


@log_success_decorator
def docker_build_run():
    if len(sys.argv) > 1:
        mode = "production"
    else:
        mode = "development"
        
    print("--- Build : " + mode)
    env = get_env(mode)
    image_name = env['image_name']
    container_name = env['container_name']
    
    env_overwriter(env)    
    # update_requirements() # this is source code resposibility
    docker_build(image_name)
    # push_container(image_name)
    docker_stop_rm(container_name)
    docker_run_only_one(container_name, image_name)
    # docker_run_keep_container(container_name, image_name)
    docker_cp_private_files(container_name)  # for product
    # docker_additional_job()
    # show_log_for_success(container_name)
    print("--- Build end: " + mode)


def test():
    show_log_for_success()

# test()
docker_build_run()
