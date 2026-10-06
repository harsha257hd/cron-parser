import unittest

from cron_parser import expand_field, parse_cron, format_output


class TestCronParser(unittest.TestCase):

    def test_wildcard(self):
        result = expand_field("*", 0, 5)
        self.assertEqual(result, [0, 1, 2, 3, 4, 5])

    def test_step(self):
        result = expand_field("*/15", 0, 59)
        self.assertEqual(result, [0, 15, 30, 45])

    def test_single_value(self):
        result = expand_field("5", 0, 59)
        self.assertEqual(result, [5])

    def test_list(self):
        result = expand_field("1,15,30", 0, 59)
        self.assertEqual(result, [1, 15, 30])

    def test_range(self):
        result = expand_field("1-5", 0, 59)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_range_with_step(self):
        result = expand_field("0-10/2", 0, 59)
        self.assertEqual(result, [0, 2, 4, 6, 8, 10])

    def test_combination(self):
        result = expand_field("1,5-7,10", 0, 59)
        self.assertEqual(result, [1, 5, 6, 7, 10])

    def test_sample_expression(self):
        expression = "*/15 0 1,15 * 1-5 /usr/bin/find"

        result = parse_cron(expression)

        self.assertEqual(result["minute"], [0, 15, 30, 45])
        self.assertEqual(result["hour"], [0])
        self.assertEqual(result["day of month"], [1, 15])
        self.assertEqual(
            result["month"],
            list(range(1, 13))
        )
        self.assertEqual(
            result["day of week"],
            [1, 2, 3, 4, 5]
        )
        self.assertEqual(result["command"], "/usr/bin/find")

    def test_command_with_spaces(self):
        expression = "0 0 * * * /usr/bin/find /tmp -type f"

        result = parse_cron(expression)

        self.assertEqual(
            result["command"],
            "/usr/bin/find /tmp -type f"
        )

    def test_invalid_field_count(self):
        with self.assertRaises(ValueError):
            parse_cron("* * *")

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            expand_field("60", 0, 59)

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            expand_field("10-5", 0, 59)

    def test_invalid_step(self):
        with self.assertRaises(ValueError):
            expand_field("*/0", 0, 59)


if __name__ == "__main__":
    unittest.main()