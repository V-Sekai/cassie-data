# Curves data

Each file contains all polylines from the final state of a given sketch. The strokes we store here are the **input strokes**, that haven't been neatened or smoothed in any way. We provide this data believing that it could be useful for further work on 3D sketch processing, which would work on raw user input.

## Examples of use

* [Python script that displays a sketch](../../scripts/example_curves_file.py)

## .curves format

The `.curves` format is extremely simple:

```js
v 10
x1 y1 z1
x2 y2 z2
...
x10 y10 z10
v 20
x1 y1 z1
...
```

