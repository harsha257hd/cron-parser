# Cron Expression Parser

A command-line application written in Python that parses a standard
five-field cron expression and expands each time field.

## Supported Format

    minute hour day-of-month month day-of-week command

Example:

    */15 0 1,15 * 1-5 /usr/bin/find

## Supported Expressions

The parser supports:

- Wildcards: `*`
- Lists: `1,15,30`
- Ranges: `1-5`
- Steps: `*/15`
- Ranges with steps: `1-10/2`
- Combinations: `1,5-10,20`
- Commands containing spaces

## Field Ranges

| Field | Range |
|---|---|
| Minute | 0-59 |
| Hour | 0-23 |
| Day of month | 1-31 |
| Month | 1-12 |
| Day of week | 0-6 |

## Requirements

Python 3.8 or newer.

No external packages are required.

## Running

```bash
python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```