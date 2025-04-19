import connect
from models import Cat



def read_all():
    for cat in Cat.objects():
        print(f"Name: {cat.name}, Age: {cat.age}, Features: {cat.features}")

if __name__ == "__main__":
    read_all()
