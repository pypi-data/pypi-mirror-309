import numpy as np

def create_batches(x_train, y_train, batch_size, shuffle=True):
    if shuffle:
        indices = np.arange(len(x_train))
        np.random.shuffle(indices)
        x_train = x_train[indices]
        y_train = y_train[indices]

    batches = []
    for i in range(0, len(x_train), batch_size):
        batches.append((x_train[i:i+batch_size], y_train[i:i+batch_size]))
    return batches


# Xavier initialization with uniform distribution
def xavier_init_uniform(input_size, output_size):
        limit = np.sqrt(6 / (input_size + output_size))
        return np.random.uniform(-limit, limit, (output_size, input_size))

# Xavier initialization with normal distribution
def xavier_init_normal(input_size, output_size):
    stddev = np.sqrt(2 / (input_size + output_size))
    return np.random.normal(0, stddev, (output_size, input_size))

# He initialization with uniform distribution
def he_init_uniform(input_size, output_size):
    limit = np.sqrt(6 / input_size)
    return np.random.uniform(-limit, limit, (output_size, input_size))

# He initialization with normal distribution
def he_init_normal(input_size, output_size):
    stddev = np.sqrt(2 / input_size)
    return np.random.normal(0, stddev, (output_size, input_size))