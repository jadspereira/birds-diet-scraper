# Birds of the World Diet Scraper 🪶

Python tool to extract bird diet data from [Birds of the World](https://birdsoftheworld.org).

## Features

- Collects species IDs from Cornell Lab's database (hardcoded limit in `sp_list_cornell.py`)
- Scrapes diet information for hardcoded keywords: `ant`, `ants`, `hymenoptera`
- Exports structured CSV data
- Simulates human browsing patterns to avoid blocks

## Installation

```bash
git clone https://github.com/jadspereira/birds-diet-scraper.git
cd birds-diet-scraper
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Usage

1. Collect species codes (edit `limit` in `sp_list_cornell.py` if needed):

```bash
python src/sp_list_cornell.py
```

2. Search for dietary habits (uses hardcoded keywords):

```bash
python src/login_search.py
```

## Customization

- To change species limit:Edit `limit = 100` in `sp_list_cornell.py`
- To change keywords:
  Edit `keywords = [r'\bant\b', r'\bhymenoptera\b', r'\bants\b']` in `login_search.py`

## Project Structure

```
src/
  sp_list_cornell.py    # Collects species IDs (hardcoded limit)
  login_search.py       # Checks diet pages (hardcoded keywords)
  speciescodes.csv     # Generated IDs
  end_diet.txt         # URL template
outputs/               # Generated reports
```

## License

MIT License
