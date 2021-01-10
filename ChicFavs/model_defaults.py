from .models import *

def get_or_create_branch():
    return Branch.objects.get_or_create(name="Head office")[0]

print(type(get_or_create_branch().id))