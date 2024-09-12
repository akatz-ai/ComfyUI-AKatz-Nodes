import numpy as np
import re

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

def apply_easing(schedule, mode='linear'):
    if mode not in easing_functions:
        raise ValueError(f"Easing mode '{mode}' is not supported.")

    schedule_arr = np.array(schedule, dtype=float)

    if not np.all((schedule_arr >= -1) & (schedule_arr <= 1)):
        min_val = schedule_arr.min()
        max_val = schedule_arr.max()
        normalized_numbers = (schedule_arr - min_val) / (max_val - min_val)
        schedule_arr = easing_functions[mode](normalized_numbers)
        schedule_arr = schedule_arr * (max_val - min_val) + min_val
    else:
        schedule_arr = easing_functions[mode](schedule_arr)

    return schedule_arr

def safe_eval(expr, t_val=1, end_frame=1, custom_vars={}):
    allowed_funcs = ['where', 'invert', 'put', 'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs', 'arcsin', 'arccos', 'arctan', 'power', 'pi', 'arctan2']
    allowed_names = {name: getattr(np, name) for name in allowed_funcs}
    allowed_names.update({
        "np": np,
        "t": t_val,
        "z": end_frame,
        "end_frame": end_frame,
        "len": len,
    })
        
    if custom_vars and isinstance(custom_vars, dict):
        allowed_names.update(custom_vars)

    try:
        return eval(expr, {"__builtins__": None}, allowed_names)
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {str(e)}")

class KeyframeScheduler:
    def __init__(self, end_frame=0, custom_vars={}):
        self.keyframes = []
        self.end_frame = end_frame
        self.custom_vars = custom_vars

    def parse_keyframes(self, schedule_str):
        self.keyframes = []
        pattern = re.compile(r'\[(.*?)\]')
        
        schedule_str = schedule_str.replace('\n', ' ').replace('\r', ' ').strip()
        segments = [segment.strip() for segment in schedule_str.split(",")]
        for segment in segments:
            if segment.strip():
                index_expr, value_expr = [expr.strip() for expr in segment.split(":")]

                if pattern.match(index_expr):
                    expr = pattern.search(index_expr).group(1)
                    try:
                        index = int(safe_eval(expr, 0, self.end_frame, self.custom_vars))
                    except Exception as e:
                        raise ValueError(f"Error evaluating index expression '{expr}': {str(e)}")
                elif index_expr == "end_frame" or index_expr == "z":
                    if self.end_frame != 0:
                        index = self.end_frame - 1
                    else:
                        raise ValueError("`end_frame` must be specified and greater than 0 to use 'z'.")
                else:
                    index = int(index_expr)

                if value_expr.startswith("(") and value_expr.endswith(")"):
                    value_expr = value_expr[1:-1]

                self.keyframes.append((index, value_expr))

    def is_numeric(self, val):
        if isinstance(val, (int, float)):
            return True
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False

    def generate_schedule(self, schedule_str, easing_mode='None', ndigits=2):
        self.parse_keyframes(schedule_str)
        if not self.keyframes:
            return []

        max_index = self.end_frame if self.end_frame != 0 else max(self.keyframes, key=lambda kf: kf[0])[0] + 1
        schedule = np.zeros(max_index)

        for i in range(len(self.keyframes)):
            start_index, start_expr = self.keyframes[i]
            end_index = self.keyframes[i+1][0] if i+1 < len(self.keyframes) else max_index

            start_val = safe_eval(start_expr, start_index, self.end_frame, self.custom_vars)
            end_val = safe_eval(self.keyframes[i+1][1], end_index, self.end_frame, self.custom_vars) if i+1 < len(self.keyframes) else start_val

            start_numeric = self.is_numeric(start_expr)
            end_numeric = self.is_numeric(self.keyframes[i+1][1]) if i+1 < len(self.keyframes) else True

            if start_index == end_index:
                schedule[start_index] = start_val
            elif start_numeric and end_numeric:
                start_val = float(start_val)
                end_val = float(end_val)
                for j in range(start_index, end_index):
                    t = j
                    progress = (j - start_index) / (end_index - start_index) if end_index != start_index else 0
                    schedule[j] = start_val + (end_val - start_val) * progress
            else:
                for j in range(start_index, end_index):
                    t = j
                    schedule[j] = safe_eval(start_expr, t, self.end_frame, self.custom_vars)

        if easing_mode != "None":
            schedule = apply_easing(schedule, easing_mode)

        schedule = np.round(schedule, ndigits)

        return schedule.tolist()