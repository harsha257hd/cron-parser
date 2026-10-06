#!/usr/bin/env python3

import sys


FIELD_RANGES = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day of month": (1, 31),
    "month": (1, 12),
    "day of week": (0, 6),
}


def expand_field(field, minimum, maximum):
    """
    Expand a single cron field.

    Supported formats:
        *
        */n
        n
        n,m
        n-m
        n-m/s
        n,m,p
        combinations of the above
    """

    values = set()

    for part in field.split(","):
        part = part.strip()

        if not part:
            raise ValueError("Invalid empty field")

        # Handle step syntax
        if "/" in part:
            if part.count("/") != 1:
                raise ValueError(f"Invalid step expression: {part}")

            base, step_text = part.split("/")

            try:
                step = int(step_text)
            except ValueError:
                raise ValueError(f"Invalid step value: {step_text}")

            if step <= 0:
                raise ValueError("Step must be greater than zero")

        else:
            base = part
            step = 1

        # Determine the range
        if base == "*":
            start = minimum
            end = maximum

        elif "-" in base:
            if base.count("-") != 1:
                raise ValueError(f"Invalid range: {base}")

            start_text, end_text = base.split("-")

            try:
                start = int(start_text)
                end = int(end_text)
            except ValueError:
                raise ValueError(f"Invalid range: {base}")

            if start > end:
                raise ValueError(f"Range start is greater than end: {base}")

        else:
            try:
                start = int(base)
                end = start
            except ValueError:
                raise ValueError(f"Invalid value: {base}")

        # Validate range
        if start < minimum or end > maximum:
            raise ValueError(
                f"Value {start}-{end} outside allowed range "
                f"{minimum}-{maximum}"
            )

        # Add expanded values
        values.update(range(start, end + 1, step))

    return sorted(values)


def parse_cron(cron_expression):
    """
    Parse a complete cron expression.

    Expected format:
        minute hour day-of-month month day-of-week command
    """

    parts = cron_expression.split(maxsplit=5)

    if len(parts) != 6:
        raise ValueError(
            "Cron expression must contain five time fields followed by a command"
        )

    minute, hour, day_of_month, month, day_of_week, command = parts

    expanded = {
        "minute": expand_field(
            minute,
            *FIELD_RANGES["minute"]
        ),
        "hour": expand_field(
            hour,
            *FIELD_RANGES["hour"]
        ),
        "day of month": expand_field(
            day_of_month,
            *FIELD_RANGES["day of month"]
        ),
        "month": expand_field(
            month,
            *FIELD_RANGES["month"]
        ),
        "day of week": expand_field(
            day_of_week,
            *FIELD_RANGES["day of week"]
        ),
        "command": command,
    }

    return expanded


def format_output(result):
    """
    Format output so that field names occupy 14 columns.
    """

    lines = []

    for field, values in result.items():
        if field == "command":
            value = values
        else:
            value = " ".join(str(v) for v in values)

        lines.append(f"{field:<14}{value}")

    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print(
            'Usage: python3 cron_parser.py '
            '"*/15 0 1,15 * 1-5 /usr/bin/find"',
            file=sys.stderr,
        )
        sys.exit(1)

    cron_expression = sys.argv[1]

    try:
        result = parse_cron(cron_expression)
        print(format_output(result))

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()