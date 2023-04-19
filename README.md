# Space Invaders Surveillance

This is a fun project that allows you to search for invaders on a map.

## Installation

To run the project you need Python 3.11 and `poetry` installed on your system.

Run `poetry install` to install all its dependencies.

## Architecture and Design principles

The current library is implemented with the SOLID design principles in mind.

There are the following entities that each play its own role in searching for invaders:

### Invader

An `Invader` instance is a reference pattern to match against when searching for invaders
on the Map. There can be different types of Invaders. Currently, there is an
`AsciiInvader` that is represented by an ASCII set of dashes (`-`) and circles (`o`).

For instance, this is an example of an invader:

```text
~~~~
---oo---
--oooo--
-oooooo-
oo-oo-oo
oooooooo
--o--o--
-o-oo-o-
o-o--o-o
~~~~
```

Other invaders can be defined by inheriting from the `invaders.base.Invader` abstract class and defining two things:

1. Transform the invader input pattern into a binary matrix that is used under the hood
by the Invader class
2. Implement the `pretty_representation` method to transform the binary matrix into a more
readable pattern.

### Map

A `Map` instance is a matrix where invaders are being searched.

Currently, there are two types of maps: `AsciiMap` and `AsciiSphericalMap`. The latter
one treats the rectangular shape as the surface of a sphere that was flattened out.

To add a new type of map, you need to inherit from the `maps.base.Map` abstract class
and implement `print_frame_at` and `get_frame_at` abstract methods.

### Scanner

A `Scanner` is responsible for identifying a specific `Invader` instance on a portion
(frame) on the `Map`.

Currently, there is only one type of scanner, the `BasicScanner`. To add other types of
scanners, you should inherit from `scanners.base.Scanner` and provide an implementation
for `process_frame` and `is_worth_processing_frame` methods.

### Radar

A `Radar` is responsible for using a `Scanner` that knows how to identify an
`Invader` to search for it on a `Map`.

There are two types of radars currently: a `DPAreaRadar` and `DPSphericalRadar`.
DP stands for DynamicProgramming, as it is used for improving the performance of searching
for invaders.

To use a radar, you must provide a `Scanner` and a `Map` instance to it. The search is
performed by running the `.scan()` method. Once it is done, you can obtain a list of
`IdentifiedInvader`s by running `.get_identified_invaders()` method.

### IdentifiedInvader

Finally, an `IdentifiedInvader` is a subtype of `Invader` that has a reference to the
original invader, the similarity ratio to the original invader, as well as the coordinates
where it can be found on the map.

## Example usage

Below you can find an example of how it works in code. Check out `main.py` for more examples.

```python
    # setting things up
    invader_ascii_pattern = # ascii pattern here
    invader = AsciiInvader(invader_ascii_pattern)
    
    map_ascii_pattern = # ascii pattern here
    ascii_map = AsciiMap(map_ascii_pattern)
    
    scanner = BasicScanner(invader)
    radar = DPAreaRadar(ascii_map, scanner)
    
    # run the logic
    radar.scan()
    
    # view results
    identified_invaders = radar.get_identified_invaders()
    for identified_invader in identified_invaders:
        print(identified_invader.pretty_representation())
```
An example of `print(identified_invader.pretty_representation())` would look like:
```python
    Similarity ratio: 0.859375
    Coords on map: [[82, 41], [89, 48]]
    Visual representation:
    ---oo---
    --ooooo-
    -oo-ooo-
    oo-o-ooo
    o-oooooo
    --o--o--
    oo-oo-o-
    --oooo-o
```

## Adherence to SOLID design principles

The following SOLID design principles were followed:

#### Single Responsibility Principle

Each type of class (Radar, Scanner, etc) is responsible only for its subset of
responsibilities, not trying to do things they are not responsible for.

#### Open/Closed Principle

For instance, there are `AsciiInvader` and `AsciiMap`. If a new type of invader, map,
scanner, or radar is required, it can be easily added by inheriting from their
corresponding abstract classes.

#### Liskov Substitution Principle

Derived classes can replace objects of the base class without affecting the logic. For
instance, `AsciiSphericalMap` is a derived class of `AsciiMap`, and it is used in the
`main.py` example without breaking the flow.

#### Interface Segregation Principle

There is a `PrettyRepresentationABC` specific class that is inherited only by relevant
classes.

#### Dependency Inversion Principle

The `Radar` class relies on abstract `Scanner`, `Map` input types, rather than on
specific implementations:

```python
class Radar(ABC):
    def __init__(self, map_: Map, scanner: Scanner):
        self.map = map_
        self.scanner = scanner
```
Similarly, the `Scanner` class also relies on abstract `Invader` type.

## Development dependencies

The project uses `pytest` framework for running tests and `black` and `flake8` for
keeping the code well formatted.

The `flake8 --extend-ignore=E501 .` is used to ignore long lines (this would be
discussed with the team to agree on a convention around line length)

To run tests with coverage, use `pytest --cov=. tests/` from project root.

Current test coverage (with `main.py` code commeented out):
```text
---------- coverage: platform darwin, python 3.11.3-final-0 ----------
Name                         Stmts   Miss  Cover
------------------------------------------------
core/__init__.py                 0      0   100%
core/exceptions.py              14      0   100%
core/mixins.py                  38      0   100%
core/types.py                    2      0   100%
core/utils.py                   14      0   100%
invaders/__init__.py             0      0   100%
invaders/ascii.py               24      0   100%
invaders/base.py                53      5    91%
invaders/identified.py           7      0   100%
main.py                          7      7     0%
maps/__init__.py                 0      0   100%
maps/ascii.py                   38      3    92%
maps/base.py                    22      3    86%
radars/__init__.py               0      0   100%
radars/area.py                  50      1    98%
radars/base.py                  22      2    91%
radars/spherical.py             49      1    98%
scanners/__init__.py             0      0   100%
scanners/base.py                16      2    88%
scanners/basic.py               16      0   100%
tests/__init__.py                0      0   100%
tests/test_frame_coords.py       9      0   100%
tests/test_invaders.py          32      0   100%
tests/test_maps.py              31      0   100%
tests/test_mixins.py            23      0   100%
tests/test_radars.py           117      0   100%
tests/test_scanners.py          41      0   100%
------------------------------------------------
TOTAL                          625     24    96%
```