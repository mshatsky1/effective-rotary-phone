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

### Statistics

```bash
# View statistics
python main.py stats
python main.py stats --top 10
```

### Export/Import

```bash
# Export data to JSON file
python main.py export backup.json
python main.py export backup_no_history.json --no-history

# Import data from JSON file
python main.py import backup.json
python main.py import backup.json --replace
```

### Configuration

```bash
# Show configuration
python main.py config show

# Set configuration values
python main.py config set default_delay 0.2
python main.py config set history_limit 200
```

### Search

```bash
# Search contacts by name
python main.py contacts --search "John"
```

### Advanced Features

```bash
# Dial in quiet mode (suppress output)
python main.py dial 555-1234 --quiet

# Show daily call statistics
python main.py stats --daily

# Show calls from last 7 days
python main.py history --days 7

# Add contact with force overwrite
python main.py add "John Doe" "555-1234" --force

# Reset configuration value
python main.py config unset default_delay
```

## Features

- Phone number validation with length checking
- Multiple number formats supported (7 and 10 digit)
- Configurable dialing delay (with config file support)
- Contact management (add, delete, list, search, update)
- Call history tracking with configurable limits
- Dial by contact name
- Statistics and analytics (including average calls per day and daily call counts)
- Export/import functionality with version metadata and timestamps
- Configuration file management
- Enhanced logging with millisecond precision
- Comprehensive error handling
- Normalized phone number processing
- Visual feedback during dialing
- Configurable number length validation

## Testing

```bash
pytest
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


<!-- Update 1 -->

<!-- Update 2 -->

<!-- Update 3 -->

<!-- Update 4 -->

<!-- Update 5 -->

<!-- Update 6 -->

<!-- Update 7 -->
