import paho.mqtt.client as mqtt
import random
from typing import Callable
import threading
import time
import erspi.packet as packet


class erspi:
    def __init__(self,game_name: str, controller_name: str, callback : Callable[[packet.erspacket],None], get_status_update : Callable[[],packet.erspacket]) -> None:
        self._base_mqtt_topic = "{}/{}/".format(game_name,controller_name)
        self.time_between_updates = 1.0
        self.last_update = 0.0
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,controller_name + str(random.randint(1,99999)))
        self.client.on_connect = self._on_connect
        self.client._on_message = self._on_message
        self.client.will_set("dead")
        self.callback = callback
        self.get_status_update = get_status_update

    
    def _on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        client.subscribe(self._base_mqtt_topic + "command")


    def _on_message(self,client, userdata, msg) -> packet.erspacket:
        message_string : str = msg.payload.decode('utf-8')
        message_parts : list[str] = message_string.split("?")
        packet : packet.erspacket = packet.erspacket()
        packet.command = message_parts[0]

        if len(message_parts) == 1:
            self.callback(packet)
            return

        data_parts : list[str] = message_parts[1].split("&")

        for key_value_pair in data_parts:
            key_value_parts : list[str] = key_value_pair.split("=")
            if len(key_value_parts) != 2:
                continue
            
            if key_value_parts[1].isdigit():
                packet.add_value(key_value_parts[0],float(key_value_parts[1]))
            else:
                packet.add_value(key_value_parts[0],key_value_parts[1])
        self.callback(packet)


    def begin(self, broker : str) -> None:
        self.client.connect(broker,keepalive=5)
        self.client.loop_start()
        self._thread = threading.Thread(target=self._thread_main, name=f"erspy-{self.client._client_id.decode()}",daemon=True)
        self._kill_thread = False
        self._thread.start()
    

    def send_message(self,message : packet.erspacket) -> None:
        if not self.client.is_connected():
            return
        self.client.publish(self._base_mqtt_topic + "messages",str(message))
    

    def _thread_main(self) -> None:
        while not self._kill_thread:
            current_time = time.monotonic()
            if current_time < self.last_update + self.time_between_updates:
                continue
            self.send_status_update()
            self.last_update = current_time


    def send_status_update(self) -> None:
        if not self.client.is_connected():
            return
        packet : packet.erspacket = self.get_status_update()
        self.client.publish(self._base_mqtt_topic + "status",str(packet))

    
    def cleanup(self) -> None:
        self._kill_thread = True
        self._thread.join()
        self.client.loop_stop()


