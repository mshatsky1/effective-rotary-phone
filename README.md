# Effective Rotary Phone

A simple CLI tool for rotary phone number dialing simulation.

## Installation

```bash
pip install -r requirements.txt
```

Or install as a package:

```bash
pip install -e .
```

## Usage

### Basic Dialing

```bash
python main.py dial 555-1234
python main.py dial "(555) 123-4567" --delay 0.2
```

### Contact Management

```bash
# Add a contact
python main.py add "John Doe" "555-1234"

# List all contacts
python main.py contacts

# Dial using a contact
python main.py dial "John Doe" --contact

# Delete a contact
python main.py delete "John Doe"
```

### Call History

```bash
# View call history
python main.py history
python main.py history --limit 20

# Clear call history
python main.py clear
```

## Features

- Phone number validation
- Multiple number formats supported
- Configurable dialing delay
- Contact management (add, delete, list)
- Call history tracking
- Dial by contact name
- Logging support
- Comprehensive error handling

## Testing

```bash
pytest
```

## License

MIT License - see LICENSE file for details.

