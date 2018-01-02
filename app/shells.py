def first(f):
    def wrapper(*args, **kwargs):
        return wrapper(*args, **kwargs)
    return f

def second(params):
    def wrapper(f):
        def inner(*args, **kwargs):
            return inner(*args, **kwargs)
        return f

@first
@second('asdsad')
def main():
    pass
