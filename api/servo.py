import pigpio
import time

SERVO_GPIO = 18  # Pino GPIO onde o servo está conectado

pi = pigpio.pi()  # Inicia a biblioteca pigpio

def open_lock():
    pi.set_servo_pulsewidth(SERVO_GPIO, 500)  # Aproximadamente 0°
    time.sleep(0.5)

def close_lock():
    pi.set_servo_pulsewidth(SERVO_GPIO, 1500)  # Aproximadamente 90°
    time.sleep(0.5)

    #pi.set_servo_pulsewidth(SERVO_GPIO, 0)  # Desativa o servo
    #pi.stop()

