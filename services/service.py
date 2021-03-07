from time import sleep
from modules.vk import Vk

def check_messages():
    vk = Vk()
    while (True):
        sleep(10)
        posts = vk.get_posts()
        for item in reversed(posts['items']):
            vk.publish_post(item)
            vk.delete_post(item)



