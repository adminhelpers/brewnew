
from pypresence import Presence 
import time

client_id = 810036641963704331
RPC = Presence(client_id)
RPC.connect()

while True:
    RPC.update(state="Python Developer", large_image = '1', small_image = '2', buttons = [{"label" : "VK" , "url" : "https://vk.com/dollarbabys"},{"label" : "Сделать заказ", "url" : "https://vk.com/dollarbabys"}])
    time.sleep(100000)
                                                  