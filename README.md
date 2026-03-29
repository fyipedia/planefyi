# planefyi

[![PyPI version](https://agentgif.com/badge/pypi/planefyi/version.svg)](https://pypi.org/project/planefyi/)
[![Python](https://img.shields.io/pypi/pyversions/planefyi)](https://pypi.org/project/planefyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://pypi.org/project/planefyi/)

Python API client for aircraft data. Look up aircraft models by ICAO type designator, compare performance specifications (range, speed, ceiling), explore manufacturer families (Airbus A320, Boeing 737), and query engine configurations — all from [PlaneFYI](https://planefyi.com/), an aircraft encyclopedia covering commercial, military, and general aviation aircraft.

PlaneFYI catalogs aircraft type designators, manufacturer lineages, performance envelopes (MTOW, range, cruise speed, service ceiling), seating configurations, engine types, and first flight dates — used by aviation enthusiasts, flight sim developers, and airline analytics platforms.

> **Explore aircraft at [planefyi.com](https://planefyi.com/)** — browse by [manufacturer](https://planefyi.com/manufacturers/), search by [type code](https://planefyi.com/aircraft/), and compare specifications.

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/planefyi/main/demo.gif" alt="planefyi demo — aircraft specifications, type codes, and manufacturer data in Python" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [Aircraft Families](#aircraft-families)
  - [Performance Specifications](#performance-specifications)
  - [Engine Configurations](#engine-configurations)
  - [ICAO Type Designators](#icao-type-designators)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
- [Learn More About Aircraft](#learn-more-about-aircraft)
- [Also Available](#also-available)
- [Transport FYI Family](#transport-fyi-family)
- [License](#license)

## Install

```bash
pip install planefyi                # Core (zero deps)
pip install "planefyi[cli]"         # + Command-line interface
pip install "planefyi[mcp]"         # + MCP server for AI assistants
pip install "planefyi[api]"         # + HTTP client for planefyi.com API
pip install "planefyi[all]"         # Everything
```

## Quick Start

```python
from planefyi.api import PlaneFYI

with PlaneFYI() as api:
    # Look up an aircraft model
    a350 = api.get_aircraft("airbus-a350-900")
    print(a350["icao_code"])        # A359
    print(a350["manufacturer"])     # Airbus
    print(a350["range_km"])         # 15,000 km
    print(a350["max_passengers"])   # 440

    # List aircraft by manufacturer
    airbus = api.list_aircraft(manufacturer="airbus")
    for a in airbus:
        print(f"{a['icao_code']} — {a['name']}")

    # Search aircraft
    results = api.search("787")
```

## What You Can Do

### Aircraft Families

Commercial aircraft are organized into families — groups of variants sharing a common fuselage design. The Airbus A320 family (A318/A319/A320/A321) and Boeing 737 family (737-700/800/900/MAX) are the world's most-produced narrowbody families, while the A350 and B787 represent the current generation of widebody aircraft.

| Family | Variants | Category | Typical Range |
|--------|----------|----------|--------------|
| Airbus A220 | A220-100, A220-300 | Narrowbody | 3,400-6,300 km |
| Airbus A320 | A318, A319, A320, A321 | Narrowbody | 3,100-7,400 km |
| Airbus A330 | A330-200, A330-300, A330-800/900neo | Widebody | 10,800-13,300 km |
| Airbus A350 | A350-900, A350-1000 | Widebody | 15,000-16,100 km |
| Boeing 737 | 737-700/800/900, MAX 7/8/9/10 | Narrowbody | 5,600-7,100 km |
| Boeing 777 | 777-200/300, 777X | Widebody | 9,700-16,090 km |
| Boeing 787 | 787-8, 787-9, 787-10 | Widebody | 11,700-14,100 km |
| Embraer E-Jet | E170, E175, E190, E195 | Regional | 2,200-4,500 km |

```python
from planefyi.api import PlaneFYI

with PlaneFYI() as api:
    # Browse aircraft by manufacturer
    boeing = api.list_aircraft(manufacturer="boeing")
    for aircraft in boeing:
        print(f"{aircraft['name']}: range {aircraft.get('range_km', 'N/A')} km")

    # Get all manufacturers
    manufacturers = api.list_manufacturers()
```

Learn more: [Aircraft Directory](https://planefyi.com/aircraft/) · [Glossary](https://planefyi.com/glossary/)

### Performance Specifications

Aircraft performance is defined by key metrics: Maximum Takeoff Weight (MTOW) determines payload capacity, range defines non-stop distance capability, cruise speed affects block time, and service ceiling sets the maximum operating altitude.

| Metric | Unit | Determines |
|--------|------|-----------|
| MTOW | kg/lbs | Max payload + fuel capacity |
| Range | km/nm | Non-stop distance capability |
| Cruise Speed | Mach/km/h | Block time, fuel efficiency |
| Service Ceiling | ft/m | Maximum flight altitude |
| Wingspan | m/ft | Gate compatibility (ICAO code) |
| Cabin Width | m/ft | Seat layout (single vs twin aisle) |

```python
from planefyi.api import PlaneFYI

with PlaneFYI() as api:
    # Compare two aircraft
    a350 = api.get_aircraft("airbus-a350-900")
    b787 = api.get_aircraft("boeing-787-9")
    print(f"A350: {a350.get('range_km')} km range, Mach {a350.get('cruise_mach')}")
    print(f"B787: {b787.get('range_km')} km range, Mach {b787.get('cruise_mach')}")
```

Learn more: [Aircraft Specifications](https://planefyi.com/aircraft/) · [Guides](https://planefyi.com/guides/)

### Engine Configurations

Aircraft engines are categorized by type (turbofan, turboprop, piston) and mounting (underwing, rear-fuselage, integrated). Modern turbofans are identified by bypass ratio — high-bypass engines (5:1+) power commercial jets for fuel efficiency, while low-bypass engines power military fighters for raw thrust.

| Engine Type | Application | Examples |
|-------------|------------|---------|
| High-bypass turbofan | Commercial jets | CFM LEAP, PW GTF, GE9X |
| Low-bypass turbofan | Military fighters | F110, EJ200 |
| Turboprop | Regional/cargo | PW150A, CT7 |
| Turboshaft | Helicopters | T700, Arrius |

```python
from planefyi.api import PlaneFYI

with PlaneFYI() as api:
    aircraft = api.get_aircraft("boeing-777-300er")
    print(f"Engines: {aircraft.get('engine_type')}")
    print(f"Engine count: {aircraft.get('engine_count')}")
```

Learn more: [Aircraft Data](https://planefyi.com/aircraft/) · [Glossary](https://planefyi.com/glossary/)

### ICAO Type Designators

Every aircraft type is assigned an ICAO type designator — a 2-4 character code used in flight plans. The code encodes manufacturer and variant: A320 (Airbus A320), B738 (Boeing 737-800), E195 (Embraer 195). The ICAO wake turbulence category (L/M/H/J) determines required separation distances.

| Wake Category | MTOW | Example Types |
|---------------|------|---------------|
| L (Light) | <7,000 kg | C172, PA28 |
| M (Medium) | 7,000-136,000 kg | A320, B738, E195 |
| H (Heavy) | >136,000 kg | B777, A350, B747 |
| J (Super) | A380 only | A388 |

```python
from planefyi.api import PlaneFYI

with PlaneFYI() as api:
    # Search by ICAO type designator
    results = api.search("A359")
    aircraft = results[0]
    print(f"{aircraft['icao_code']} — {aircraft['name']}")
    print(f"Wake category: {aircraft.get('wake_category')}")
```

Learn more: [Type Designators](https://planefyi.com/aircraft/) · [API Documentation](https://planefyi.com/developers/)

## Command-Line Interface

```bash
pip install "planefyi[cli]"

planefyi aircraft airbus-a350-900          # Aircraft details
planefyi search "737 MAX"                  # Search aircraft
planefyi manufacturer boeing               # All Boeing aircraft
planefyi manufacturers                     # List all manufacturers
```

## MCP Server (Claude, Cursor, Windsurf)

```bash
pip install "planefyi[mcp]"
```

```json
{
    "mcpServers": {
        "planefyi": {
            "command": "uvx",
            "args": ["--from", "planefyi[mcp]", "python", "-m", "planefyi.mcp_server"]
        }
    }
}
```

## REST API Client

```python
from planefyi.api import PlaneFYI

with PlaneFYI() as api:
    aircraft = api.get_aircraft("airbus-a350-900")      # GET /api/v1/aircraft/airbus-a350-900/
    boeing = api.list_aircraft(manufacturer="boeing")     # GET /api/v1/aircraft/?manufacturer=boeing
    manufacturers = api.list_manufacturers()              # GET /api/v1/manufacturers/
    results = api.search("787")                          # GET /api/v1/search/?q=787
```

### Example

```bash
curl -s "https://planefyi.com/api/v1/aircraft/airbus-a350-900/"
```

```json
{
    "slug": "airbus-a350-900",
    "name": "Airbus A350-900",
    "icao_code": "A359",
    "manufacturer": "Airbus",
    "category": "Widebody",
    "range_km": 15000
}
```

Full API documentation at [planefyi.com/developers/](https://planefyi.com/developers/).

## API Reference

| Function | Description |
|----------|-------------|
| `api.get_aircraft(slug)` | Aircraft details (specs, engine, dimensions) |
| `api.list_aircraft(manufacturer)` | List aircraft, optionally by manufacturer |
| `api.list_manufacturers()` | All aircraft manufacturers |
| `api.get_manufacturer(slug)` | Manufacturer details with aircraft list |
| `api.search(query)` | Search by name, ICAO code, or manufacturer |

## Learn More About Aircraft

- **Browse**: [Aircraft Directory](https://planefyi.com/aircraft/) · [Manufacturers](https://planefyi.com/manufacturers/)
- **Guides**: [Aviation Guides](https://planefyi.com/guides/) · [Glossary](https://planefyi.com/glossary/)
- **API**: [REST API Docs](https://planefyi.com/developers/) · [OpenAPI Spec](https://planefyi.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install planefyi` | [npm](https://www.npmjs.com/package/planefyi) |
| **MCP** | `uvx --from "planefyi[mcp]" python -m planefyi.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |

## Transport FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem — airports, airlines, aircraft, and railways.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| airportfyi | [PyPI](https://pypi.org/project/airportfyi/) | [npm](https://www.npmjs.com/package/airportfyi) | 4,500+ airports, IATA/ICAO codes, routes — [airportfyi.com](https://airportfyi.com/) |
| airlinefyi | [PyPI](https://pypi.org/project/airlinefyi/) | [npm](https://www.npmjs.com/package/airlinefyi) | Airlines, fleets, alliances, routes — [airlinefyi.com](https://airlinefyi.com/) |
| **planefyi** | [PyPI](https://pypi.org/project/planefyi/) | [npm](https://www.npmjs.com/package/planefyi) | **Aircraft models, specifications, manufacturers — [planefyi.com](https://planefyi.com/)** |
| trainfyi | [PyPI](https://pypi.org/project/trainfyi/) | [npm](https://www.npmjs.com/package/trainfyi) | Railway stations, train routes, rail networks — [trainfyi.com](https://trainfyi.com/) |

## Embed Widget

Embed [PlaneFYI](https://planefyi.com) widgets on any website with [planefyi-embed](https://widget.planefyi.com):

```html
<script src="https://cdn.jsdelivr.net/npm/planefyi-embed@1/dist/embed.min.js"></script>
<div data-planefyi="entity" data-slug="example"></div>
```

Zero dependencies · Shadow DOM · 4 themes (light/dark/sepia/auto) · [Widget docs](https://widget.planefyi.com)

## License

MIT
