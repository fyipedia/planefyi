# planefyi

Aircraft models and specifications API client — [planefyi.com](https://planefyi.com)

## Install

```bash
pip install planefyi
```

## Quick Start

```python
from planefyi.api import PlaneFYI

with PlaneFYI() as api:
    results = api.search("747")
    print(results)
```

## License

MIT
