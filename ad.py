import uiautomator2 as u2
import threading

class StateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, name, state):
        self.states[name] = state

    def set_state(self, name):
        self.current_state = self.states[name]

    def run(self, device):
        return self.current_state(device)

state_machine = StateMachine()
state_machine.add_state('state1', state1)  
state_machine.set_state('state1')   

d = u2.UIAutomator2()
devices = []
for i in range(1, 5):  
    try:
        devices.append(d.device(f'PHONE{i}'))
    except u2.exceptions.DeviceConnectionError:
        break
        
def thread_phone(device): 
    while True:
        state_machine.run(device)

threads = []
for device in devices:
    threads.append(threading.Thread(target=thread_phone, args=(device,)))
for thread in threads:
    thread.start()

def state1(device): 
    if device.device_info['serial'] == 'PHONE1':
        device.click(100, 100)                 
    elif device.device_info['serial'] == 'PHONE2': 
        device.swipe()        
    elif device.device_info['serial'] == 'PHONE3':
        device.press('back')
    else: 
        device.press('home')