# python-vector-swizzling

The `vector_swizzling` library provides flexible and intuitive vector manipulation with swizzling capabilities, designed to resemble GLSL vector handling for 2D, 3D, and 4D vectors.

## Overview
`SVec` is a base class for representing vectors with a list of components and a lookup table allowing swizzling. Swizzling lets you access components in different combinations or orders, similar to GLSL's swizzling. See [Swizzling on Wikipedia](https://en.wikipedia.org/wiki/Swizzling_(computer_graphics)) for more information.

### Classes and Structure
The main `SVec` class has three subclasses for specific dimensions:
- **`SVec2`**: for 2D vectors.
- **`SVec3`**: for 3D vectors.
- **`SVec4`**: for 4D vectors.

These subclasses come with dimension-specific operations, such as `srotate` for `SVec2` and `scross` for `SVec3`.

### Component Lookup Table
The swizzling table maps to the following indices:
- `'x' or 'r' = 0`
- `'y' or 'g' = 1`
- `'z' or 'b' = 2`
- `'w' or 'a' = 3`

This table lets you use letters from both Cartesian (`x`, `y`, `z`, `w`) and color (`r`, `g`, `b`, `a`) spaces interchangeably.

## Usage Examples

### Declaring Vectors
You can declare vectors in different ways:
```python
# Standard declaration
a = SVec2(1, 2)
b = SVec3(1, 2, 3)
c = SVec4(1, 2, 3, 4)
d = SVec4(4, 3, 2, 1)

# Using list as components
a = SVec2([1, 2])
b = SVec3([1, 2], 3)
c = SVec4(1, 2, [3, 4])
d = SVec4([4, 3, 2], 1)

# Using vectors as components
b = SVec3(a, 3)
c = SVec4(b, 4)`
d = SVec4(c.wzy, 1)
```

### Swizzling Vectors
You can assign to and operate on swizzled vectors, as well passing them as function arguments:
```python
# Assigning and operating on swizzled vectors
b.xy = a.xy + b.yx

# Swizzling with RGBA space
d.xyzw = d.rgba

# Swizzling an SVec2 into an SVec3 and calling scross
cross_vec = scross(a.xyx, b)

```

### Swizzling quirks
This module allows higher dimensional swizzles and swizzle chaining:
```python
# Swizzle an SVec4 into a 7D SVec and call a dimension agnostic function on it
normalized_7D_vector = snormalize(d.xyzwxyz)

# Swizzle chaining is permitted but only works for the first 4 components, just like GLSL
d.xyzwxyz.xyzw
            #^ You run out of swizzles here
```
### Vectors as lists
Vectors are just cool lists, so you can use them as such
```python
# Iterate over vector components
for i in d.xyzwxyz:
    print(i)

# Assign to a component with its index
d[3] = 1
```
