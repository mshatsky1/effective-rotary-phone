#!/bin/bash
# Advanced usage examples for rotary phone CLI

# Add multiple contacts
python main.py add "Alice" "555-0100"
python main.py add "Bob" "555-0200"
python main.py add "Charlie" "555-0300"

# Search contacts
python main.py contacts --search "Alice"

# View statistics
python main.py stats
python main.py stats --top 10

# Export data
python main.py export backup.json
python main.py export backup_no_history.json --no-history

# Import data
python main.py import backup.json
python main.py import backup.json --replace

# Configuration management
python main.py config show
python main.py config set default_delay 0.2
python main.py config set history_limit 200

# View call history with custom limit
python main.py history --limit 20

# Dial by contact name
python main.py dial "Alice" --contact






