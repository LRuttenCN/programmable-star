from time import sleep
from datetime import datetime, timedelta
import math
from gpiozero import LEDBoard

# partying until 4AM is allowed. After that, it's embarrassing. Go to bed.
# Setting this to 4AM means that the star won't instantly turn off after 12
DAY_START_HOUR = 4  # Start over at 4AM
BEER_HOUR = 16      # Lights up fully at 16:00
ON_BRIGHTNESS = 0.1 # How brights leds should be


class Star(LEDBoard):
    # Set up a Star using GPIO Zero to build a class.
    # To use:
    # star = Star() for a simple instance using LED class.
    # star = Star(pwm=True) for a version which can use PWM.
    # See example files in this repo for more examples of use...
    def __init__(self, pwm=False, initial_value=False, pin_factory=None):
        super(Star, self).__init__(
            outer=LEDBoard(
                A=8,B=7,C=12,D=21,E=20,F=16,G=26,H=19,I=13,J=6,K=5,L=11,M=9,
                N=10,O=22,P=27,Q=17,R=4,S=3,T=14,U=23,V=18,W=15,X=24,Y=25,
                pwm=pwm, initial_value=initial_value,
                _order=('A','B','C','D','E','F','G','H','I','J','K','L',
                        'M','N','O','P','Q','R','S','T','U','V','W','X','Y'),
                pin_factory=pin_factory),
            inner=2,
            pwm=pwm, initial_value=initial_value,
            _order=('inner','outer'),
            pin_factory=pin_factory
            )


if __name__ == '__main__':
    star = Star(pwm=True)
    try:
        leds = list(star.leds)
        # Rotate the list so the center comes last
        leds.append(leds.pop(0))
        while True:
            now = datetime.now()
            if DAY_START_HOUR >= now.hour or now.hour >= BEER_HOUR:
                # It's beer time!
                pulse_index = 25
                led_filter = [ON_BRIGHTNESS] * 26

            else:
                # No beer yet :(
                # Count hours until 16:00
                led_filter = [0] * 26
                now = datetime.now()
                next_beer_time = datetime(now.year, now.month, now.day, hour=BEER_HOUR)
                duration_in_seconds = (next_beer_time - now).seconds
                max_duration = BEER_HOUR * 3600
                pulse_index = 25 - math.floor(duration_in_seconds / max_duration * 25)
                led_filter[0:pulse_index] = [ON_BRIGHTNESS] * (pulse_index + 1)

            for idx, led in enumerate(leds):
                led.value = led_filter[idx]
                if idx == pulse_index:
                    led.pulse()
                sleep(0.5)

            sleep(60)
            star.off()
            sleep(2)

    except KeyboardInterrupt:
        star.close()
