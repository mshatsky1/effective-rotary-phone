# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial project structure with basic CLI framework
- Phone number dialing simulation
- Phone number validation and formatting utilities
- Contact management (add, delete, list, search)
- Call history tracking with timestamps
- Statistics and analytics feature
- Export/import functionality for contacts and history
- Configuration file support
- Dial by contact name
- Comprehensive test suite
- Logging support
- GitHub Actions CI workflow
- MIT License
- Setup.py for package distribution
- Examples and documentation

### Features
- Multiple phone number format support
- Configurable dialing delay
- History limit management
- Search functionality for contacts
- Top dialed numbers statistics
- Configuration management commands
- Export/import with merge/replace options

## [0.2.0] - 2024-01-XX

### Added
- Version 0.2.0 release
- normalize_number utility function
- update_contact function for modifying existing contacts
- get_average_calls_per_day statistics function
- Export version metadata in exported data
- Enhanced number validation with minimum length check
- Configurable history limit support
- Improved error handling and exception types
- Better logging with formatted connection messages

### Changed
- Bumped version to 0.2.0
- Improved contact management with return values
- Enhanced dialer to use normalize_number utility
- Updated CLI to handle existing contacts better
- Improved documentation and docstrings
- Enhanced logging format with millisecond precision
- Refactored validate_number to use utility functions
- Improved history sorting by timestamp
- Added visual feedback during dialing

## [Unreleased]

### Added
- get_calls_by_day function for daily statistics
- is_valid_length utility function
- Export date timestamps
- Configurable min/max number length
- Enhanced stats command with average calls per day
- Sorted JSON output for contacts and exports
- Improved error documentation

### Planned
- Interactive mode
- Contact groups/tags
- Backup scheduling
- More advanced statistics





