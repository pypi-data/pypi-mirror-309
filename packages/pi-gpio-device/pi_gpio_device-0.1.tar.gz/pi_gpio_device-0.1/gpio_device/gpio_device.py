import RPi.GPIO as GPIO

class GpioDevice:
    def __init__(self, pin_no, mode='input', pwm_freq=None):
        """
        Initializes a GPIO pin for different purposes.

        Args:
            pin_no (int): GPIO pin number.
            mode (str): The mode in which the GPIO pin will operate. Options are 'input', 'output', 'pwm'.
            pwm_freq (int, optional): Frequency for PWM if mode is 'pwm'. Defaults to None.
        """
        self.pin_no = pin_no
        self.mode = mode
        self.pwm = None

        # Configure GPIO
        GPIO.setmode(GPIO.BCM)

        if self.mode == 'input':
            GPIO.setup(self.pin_no, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif self.mode == 'output':
            GPIO.setup(self.pin_no, GPIO.OUT)
        elif self.mode == 'pwm' and pwm_freq:
            GPIO.setup(self.pin_no, GPIO.OUT)
            self.pwm = GPIO.PWM(self.pin_no, pwm_freq)
        else:
            raise ValueError("Invalid mode or missing PWM frequency.")

    def read_input(self):
        """
        Reads input value from a GPIO pin. Only relevant for 'input' mode.
        Returns:
            bool: True if input is HIGH, False otherwise.
        """
        if self.mode == 'input':
            return GPIO.input(self.pin_no) == GPIO.HIGH
        else:
            raise Exception("GPIO is not configured as input.")

    def set_output(self, state):
        """
        Sets the state of an output pin. Only relevant for 'output' mode.
        
        Args:
            state (bool): True for HIGH (on), False for LOW (off).
        """
        if self.mode == 'output':
            GPIO.output(self.pin_no, GPIO.HIGH if state else GPIO.LOW)
        else:
            raise Exception("GPIO is not configured as output.")

    def start_pwm(self, duty_cycle):
        """
        Starts PWM on the pin. Only relevant for 'pwm' mode.
        
        Args:
            duty_cycle (float): The duty cycle (0.0 to 100.0).
        """
        if self.mode == 'pwm' and self.pwm:
            self.pwm.start(duty_cycle)
        else:
            raise Exception("GPIO is not configured for PWM or PWM not initialized.")

    def stop_pwm(self):
        """
        Stops PWM on the pin.
        """
        if self.mode == 'pwm' and self.pwm:
            self.pwm.stop()
        else:
            raise Exception("GPIO is not configured for PWM or PWM not initialized.")

    def cleanup(self):
        """
        Cleans up the GPIO settings.
        """
        GPIO.cleanup()
