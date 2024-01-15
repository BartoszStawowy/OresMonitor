import re

def match_engine(mint, ore):
    # Every mint has different way to show names and prices. Matcher solve it #

    if mint == 'dragon_mint':
        return re.match(r'^(.*?)\s+(\d{4})?\s*-\s*([\d,]+)zł$', ore)
    if mint == 'silver_mint':
        patterns = [
            re.compile(r'^(.*?) (\d{4}),[^-]+- ([^ zł]+) zł$'),
            re.compile(r'^(.*?) (\d{4}),[^-]+- ([^,]+),00 zł$'),
        ]
        for pattern in patterns:
            return pattern.match(ore)

