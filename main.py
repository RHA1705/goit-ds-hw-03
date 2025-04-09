import connect
from models import Cat


def read_all():
    result = Cat.objects()
    return result

if __name__ == "__main__":
    read_all()
