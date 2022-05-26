#!/usr/bin/env python3

import torch
from copy import copy, deepcopy

#
# This example illustrates when torch builds a gradient graph,
# how it can be prevented, and when torch shares or copies tensor
# data

def print_sep():
    print()
    print("---------------------------------------------------------------")
    print()

print_sep()

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
print(f'{"x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True):":55}', x)
y = x.clone()
print(f'{"y = x.clone():":55}', y)
z = y.detach()
print(f'{"z = y.detach():":55}', z)
print()

print("x[1] = 0 is not possible because x is a leaf variable that requires gradient.")
print("Note that z does not require a gradient as it was detached.")
print()

y[1] = 0
print("After y[1] = 0:")
print(f'{"x = ":55}', x)
print(f'{"y = ":55}', y)
print(f'{"z = ":55}', z)
print()

z[1] = 5
print("After z[1] = 5:")
print(f'{"x = ":55}', x)
print(f'{"y = ":55}', y)
print(f'{"z = ":55}', z)

print_sep()

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
print(f'{"x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True):":55}', x)

y = copy(x)
print(f'{"y = copy(x):":55}', y)
print()

print("x[1] = 0 is not possible because x is a leaf variable that requires gradient.")
print("y[1] = 0 is not possible because y is a leaf variable that requires gradient.")
print("Note that y is a second leaf node (not a child of x as previously).")

print_sep()

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
print(f'{"x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True):":55}', x)
y = deepcopy(x)
print(f'{"y = deepcopy(x):":55}', y)
print()

print("x[1] = 0 is not possible because x is a leaf variable that requires gradient.")
print("y[1] = 0 is not possible because y is a leaf variable that requires gradient.")
print("Note that y is a second leaf node (not a child of x as previously).")

print_sep()

x = torch.tensor([1.0, 2.0, 3.0])
print("requires_grad = False by default")
print()
print(f'{"x = torch.tensor([1.0, 2.0, 3.0]):":55}', x)
y = copy(x)
print(f'{"y = copy(x):":55}', y)
print()

x[1] = 0
print("After x[1] = 0:")
print(f'{"x = ":55}', x)
print(f'{"y = ":55}', y)
print()

y[1] = 5
print("After y[1] = 5:")
print(f'{"x = ":55}', x)
print(f'{"y = ":55}', y)

print_sep()

x = torch.tensor([1.0, 2.0, 3.0])
print("requires_grad = False by default")
print()
print(f'{"x = torch.tensor([1.0, 2.0, 3.0]):":55}', x)
y = deepcopy(x)
print(f'{"y = deepcopy(x):":55}', y)
print()

x[1] = 0
print("After x[1] = 0:")
print(f'{"x = ":55}', x)
print(f'{"y = ":55}', y)
print()

y[1] = 5
print("After y[1] = 5:")
print(f'{"x = ":55}', x)
print(f'{"y = ":55}', y)

print_sep()

