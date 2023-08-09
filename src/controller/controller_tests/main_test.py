import sys
print(sys.path)
sys.path.append("..")
print(sys.path)
from main import squared

print(squared(4))