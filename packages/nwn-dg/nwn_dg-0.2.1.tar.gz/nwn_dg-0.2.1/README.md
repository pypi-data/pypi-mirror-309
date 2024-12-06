[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/cappysan/nwn-dg/badges/master/pipeline.svg?ignore_skipped=true)](https://gitlab.com/cappysan/nwn-dg/pipelines)
[![coverage](https://gitlab.com/cappysan/nwn-dg/badges/master/coverage.svg)](/coverage/index.html)

# nwn-dg

Work in progress: in alpha stage.

Neverwinter Nights (nwn) dungeon generator


## Installation

You can install the latest version from PyPI package repository.

~~~bash
pipx install nwn-dg
~~~


## Roadmap

- Entrance point, and optionally exit point, also depends on tileset
  - map-stairs-up 1 (U)
    - replace deadend
    - extend deadend
    - on any corridor
    - on any room border
  - map-stairs-down 1 (D)
    - replace deadend
    - extend deadend
    - on any room border
  - map-exits 0
    - on room border
    - requires 5x5 rooms
  - map-transitions
    (door transition)
    - replace deadend
    - extend deadend
    - on any corridor
    - on any room border
  - Load from tileset?

- Map layout (box, cross, dagger, ...)
  - Reserved cells

- Add tileset groups
- Doors (on separations and not on the cell)
- For are and are.json generation, take an input file to serve as base.
- An HTTP REST API frontend to be called via nwnxee requests.
- Allow 5x5 rooms, and 5x5 room reshaping.
- Room reshaping just to cut corners (and not entire rows)
- Allow any (binary) type file as seed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Locations

  * Website: [https://gitlab.com/cappysan/nwn-dg](https://gitlab.com/cappysan/nwn-dg)
  * PyPi: [https://pypi.org/project/nwn_dg](https://pypi.org/project/nwn_dg)
