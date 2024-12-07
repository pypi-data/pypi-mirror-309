
def printf(obj = ''):
    print(obj, flush = True)

def pickle_object(obj, path):
    import pickle
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def unpickle_object(path):
    import pickle
    with open(path, 'rb') as f:
        obj = pickle.load(f)
        return(obj)

def log_timestamp(message = ''):
    import datetime
    printf(f'{str(datetime.datetime.now())}: {message}')


