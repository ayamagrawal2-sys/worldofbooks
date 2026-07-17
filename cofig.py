"""
config.py
---------
Central configuration for the Library Management System.

Holds filesystem paths, business-rule constants (loan periods, fine rates,
membership tiers) and display settings used across every other module.
Keeping these values in one place means a librarian can retune the whole
system (e.g. change the fine rate) by editing a single file.
"""

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Filesystem layout
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"

for _directory in (DATA_DIR, REPORTS_DIR, LOG_DIR):
    _directory.mkdir(parents=True, exist_ok=True)

BOOKS_CSV = DATA_DIR / "books.csv"
MEMBERS_CSV = DATA_DIR / "members.csv"
TRANSACTIONS_CSV = DATA_DIR / "transactions.csv"
LOG_FILE = LOG_DIR / "library_system.log"

# --------------------------------------------------------------------------
# Business rules
# --------------------------------------------------------------------------
LOAN_PERIOD_DAYS = 14          # standard borrowing window
MAX_RENEWALS = 2               # times a single loan can be extended
RENEWAL_EXTENSION_DAYS = 7

FINE_PER_DAY = 5.0             # currency units per day overdue
FINE_GRACE_PERIOD_DAYS = 1     # no fine accrues for the first day late
MAX_FINE_CAP = 500.0           # fines never exceed this per transaction

# A member cannot borrow more books than their tier allows
MEMBERSHIP_TIERS = {
    "STUDENT": {"max_books": 3, "loan_days": 14},
    "FACULTY": {"max_books": 8, "loan_days": 30},
    "GENERAL": {"max_books": 5, "loan_days": 21},
}

DEFAULT_TIER = "STUDENT"

# Members with unpaid fines above this threshold cannot borrow more books
FINE_BLOCK_THRESHOLD = 50.0

# --------------------------------------------------------------------------
# Catalogue
# --------------------------------------------------------------------------
VALID_GENRES = [
    "Fiction", "Non-Fiction", "Science", "Mathematics", "History",
    "Biography", "Fantasy", "Technology", "Philosophy", "Poetry",
    "Reference", "Children",
]

BOOK_ID_PREFIX = "BK"
MEMBER_ID_PREFIX = "MB"
TXN_ID_PREFIX = "TX"

# --------------------------------------------------------------------------
# Display / formatting
# --------------------------------------------------------------------------
DATE_FORMAT = "%Y-%m-%d"
CURRENCY_SYMBOL = "₹"
TABLE_WIDTH = 100

CHART_STYLE = "seaborn-v0_8-darkgrid"
CHART_DPI = 150
CHART_FIGSIZE = (10, 6)
CHART_COLOR_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B",
    "#6A994E", "#BC4749", "#386641", "#F2E8CF", "#457B9D",
]

APP_NAME = "PyLibrary — Library Management System"
APP_VERSION = "2.1.0"
