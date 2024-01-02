import re


def match_engine(mint, ore):
    if mint == 'dragon_mint':
        return re.match(r'^(.*?)\s+(\d{4})?\s*-\s*([\d,]+)zł$', ore)
    if mint == 'silver_mint':
        patterns = [
            re.compile(r'^(.*?) (\d{4}),.*? - (\d+,\d+\.\d{2})\xa0zł$'),
            re.compile(r'^(.*?) (\d{4}),.*? - (\d+\.\d{2})\xa0zł$'),
        ]
        for pattern in patterns:
            return pattern.match(ore)
