from urllib.parse import urlparse

DOMAIN_COUNTRY_MAP = {
    # United Kingdom
    ".ac.uk": "United Kingdom",

    # Germany
    ".de": "Germany",

    # Netherlands
    ".nl": "Netherlands",

    # Sweden
    ".se": "Sweden",

    # Finland
    ".fi": "Finland",

    # Norway
    ".no": "Norway",

    # Denmark
    ".dk": "Denmark",

    # France
    ".fr": "France",

    # Italy
    ".it": "Italy",

    # Spain
    ".es": "Spain",

    # Switzerland
    ".ch": "Switzerland",

    # Ireland
    ".ie": "Ireland",

    # Belgium
    ".be": "Belgium",

    # Austria
    ".at": "Austria",

    # Poland
    ".pl": "Poland",

    # Portugal
    ".pt": "Portugal",

    # Czech Republic
    ".cz": "Czech Republic",

    # Hungary
    ".hu": "Hungary",

    # Greece
    ".gr": "Greece",

    # Romania
    ".ro": "Romania",

    # Slovakia
    ".sk": "Slovakia",

    # Slovenia
    ".si": "Slovenia",

    # Croatia
    ".hr": "Croatia",

    # Estonia
    ".ee": "Estonia",

    # Latvia
    ".lv": "Latvia",

    # Lithuania
    ".lt": "Lithuania",


    # -------------------------
    # NORTH AMERICA
    # -------------------------

    ".edu": "United States",
    ".ca": "Canada",
    ".edu.mx": "Mexico",

    # Canadian academic
    ".ac.ca": "Canada",


    # -------------------------
    # AUSTRALIA / OCEANIA
    # -------------------------

    ".edu.au": "Australia",
    ".ac.nz": "New Zealand",
    ".nz": "New Zealand",

    # -------------------------
    # MIDDLE EAST
    # -------------------------

    ".ac.ae": "United Arab Emirates",
    ".ae": "United Arab Emirates",

    ".edu.sa": "Saudi Arabia",
    ".sa": "Saudi Arabia",

    ".ac.il": "Israel",
    ".il": "Israel",

    ".qa": "Qatar",
    ".edu.qa": "Qatar",

    ".om": "Oman",
    ".edu.om": "Oman",

    ".edu.kw": "Kuwait",
    ".kw": "Kuwait",

    ".edu.jo": "Jordan",
    ".jo": "Jordan",

    ".edu.lb": "Lebanon",
    ".lb": "Lebanon",


    # -------------------------
    # ASIA
    # -------------------------

    ".ac.in": "India",
    ".in": "India",

    ".ac.jp": "Japan",
    ".jp": "Japan",

    ".ac.kr": "South Korea",
    ".kr": "South Korea",

    ".edu.sg": "Singapore",
    ".sg": "Singapore",

    ".edu.cn": "China",
    ".cn": "China",

    ".edu.hk": "Hong Kong",
    ".hk": "Hong Kong",

    ".edu.tw": "Taiwan",
    ".tw": "Taiwan",

    ".edu.my": "Malaysia",
    ".my": "Malaysia",

    ".ac.th": "Thailand",
    ".th": "Thailand",

    ".ac.id": "Indonesia",
    ".id": "Indonesia",


    # -------------------------
    # SOUTH AMERICA
    # -------------------------

    ".edu.br": "Brazil",
    ".br": "Brazil",

    ".edu.ar": "Argentina",
    ".ar": "Argentina",

    ".edu.cl": "Chile",
    ".cl": "Chile",

    ".edu.pe": "Peru",
    ".pe": "Peru",

    ".edu.co": "Colombia",
    ".co": "Colombia",


    # -------------------------
    # AFRICA
    # -------------------------

    ".ac.za": "South Africa",
    ".za": "South Africa",

    ".edu.ng": "Nigeria",
    ".ng": "Nigeria",

    ".edu.eg": "Egypt",
    ".eg": "Egypt",

    ".edu.gh": "Ghana",
    ".gh": "Ghana",

    ".edu.ke": "Kenya",
    ".ke": "Kenya"
}


def detect_country(url, text=""):

    domain = urlparse(url).netloc.lower()

    #  Domain detection
    for ext, country in DOMAIN_COUNTRY_MAP.items():
        if ext in domain:
            return country

    # Text detection
    country_keywords = [
        "united kingdom",
        "germany",
        "france",
        "netherlands",
        "sweden",
        "italy",
        "spain",
        "finland"
    ]

    text_lower = text.lower()

    for c in country_keywords:
        if c in text_lower:
            return c.title()

    return "Not found"