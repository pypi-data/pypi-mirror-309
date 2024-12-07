from enum import Enum
import time

class Note(Enum):

    C1 = 32.703; CS1 = 34.648; D1 = 36.708; DS1 = 38.891; E1 = 41.203; F1 = 43.654; FS1 = 46.249; G1 = 48.999; GS1 = 51.913; A1 = 55.000; AS1 = 58.270; B1 = 61.735
    C2 = 65.406; CS2 = 69.296; D2 = 73.416; DS2 = 77.782; E2 = 82.407; F2 = 87.307; FS2 = 92.499; G2 = 97.999; GS2 = 103.826; A2 = 110.000; AS2 = 116.541; B2 = 123.471
    C3 = 130.813; CS3 = 138.591; D3 = 146.832; DS3 = 155.564; E3 = 164.814; F3 = 174.614; FS3 = 184.997; G3 = 195.998; GS3 = 207.652; A3 = 220.000; AS3 = 233.082; B3 = 246.942
    C4 = 261.626; CS4 = 277.183; D4 = 293.665; DS4 = 311.127; E4 = 329.628; F4 = 349.228; FS4 = 369.994; G4 = 391.995; GS4 = 415.305; A4 = 440.000; AS4 = 466.164; B4 = 493.883

    C5 = 523.251; CS5 = 554.365; D5 = 587.330; DS5 = 622.254; E5 = 659.255; F5 = 698.457; FS5 = 739.989; G5 = 783.991; GS5 = 830.609; A5 = 880.000; AS5 = 932.328; B5 = 987.767
    C6 = 1046.502; CS6 = 1108.731; D6 = 1174.659; DS6 = 1244.508; E6 = 1318.510; F6 = 1396.913; FS6 = 1479.978; G6 = 1567.982; GS6 = 1661.219; A6 = 1760.000; AS6 = 1864.655; B6 = 1975.533
    C7 = 2093.005; CS7 = 2217.461; D7 = 2349.318; DS7 = 2489.016; E7 = 2637.021; F7 = 2793.826; FS7 = 2959.956; G7 = 3135.964; GS7 = 3322.438; A7 = 3520.000; AS7 = 3729.310; B7 = 3951.066	
    C8 = 4186.009; CS8 = 4434.922; D8 = 4698.637; DS8 = 4978.032; E8 = 5274.042; F8 = 5587.652; FS8 = 5919.912; G8 = 6271.928; GS8 = 6644.876; A8 = 7040.000; AS8 = 7458.620; B8 = 7902.133

class Drone():
    
    def __init__(self, is_synchronize = False):
        # Drone property
        self._pitch = 0
        self._roll = 0
        self._throttle = 0
        self._yaw = 0

        # UPD property
        self._udp_ip = "127.0.0.1"
        self._udp_port = 5000
        import socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.connect((self._udp_ip, self._udp_port))

        # Real drone property
        self.drone = None

            

    #---------------------------------------
    # API
    #---------------------------------------
    def pair(self):
        self._send_to_server("pair")
        time.sleep(1)
    
    def close(self):
        return
    
    def land(self):
        self._send_to_server("land")
    
    def takeoff(self):
        self._send_to_server("takeoff")
        time.sleep(1)

    def avoid_wall(self, timeout=2, distance=70):
        self._send_to_server(f"avoid_wall,{timeout},{distance}")
        time.sleep(timeout)
    
    def detect_wall(self, distance=50):
        return self._get_from_server(f"detect_wall,{distance}", 1)[0] == b'\x01'
    
    def hover(self, duration=0.01):
        time.sleep(duration)

    def move(self, duration):
        self._send_to_server(f"go,{self._roll},{self._pitch},{self._yaw},{self._throttle},{duration}")
        time.sleep(duration)

    def reset_move(self, attmepts):
        self._pitch = 0
        self._roll = 0
        self._yaw = 0
        self._throttle = 0

    def set_pitch(self, power):
        self._pitch = power

    def set_roll(self, power):
        self._roll = power

    def set_throttle(self, power):
        self._throttle = power

    def set_yaw(self, power):
        self._yaw = power

    def turn_left(self, degree=90, timeout=3):
        self._send_to_server(f"turn_left,{degree},{timeout}")
        time.sleep(timeout)

    def turn_right(self, degree=90, timeout=3):
        self._send_to_server(f"turn_right,{degree},{timeout}")
        time.sleep(timeout)
    
    def go(self, roll, pitch, yaw, throttle, duration):
        self._send_to_server(f"go,{roll},{pitch},{yaw},{throttle},{duration}")
        time.sleep(duration)

    def move_forward(self, distance, unit="cm", speed=1):
        self._send_to_server(f"move_forward,{distance},{unit},{speed}")
        time.sleep(0.001)

    def move_backward(self, distance, unit="cm", speed=1):
        self._send_to_server(f"move_backward,{distance},{unit},{speed}")
        time.sleep(0.001)
    
    def move_left(self, distance, unit="cm", speed=1):
        self._send_to_server(f"move_left,{distance},{unit},{speed}")
        time.sleep(0.001)
    
    def move_right(self, distance, unit="cm", speed=1):
        self._send_to_server(f"move_right,{distance},{unit},{speed}")
        time.sleep(0.001)

    def drone_LED_off(self):
        self._send_to_server("set_drone_LED,0,0,0,0")
        time.sleep(0.005)

    def set_drone_LED(self, r, g, b, brightness):
        self._send_to_server(f"set_drone_LED,{r},{g},{b},{brightness}")
        time.sleep(0.005)

    def drone_buzzer(self, note, duration):
        value = 0
        if isinstance(note, int):
            value = note
        elif isinstance(note, Note):
            value = note.value
        else:
            print("Input must be Note or integer.")
            return
        self._send_to_server(f"start_drone_buzzer,{value},{duration}")
        time.sleep(duration/1000)
        self._send_to_server("end_drone_buzzer," + str(value))
    
    def start_drone_buzzer(self, note):
        value = 0
        if isinstance(note, int):
            value = note
        elif isinstance(note, Note):
            value = note.value
        else:
            print("Input must be Note or integer.")
            return
        self._send_to_server(f"start_drone_buzzer,{value}")
    
    def end_drone_buzzer(self):
        self._send_to_server("end_drone_buzzer,")

    def get_bottom_range(self, unit="cm"):
        import struct
        result = self._get_from_server(f"get_bottom_range,{unit}", 4)[0]
        [x] = struct.unpack('f', result)
        return x
    
    def get_front_range(self, unit="cm"):
        import struct
        result = self._get_from_server(f"get_front_range,{unit}", 4)[0]
        [x] = struct.unpack('f', result)
        return x

    #---------------------------------------
    # Custom API
    #---------------------------------------
    def grab(self):
        self._send_to_server("grab")
        time.sleep(1)

    def release(self):
        self._send_to_server("release")
        time.sleep(1)

    def reset_position_and_rotation(self):
        self._send_to_server("reset_position_and_rotation")
        time.sleep(0.02)

    #---------------------------------------
    # Custom API
    #---------------------------------------
    def teleport_to(self, x, y, z):
        self._send_to_server(f"teleport_to,{x},{y},{z}")
        time.sleep(0.02)

    def teleport_by(self, x=0, y=0, z=0):
        self._send_to_server(f"teleport_by,{x},{y},{z}")
        time.sleep(0.02)

    def teleport_yaw_to(self, yaw):
        self._send_to_server(f"teleport_yaw_to,{yaw}")
        time.sleep(0.02)

    def teleport_yaw_by(self, yaw):
        self._send_to_server(f"teleport_yaw_by,{yaw}")
        time.sleep(0.02)

    def set_restart_pos(self, x, z):
        self._send_to_server(f"set_restart_pos,{x},{z}")
        time.sleep(0.02)

    def set_restart_yaw(self, yaw):
        self._send_to_server(f"set_restart_yaw,{yaw}")
        time.sleep(0.02)

    #---------------------------------------
    # Custom private method
    #---------------------------------------

    def _send_to_server(self, data):
        self._socket.send(str(data).encode())

    def _get_from_server(self, data, size):
        self._socket.send(str(data).encode())
        return self._socket.recvfrom(size)
        
    def __del__(self):
        if self._socket:
            self._socket.close() 