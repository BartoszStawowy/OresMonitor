import re


def match_engine(mint, ore):
    if mint == 'dragon_mint':
        return re.match(r'^(.*?)\s+(\d{4})?\s*-\s*([\d,]+)zł$', ore)
    if mint == 'silver_mint':
        patterns = [
            re.compile(r'^(.*?) (\d{4}),.*? - (\d+,\d+\.\d{2})\xa0zł$'),  # Pattern with a comma in the year
            re.compile(r'^(.*?) (\d{4}),.*? - (\d+\.\d{2})\xa0zł$'),  # Pattern without a comma in the year
        ]
        for pattern in patterns:
            return pattern.match(ore)
