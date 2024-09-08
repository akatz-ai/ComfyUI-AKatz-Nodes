import numpy as np

# Credit to https://github.com/get-salt-AI/SaltAI_AudioViz/tree/main for the easing function code

# Easing
def ease_in(t):
    return np.power(t, 3)

def ease_out(t):
    return 1 - np.power(1 - t, 3)

def ease_in_out(t):
    return np.where(t < 0.5, 4 * np.power(t, 3), 1 - np.power(-2 * t + 2, 3) / 2)

def bounce_out(t):
    n1 = 7.5625
    d1 = 2.75
    conditions = [
        t < 1 / d1,
        (t >= 1 / d1) & (t < 2 / d1),
        (t >= 2 / d1) & (t < 2.5 / d1),
        t >= 2.5 / d1
    ]
    functions = [
        lambda t: n1 * t * t,
        lambda t: n1 * (t - 1.5 / d1) ** 2 + 0.75,
        lambda t: n1 * (t - 2.25 / d1) ** 2 + 0.9375,
        lambda t: n1 * (t - 2.625 / d1) ** 2 + 0.984375
    ]
    return np.piecewise(t, conditions, functions)

def square(t):
    return np.where(t < 0.5, 0, 1)

def sawtooth(t, repetitions=4):
    return (t * repetitions) % 1

def bump_dip(t):
    return np.where(
        t < 0.3, t**2,
        np.where(
            t < 0.6, np.abs(t - 0.45) * 4,
            1 - ((t - 0.6) / 0.4)**2
        )
    )

def exponential_in_out(t):
    return np.where(
        t < 0.5,
        np.power(2, 20 * t - 10) / 2,
        (2 - np.power(2, -20 * t + 10)) / 2
    )

# Easing functions dictionary
easing_functions = {
    'linear': lambda t: t,
    'ease-in': ease_in,
    'ease-out': ease_out,
    'ease-in-out': ease_in_out,
    'bounce-in': lambda t: 1 - bounce_out(1 - t),
    'bounce-out': bounce_out,
    'bounce-in-out': lambda t: np.where(t < 0.5, (1 - bounce_out(1 - 2 * t)) / 2, (1 + bounce_out(2 * t - 1)) / 2),
    'sinusoidal-in': lambda t: 1 - np.cos((t * np.pi) / 2),
    'sinusoidal-out': lambda t: np.sin((t * np.pi) / 2),
    'sinusoidal-in-out': lambda t: -(np.cos(np.pi * t) - 1) / 2,
    'cubic': lambda t: t ** 4,
    'square': square,
    'sawtooth': lambda t: sawtooth(t),
    'triangle': lambda t: 2 * np.abs(t - 0.5),
    'bump-dip': bump_dip,
    'exponential-in': lambda t: np.power(2, 10 * (t - 1)),
    'exponential-out': lambda t: 1 - np.power(2, -10 * t),
    'exponential-in-out': exponential_in_out
}