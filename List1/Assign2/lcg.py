from functools import reduce
from fractions import gcd
import glibc_random


def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)
 
def calculate_modular_inverse(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    #increment = 0
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * calculate_modular_inverse(states[1] - states[0], modulus) % modulus
    #multiplier = 16807
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    # modulus = 2147483647
    return crack_unknown_multiplier(states, modulus)

def predict_next_value(current_state, modulus, multiplier, increment):
    next_value = (multiplier * current_state + increment) % modulus
    return next_value

def test():
    glibc_random.initialize()
    number_of_initial_values = 10
    number_of_values_to_predict = 5
    initial_values = []
    
    for i in range(number_of_initial_values):
        initial_values.extend([glibc_random.call_glibc_random()])

    algorithm_params = crack_unknown_modulus(initial_values)
    modulus, multiplier, increment = algorithm_params
    print("modulus: {}, multiplier: {}, increment: {}".format(modulus, multiplier, increment))

    predicted_values = []
    current_state = initial_values[-1]
    
    for i in range (number_of_values_to_predict):
        current_state = predict_next_value(current_state, *algorithm_params)
        predicted_values.append(current_state)

    print("Next {} predicted values: {}".format(number_of_values_to_predict, predicted_values))

    actual_values = []

    for i in range(number_of_values_to_predict):
        actual_values.append(glibc_random.call_glibc_random())

    print("Actual {} next values: {}".format(number_of_values_to_predict, actual_values))

test()