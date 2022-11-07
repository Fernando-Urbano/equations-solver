# System of Equations Solver
The equation solver class is used to solve any system of equations and can include union and interception of groups.

Rules:
- every variable must start with lowercase.
- to write union between variable `a` and variable `b`: `aUNIb`
- to write interception between variable `a` and variable `b`: `aINTb`
- every equation in the system must be written as a string.

Start by creating an instance of the class which will work as that system of equations:

`a = Groups()`

Add any information you want:

```
a.add_information('xUNIy = 250')
a.add_information('x = 100')
a.add_information('y = 200')
```

To check the solution look at the attribute `solution`:

```
print(a.solution)
```
Result:
```
[{self.x: 100, self.xINTy: 50, self.xUNIy: 250, self.y: 200}]
```


