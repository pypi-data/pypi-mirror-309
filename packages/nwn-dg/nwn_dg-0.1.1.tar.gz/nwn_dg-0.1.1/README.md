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

- Entrance point, and optionally exit point.
- Room tree graph.
- Map layout (box, cross, dagger, ...)
- Doors.
- For are and are.json generation, take an input file to serve as base.
- An HTTP REST API frontend to be called via nwnxee requests.
- Allow 5x5 rooms, and 5x5 room reshaping.
- Room reshaping just to cut corners.
- Max / Min / Ratio rooms compared to map size.
- Allow any (binary) type file as seed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Locations

  * Website: [https://gitlab.com/cappysan/nwn-dg](https://gitlab.com/cappysan/nwn-dg)
  * PyPi: [https://pypi.org/project/nwn_dg](https://pypi.org/project/nwn_dg)
