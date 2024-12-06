# SP Ask School

A Python package for managing school information and queues for Scholars Portal Ask service. This package provides utilities to manage and query information about various Ontario universities and their associated chat queues.

## Installation

You can install the package via pip:

```bash
pip install sp-ask-school
```

## Usage

```python
from sp_ask_school import (
    find_school_by_operator_suffix,
    find_queues_from_a_school_name,
    find_school_by_queue_or_profile_name
)

# Find school from operator suffix
school = find_school_by_operator_suffix("operator_tor")
print(school)  # Output: "toronto"

# Get queues for a school
queues = find_queues_from_a_school_name("Toronto")
print(queues)  # Output: ["toronto", "toronto-mississauga", ...]

# Find school from queue name
school = find_school_by_queue_or_profile_name("western-proactive")
print(school)  # Output: "Western"
```

## Features

- Find school information by operator suffix
- Get queue lists for specific schools
- Find school information by queue name
- Support for French and SMS queues
- Practice queue management
- Support for multiple university profiles

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Guinsly Mondésir

## Maintained by

[Scholars Portal](https://scholarsportal.info/)