"""
Land of Books - Modern Library Management System
-----------------------------------------------------------------
Run with:
    streamlit run streamlit_app.py
"""

from datetime import date, datetime, timedelta
import pandas as pd
import streamlit as st
import config
import exceptions as exc
from core.library_manager import LibraryManager
from database.db_manager import DatabaseManager
from analytics.statistics import LibraryStatistics
from analytics.visualizer import LibraryVisualizer
import html
import time

# ══════════════════════════════════════════════════════════════════════
#  CONFIGURATION & INITIALIZATION
# ══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Land of Books",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Multi-language Support ───────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "app_name": "Land of Books",
        "nav": "Navigation",
        "overview": "Overview",
        "catalogue": "Catalogue",
        "members": "Members",
        "circulation": "Circulation",
        "fines": "Fines",
        "analytics": "Analytics",
        "settings": "Settings",
        "theme": "Theme",
        "language": "Language",
        "light": "Light",
        "dark": "Dark",
        "titles": "Titles",
        "copies": "Copies",
        "on_loan": "On Loan",
        "members_count": "Members",
        "overdue": "Overdue",
        "fines_due": "Fines Due",
        "overdue_loans": "Overdue Loans",
        "genre_distribution": "Genre Distribution",
        "nothing_here": "Nothing here yet",
        "search": "Search",
        "genre": "Genre",
        "all": "All",
        "no_books_found": "No books found",
        "add_book": "Add Book",
        "title": "Title",
        "author": "Author",
        "year": "Year",
        "isbn": "ISBN",
        "copies_count": "Copies",
        "price": "Price",
        "rating": "Rating",
        "add": "Add",
        "successfully_added": "Successfully Added",
        "stock": "Stock",
        "update_stock": "Update Stock",
        "remove": "Remove",
        "register": "Register",
        "member_name": "Full Name",
        "email": "Email",
        "phone": "Phone",
        "tier": "Tier",
        "issue": "Issue",
        "return": "Return",
        "renew": "Renew",
        "active_loans": "Active Loans",
        "look_up": "Look Up",
        "record_payment": "Record Payment",
        "member_id": "Member ID",
        "amount": "Amount",
        "pay": "Pay",
        "outstanding_balances": "Outstanding Balances",
        "balance": "Balance",
        "catalogue_circulation": "Catalogue & Circulation",
        "demand_forecast": "Demand Forecast",
        "forecast_months": "Forecast Months Ahead",
        "books_to_rank": "Books to Rank",
        "system_time": "System Time",
        "current_date": "Current Date",
        "transaction": "Transaction",
        "name": "Name",
        "active": "Active",
        "joined": "Joined",
        "fine": "Fine",
        "no_active_members": "No active members",
        "no_available_books": "No available books",
        "deactivate": "Deactivate",
        "confirm_removal": "Confirm Removal",
        "no_active_loans": "No active loans",
        "returned_on_time": "Returned on Time",
        "days_late": "Day(s) Late",
        "fine_incurred": "Fine Incurred",
        "due": "Due",
        "filter_by_tier": "Filter by Tier",
        "filter_by_status": "Filter by Status",
        "filter_by_outstanding_fine": "Filter by Outstanding Fine",
        "member_details": "Member Details",
        "view_history": "View History",
        "sort_by": "Sort By",
        "ascending": "Ascending",
        "descending": "Descending",
        "welcome_back": "Welcome back to your library",
        "tagline": "Manage, explore, and enjoy your book collection",
        "quick_stats": "Quick Stats",
        "recent_activity": "Recent Activity",
        "manage_books": "Manage your book collection",
        "manage_members": "Manage library members",
        "borrow_return": "Borrow and return books",
        "track_fines": "Track and manage fines",
        "insights": "Library insights and forecasts",
    },
    "hi": {
        "app_name": "किताबों की दुनिया",
        "nav": "नेविगेशन",
        "overview": "अवलोकन",
        "catalogue": "सूची",
        "members": "सदस्य",
        "circulation": "प्रचलन",
        "fines": "जुर्माना",
        "analytics": "विश्लेषण",
        "settings": "सेटिंग्स",
        "theme": "थीम",
        "language": "भाषा",
        "light": "प्रकाश",
        "dark": "अंधकार",
        "titles": "शीर्षक",
        "copies": "प्रतियाँ",
        "on_loan": "उधार पर",
        "members_count": "सदस्य",
        "overdue": "विलंब से",
        "fines_due": "देय जुर्माना",
        "overdue_loans": "विलंब से उधार",
        "genre_distribution": "शैली वितरण",
        "nothing_here": "यहाँ कुछ नहीं है",
        "search": "खोज",
        "genre": "शैली",
        "all": "सभी",
        "no_books_found": "कोई किताब नहीं मिली",
        "add_book": "किताब जोड़ें",
        "title": "शीर्षक",
        "author": "लेखक",
        "year": "वर्ष",
        "isbn": "ISBN",
        "copies_count": "प्रतियाँ",
        "price": "कीमत",
        "rating": "रेटिंग",
        "add": "जोड़ें",
        "successfully_added": "सफलतापूर्वक जोड़ा गया",
        "stock": "स्टॉक",
        "update_stock": "स्टॉक अपडेट करें",
        "remove": "हटाएं",
        "register": "पंजीकरण",
        "member_name": "पूरा नाम",
        "email": "ईमेल",
        "phone": "फोन",
        "tier": "स्तर",
        "issue": "जारी करें",
        "return": "लौटाएं",
        "renew": "नवीनीकरण करें",
        "active_loans": "सक्रिय उधार",
        "look_up": "खोज",
        "record_payment": "भुगतान रिकॉर्ड करें",
        "member_id": "सदस्य आईडी",
        "amount": "राशि",
        "pay": "भुगतान करें",
        "outstanding_balances": "बकाया शेष",
        "balance": "शेष",
        "catalogue_circulation": "सूची और प्रचलन",
        "demand_forecast": "मांग का पूर्वानुमान",
        "forecast_months": "महीनों आगे पूर्वानुमास",
        "books_to_rank": "रैंक करने के लिए किताबें",
        "system_time": "सिस्टम समय",
        "current_date": "वर्तमान तारीख",
        "transaction": "लेनदेन",
        "name": "नाम",
        "active": "सक्रिय",
        "joined": "शामिल हुए",
        "fine": "जुर्माना",
        "no_active_members": "कोई सक्रिय सदस्य नहीं",
        "no_available_books": "कोई उपलब्ध किताब नहीं",
        "deactivate": "निष्क्रिय करें",
        "confirm_removal": "हटाने की पुष्टि करें",
        "no_active_loans": "कोई सक्रिय उधार नहीं",
        "returned_on_time": "समय पर लौटाया गया",
        "days_late": "दिन विलंब से",
        "fine_incurred": "जुर्माना लगाया गया",
        "due": "देय",
        "filter_by_tier": "स्तर से फ़िल्टर करें",
        "filter_by_status": "स्थिति से फ़िल्टर करें",
        "filter_by_outstanding_fine": "बकाया जुर्माना से फ़िल्टर करें",
        "member_details": "सदस्य विवरण",
        "view_history": "इतिहास देखें",
        "sort_by": "द्वारा क्रमबद्ध करें",
        "ascending": "आरोही",
        "descending": "अवरोही",
        "welcome_back": "अपनी पुस्तकालय में वापस स्वागत है",
        "tagline": "अपने पुस्तक संग्रह का प्रबंधन करें, खोजें और आनंद लें",
        "quick_stats": "त्वरित आँकड़े",
        "recent_activity": "हालिया गतिविधि",
        "manage_books": "अपने पुस्तक संग्रह का प्रबंधन करें",
        "manage_members": "पुस्तकालय सदस्यों का प्रबंधन करें",
        "borrow_return": "पुस्तकें उधार लें और लौटाएं",
        "track_fines": "जुर्माने ट्रैक और प्रबंधित करें",
        "insights": "पुस्तकालय अंतर्दृष्टि और पूर्वानुमान",
    },
}

# ── Session State Management ─────────────────────────────────────────
if "language" not in st.session_state:
    st.session_state.language = "en"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "page" not in st.session_state:
    st.session_state.page = "overview"
if "notifications" not in st.session_state:
    st.session_state.notifications = []

def t(key: str) -> str:
    """Translate key based on current language."""
    lang = st.session_state.language
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# ── Theme Colors (Soft & User-Friendly) ─────────────────────────────
THEMES = {
    "light": {
        "bg": "#fafaf9",
        "bg_secondary": "#f5f5f4",
        "bg_card": "#ffffff",
        "fg": "#1c1917",
        "fg_muted": "#78716c",
        "border": "#e7e5e4",
        "accent": "#6366f1",
        "accent_light": "#eef2ff",
        "accent_warm": "#f59e0b",
        "success_bg": "#ecfdf5",
        "success_fg": "#065f46",
        "error_bg": "#fef2f2",
        "error_fg": "#991b1b",
        "warning_bg": "#fffbeb",
        "warning_fg": "#92400e",
        "sidebar_bg": "#f8fafc",
        "shadow": "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
        "shadow_hover": "0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04)",
        "radius": "12px",
    },
    "dark": {
        "bg": "#18181b",
        "bg_secondary": "#1f1f23",
        "bg_card": "#27272a",
        "fg": "#fafaf9",
        "fg_muted": "#a1a1aa",
        "border": "#3f3f46",
        "accent": "#818cf8",
        "accent_light": "#1e1b4b",
        "accent_warm": "#fbbf24",
        "success_bg": "#064e3b",
        "success_fg": "#d1fae5",
        "error_bg": "#7f1d1d",
        "error_fg": "#fecaca",
        "warning_bg": "#78350f",
        "warning_fg": "#fef3c7",
        "sidebar_bg": "#1c1c20",
        "shadow": "0 1px 3px rgba(0,0,0,0.2)",
        "shadow_hover": "0 4px 12px rgba(0,0,0,0.3)",
        "radius": "12px",
    },
}

theme = THEMES[st.session_state.theme]

# ── SVG Library Illustrations ────────────────────────────────────────
LIBRARY_SVG_WELCOME = f'''
<svg viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-width:420px; margin: 0 auto; display:block;">
  <rect width="500" height="200" rx="16" fill="{theme['accent_light']}" opacity="0.5"/>
  <rect x="60" y="130" width="380" height="8" rx="4" fill="{theme['accent']}" opacity="0.3"/>
  <rect x="60" y="80" width="380" height="8" rx="4" fill="{theme['accent']}" opacity="0.3"/>
  <rect x="80" y="40" width="22" height="38" rx="3" fill="#6366f1" opacity="0.8"/>
  <rect x="106" y="45" width="18" height="33" rx="3" fill="#8b5cf6" opacity="0.8"/>
  <rect x="128" y="38" width="24" height="40" rx="3" fill="#ec4899" opacity="0.7"/>
  <rect x="156" y="42" width="20" height="36" rx="3" fill="#f59e0b" opacity="0.8"/>
  <rect x="180" y="36" width="26" height="42" rx="3" fill="#10b981" opacity="0.8"/>
  <rect x="210" y="44" width="18" height="34" rx="3" fill="#3b82f6" opacity="0.7"/>
  <rect x="232" y="40" width="22" height="38" rx="3" fill="#ef4444" opacity="0.7"/>
  <rect x="258" y="46" width="16" height="32" rx="3" fill="#6366f1" opacity="0.6"/>
  <rect x="278" y="38" width="24" height="40" rx="3" fill="#8b5cf6" opacity="0.8"/>
  <rect x="306" y="42" width="20" height="36" rx="3" fill="#f59e0b" opacity="0.7"/>
  <rect x="330" y="40" width="22" height="38" rx="3" fill="#10b981" opacity="0.7"/>
  <rect x="356" y="44" width="18" height="34" rx="3" fill="#ec4899" opacity="0.8"/>
  <rect x="378" y="38" width="26" height="40" rx="3" fill="#3b82f6" opacity="0.8"/>
  <rect x="408" y="42" width="20" height="36" rx="3" fill="#6366f1" opacity="0.7"/>
  <rect x="75" y="92" width="24" height="36" rx="3" fill="#3b82f6" opacity="0.8"/>
  <rect x="103" y="96" width="20" height="32" rx="3" fill="#10b981" opacity="0.7"/>
  <rect x="127" y="90" width="26" height="38" rx="3" fill="#f59e0b" opacity="0.8"/>
  <rect x="157" y="94" width="18" height="34" rx="3" fill="#ef4444" opacity="0.7"/>
  <rect x="179" y="88" width="22" height="40" rx="3" fill="#8b5cf6" opacity="0.8"/>
  <rect x="205" y="95" width="20" height="33" rx="3" fill="#6366f1" opacity="0.7"/>
  <rect x="229" y="90" width="24" height="38" rx="3" fill="#ec4899" opacity="0.8"/>
  <rect x="257" y="94" width="18" height="34" rx="3" fill="#10b981" opacity="0.7"/>
  <rect x="279" y="88" width="26" height="40" rx="3" fill="#f59e0b" opacity="0.8"/>
  <rect x="309" y="92" width="20" height="36" rx="3" fill="#3b82f6" opacity="0.8"/>
  <rect x="333" y="96" width="18" height="32" rx="3" fill="#6366f1" opacity="0.7"/>
  <rect x="355" y="90" width="24" height="38" rx="3" fill="#8b5cf6" opacity="0.8"/>
  <rect x="383" y="94" width="20" height="34" rx="3" fill="#ef4444" opacity="0.7"/>
  <rect x="407" y="88" width="22" height="40" rx="3" fill="#10b981" opacity="0.8"/>
  <rect x="420" y="40" width="6" height="88" rx="3" fill="{theme['fg_muted']}" opacity="0.3"/>
  <ellipse cx="423" cy="40" rx="25" ry="8" fill="{theme['accent_warm']}" opacity="0.3"/>
  <ellipse cx="423" cy="38" rx="18" ry="5" fill="{theme['accent_warm']}" opacity="0.5"/>
  <rect x="38" y="125" width="16" height="18" rx="3" fill="{theme['accent']}" opacity="0.2"/>
  <circle cx="46" cy="118" r="12" fill="#10b981" opacity="0.4"/>
  <circle cx="40" cy="112" r="8" fill="#10b981" opacity="0.3"/>
  <circle cx="52" cy="110" r="9" fill="#10b981" opacity="0.35"/>
</svg>
'''

LIBRARY_SVG_SMALL = f'''
<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-width:48px;">
  <rect x="5" y="8" width="12" height="20" rx="2" fill="{theme['accent']}" opacity="0.8"/>
  <rect x="19" y="12" width="10" height="16" rx="2" fill="#8b5cf6" opacity="0.8"/>
  <rect x="31" y="6" width="14" height="22" rx="2" fill="#ec4899" opacity="0.7"/>
  <rect x="47" y="10" width="10" height="18" rx="2" fill="#f59e0b" opacity="0.8"/>
  <rect x="5" y="30" width="52" height="4" rx="2" fill="{theme['fg_muted']}" opacity="0.2"/>
  <rect x="8" y="36" width="10" height="18" rx="2" fill="#3b82f6" opacity="0.7"/>
  <rect x="20" y="34" width="12" height="20" rx="2" fill="#10b981" opacity="0.8"/>
  <rect x="34" y="38" width="10" height="16" rx="2" fill="#6366f1" opacity="0.7"/>
  <rect x="46" y="36" width="12" height="18" rx="2" fill="#ef4444" opacity="0.7"/>
  <rect x="5" y="56" width="52" height="3" rx="1.5" fill="{theme['fg_muted']}" opacity="0.2"/>
</svg>
'''

LIBRARY_SVG_EMPTY = f'''
<svg viewBox="0 0 200 160" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-width:180px; margin: 0 auto; display:block; opacity: 0.5;">
  <path d="M40 100 Q100 70 160 100 L160 60 Q100 30 40 60 Z" fill="{theme['accent']}" fill-opacity="0.15" stroke="{theme['accent']}" stroke-width="1.5" stroke-opacity="0.3"/>
  <path d="M100 75 L100 35" stroke="{theme['accent']}" stroke-width="1.5" opacity="0.3"/>
  <line x1="55" y1="72" x2="90" y2="62" stroke="{theme['fg_muted']}" stroke-width="1" opacity="0.2"/>
  <line x1="55" y1="80" x2="88" y2="70" stroke="{theme['fg_muted']}" stroke-width="1" opacity="0.2"/>
  <line x1="55" y1="88" x2="86" y2="78" stroke="{theme['fg_muted']}" stroke-width="1" opacity="0.2"/>
  <line x1="110" y1="62" x2="145" y2="72" stroke="{theme['fg_muted']}" stroke-width="1" opacity="0.2"/>
  <line x1="112" y1="70" x2="145" y2="80" stroke="{theme['fg_muted']}" stroke-width="1" opacity="0.2"/>
  <line x1="114" y1="78" x2="145" y2="88" stroke="{theme['fg_muted']}" stroke-width="1" opacity="0.2"/>
  <circle cx="140" cy="45" r="14" fill="none" stroke="{theme['accent_warm']}" stroke-width="2" opacity="0.4"/>
  <line x1="150" y1="55" x2="160" y2="65" stroke="{theme['accent_warm']}" stroke-width="2.5" stroke-linecap="round" opacity="0.4"/>
  <circle cx="170" cy="30" r="2" fill="{theme['accent_warm']}" opacity="0.3"/>
  <circle cx="35" cy="50" r="1.5" fill="{theme['accent']}" opacity="0.3"/>
</svg>
'''

# ── Apply Clean, User-Friendly Styling ───────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* === Subtle Animations (NO up/down / bounce) === */
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

@keyframes slideInLeft {{
    from {{ opacity: 0; transform: translateX(-16px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(16px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes scaleIn {{
    from {{ opacity: 0; transform: scale(0.96); }}
    to {{ opacity: 1; transform: scale(1); }}
}}

@keyframes shimmer {{
    0% {{ background-position: -1000px 0; }}
    100% {{ background-position: 1000px 0; }}
}}

@keyframes float {{
    0%, 100% {{ transform: rotate(0deg); }}
    25% {{ transform: rotate(1deg); }}
    75% {{ transform: rotate(-1deg); }}
}}

@keyframes gentlePulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.85; }}
}}

@keyframes slideInToast {{
    from {{ opacity: 0; transform: translateX(100%); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes toastFade {{
    to {{ opacity: 0; transform: translateX(100%); }}
}}

@keyframes drawLine {{
    from {{ width: 0; }}
    to {{ width: 60px; }}
}}

/* === Base Styles === */
html, body, [class*="st-"] {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    color: {theme['fg']} !important;
    background-color: {theme['bg']} !important;
}}

#MainMenu, footer, header[data-testid="stHeader"] {{
    visibility: hidden;
    height: 0 !important;
    padding: 0 !important;
}}

.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1360px !important;
    animation: fadeIn 0.5s ease-out;
}}

/* === Sidebar === */
section[data-testid="stSidebar"] {{
    background: {theme['sidebar_bg']} !important;
    border-right: 1px solid {theme['border']} !important;
    animation: slideInLeft 0.4s ease-out;
}}

section[data-testid="stSidebar"] .stRadio > label {{
    font-size: 0.85rem;
    font-weight: 500;
    color: {theme['fg_muted']};
    transition: color 0.2s ease;
}}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"] > div {{
    background: {theme['accent_light']} !important;
    border-color: {theme['accent']} !important;
    border-radius: {theme['radius']} !important;
    border-left: 3px solid {theme['accent']} !important;
}}

section[data-testid="stSidebar"] .stRadio [aria-checked="true"] > div p {{
    color: {theme['accent']} !important;
    font-weight: 600;
}}

/* === Headings === */
h1 {{
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
    color: {theme['fg']} !important;
    margin-bottom: 0.25rem !important;
}}

h2 {{
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: {theme['fg']} !important;
    margin-top: 1.25rem !important;
    margin-bottom: 0.75rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid {theme['border']} !important;
    position: relative;
}}

h2::after {{
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    display: inline-block;
    width: 60px;
    height: 2px;
    background: {theme['accent']};
    animation: drawLine 0.6s ease-out;
    border-radius: 1px;
}}

h3 {{
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: {theme['fg']} !important;
}}

/* === Metrics === */
[data-testid="stMetric"] {{
    background: {theme['bg_card']} !important;
    border: 1px solid {theme['border']} !important;
    border-radius: {theme['radius']} !important;
    padding: 1.1rem 1.25rem !important;
    animation: scaleIn 0.4s ease-out;
    transition: all 0.25s ease;
    box-shadow: {theme['shadow']} !important;
}}

[data-testid="stMetric"]:hover {{
    box-shadow: {theme['shadow_hover']} !important;
    border-color: {theme['accent']} !important;
}}

[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: {theme['accent']} !important;
}}

[data-testid="stMetricLabel"] {{
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: {theme['fg_muted']} !important;
}}

/* === DataFrames === */
[data-testid="stDataFrame"] {{
    border: 1px solid {theme['border']} !important;
    border-radius: {theme['radius']} !important;
    overflow: hidden !important;
    animation: fadeIn 0.5s ease-out;
    box-shadow: {theme['shadow']} !important;
}}

[data-testid="stDataFrame"] thead th {{
    background: {theme['bg_secondary']} !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    color: {theme['accent']} !important;
    border-bottom: 2px solid {theme['accent']} !important;
    padding: 0.7rem 1rem !important;
}}

[data-testid="stDataFrame"] tbody tr {{
    transition: background-color 0.2s ease;
}}

[data-testid="stDataFrame"] tbody tr:hover {{
    background-color: {theme['accent_light']} !important;
}}

[data-testid="stDataFrame"] td {{
    font-size: 0.85rem !important;
    padding: 0.65rem 1rem !important;
    border-bottom: 1px solid {theme['border']} !important;
    color: {theme['fg']} !important;
}}

/* === Buttons === */
.stButton > button {{
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border-radius: {theme['radius']} !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
    cursor: pointer;
}}

.stButton > button[kind="primary"] {{
    background: {theme['accent']} !important;
    color: white !important;
    box-shadow: 0 1px 3px rgba(99, 102, 241, 0.3);
}}

.stButton > button[kind="primary"]:hover {{
    opacity: 0.9;
    box-shadow: 0 3px 8px rgba(99, 102, 241, 0.3) !important;
}}

.stButton > button[kind="secondary"] {{
    background: {theme['bg_card']} !important;
    border: 1px solid {theme['border']} !important;
    color: {theme['fg']} !important;
}}

.stButton > button[kind="secondary"]:hover {{
    background: {theme['bg_secondary']} !important;
    border-color: {theme['accent']} !important;
}}

/* === Inputs === */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > input {{
    font-size: 0.85rem !important;
    border-radius: {theme['radius']} !important;
    border: 1px solid {theme['border']} !important;
    padding: 0.55rem 0.8rem !important;
    background-color: {theme['bg_card']} !important;
    color: {theme['fg']} !important;
    transition: all 0.2s ease;
}}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div > input:focus {{
    border-color: {theme['accent']} !important;
    box-shadow: 0 0 0 3px {theme['accent_light']} !important;
    outline: none;
}}

label[data-testid="stWidgetLabel"] {{
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: {theme['fg_muted']} !important;
}}

/* === Tabs === */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0 !important;
    border-bottom: 1px solid {theme['border']} !important;
}}

.stTabs [data-baseweb="tab"] {{
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: {theme['fg_muted']} !important;
    padding: 0.7rem 1.2rem !important;
    border-radius: 0 !important;
    transition: color 0.2s ease;
    cursor: pointer;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: {theme['accent']};
}}

.stTabs [aria-selected="true"] {{
    color: {theme['accent']} !important;
}}

.stTabs [data-baseweb="tab-highlight"] {{
    background-color: {theme['accent']} !important;
    height: 2px !important;
    transition: all 0.3s ease;
}}

/* === Forms === */
[data-testid="stForm"] {{
    background: {theme['bg_card']} !important;
    border: 1px solid {theme['border']} !important;
    border-radius: {theme['radius']};
    padding: 1.5rem !important;
    animation: scaleIn 0.4s ease-out;
    box-shadow: {theme['shadow']} !important;
}}

/* === Alerts === */
[data-testid="stSuccess"] > div {{
    background: {theme['success_bg']} !important;
    border: 1px solid #10b981 !important;
    border-radius: {theme['radius']} !important;
    color: {theme['success_fg']} !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    animation: slideInRight 0.3s ease-out;
}}

[data-testid="stError"] > div {{
    background: {theme['error_bg']} !important;
    border: 1px solid #ef4444 !important;
    border-radius: {theme['radius']} !important;
    color: {theme['error_fg']} !important;
    font-size: 0.85rem !important;
    animation: slideInRight 0.3s ease-out;
}}

[data-testid="stWarning"] > div {{
    background: {theme['warning_bg']} !important;
    border: 1px solid #f59e0b !important;
    border-radius: {theme['radius']} !important;
    color: {theme['warning_fg']} !important;
    font-size: 0.85rem !important;
    animation: slideInRight 0.3s ease-out;
}}

hr, .stDivider {{
    border-color: {theme['border']} !important;
    margin: 1.5rem 0 !important;
}}

/* === Images === */
.stImage > img {{
    border-radius: {theme['radius']} !important;
    transition: opacity 0.2s ease;
}}

.stImage > img:hover {{
    opacity: 0.9;
}}

/* === Cards === */
.metric-card, .filter-card, .member-card, .stat-box {{
    background: {theme['bg_card']};
    border: 1px solid {theme['border']};
    border-radius: {theme['radius']};
    padding: 1.25rem;
    text-align: center;
    animation: scaleIn 0.4s ease-out;
    transition: all 0.25s ease;
    box-shadow: {theme['shadow']};
}}

.metric-card:hover, .filter-card:hover, .member-card:hover, .stat-box:hover {{
    box-shadow: {theme['shadow_hover']};
    border-color: {theme['accent']};
}}

/* === Empty State === */
.empty-state {{
    padding: 2.5rem;
    text-align: center;
    color: {theme['fg_muted']};
    font-size: 0.9rem;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    border-radius: {theme['radius']};
    background: {theme['bg_card']};
    border: 1px dashed {theme['border']};
    animation: fadeIn 0.5s ease-out;
}}

/* === Library Header === */
.library-header {{
    text-align: center;
    margin-bottom: 1.5rem;
    padding: 1rem 0;
    animation: fadeIn 0.5s ease-out;
}}

.library-header h1 {{
    font-size: 2rem;
    font-weight: 700;
    color: {theme['fg']};
    margin-bottom: 0.25rem;
    letter-spacing: -0.03em;
}}

.library-header p {{
    color: {theme['fg_muted']};
    font-size: 0.95rem;
    font-weight: 400;
    animation: fadeIn 0.6s ease-out 0.15s backwards;
}}

/* === Welcome Banner === */
.welcome-banner {{
    background: {theme['bg_card']};
    border: 1px solid {theme['border']};
    border-radius: 16px;
    padding: 2rem 2.5rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    animation: slideInLeft 0.5s ease-out;
    box-shadow: {theme['shadow']};
    overflow: hidden;
    position: relative;
}}

.welcome-banner::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, {theme['accent']}, #8b5cf6, #ec4899, {theme['accent']});
    background-size: 200% 100%;
    animation: shimmer 4s linear infinite;
}}

.welcome-text h2 {{
    border: none !important;
    padding: 0 !important;
    margin: 0 0 0.5rem 0 !important;
    font-size: 1.5rem !important;
}}

.welcome-text h2::after {{
    display: none;
}}

.welcome-text p {{
    color: {theme['fg_muted']};
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0;
}}

.welcome-illustration {{
    flex-shrink: 0;
    animation: float 6s ease-in-out infinite;
}}

/* === Section Description Cards === */
.section-desc {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    background: {theme['bg_card']};
    border: 1px solid {theme['border']};
    border-radius: {theme['radius']};
    margin-bottom: 1.5rem;
    animation: fadeIn 0.4s ease-out;
    box-shadow: {theme['shadow']};
}}

.section-desc-icon {{
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: {theme['accent_light']};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}}

.section-desc-text h3 {{
    font-size: 0.95rem !important;
    margin: 0 0 0.15rem 0 !important;
}}

.section-desc-text p {{
    color: {theme['fg_muted']};
    font-size: 0.8rem;
    margin: 0;
}}

/* === Sidebar Time Widget === */
.time-widget {{
    background: {theme['bg_card']};
    border: 1px solid {theme['border']};
    border-radius: {theme['radius']};
    padding: 0.75rem 1rem;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    color: {theme['accent']};
    box-shadow: {theme['shadow']};
}}

/* === Notification Toasts === */
.toast-container {{
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 8px;
    pointer-events: none;
}}

.toast {{
    min-width: 260px;
    max-width: 360px;
    padding: 12px 16px;
    border-radius: {theme['radius']};
    color: white;
    font-weight: 500;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 10px;
    pointer-events: auto;
    animation: slideInToast 0.3s ease-out, toastFade 0.3s ease-in 4s forwards;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.toast-success {{ background: #10b981; }}
.toast-error {{ background: #ef4444; }}
.toast-warning {{ background: #f59e0b; color: #1c1917; }}
.toast-info {{ background: {theme['accent']}; }}

.toast-icon {{
    font-size: 1.2rem;
}}

/* === Responsive === */
@media (max-width: 768px) {{
    .welcome-banner {{
        flex-direction: column;
        text-align: center;
        padding: 1.5rem;
    }}
    .welcome-illustration {{
        order: -1;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def rerun():
    """Rerun the app."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def id_from_choice(choice: str) -> str:
    """Extract ID from formatted choice string."""
    return choice.split(" — ")[0].strip()

def fmt_currency(val):
    """Format value as currency."""
    return f"{config.CURRENCY_SYMBOL}{val:,.2f}"

def empty_state(msg: str = None):
    """Display empty state with library illustration."""
    msg = msg or t("nothing_here")
    st.markdown(
        f'<div class="empty-state">{LIBRARY_SVG_EMPTY}<span>{msg}</span></div>',
        unsafe_allow_html=True,
    )

def library_header():
    """Display clean library header."""
    st.markdown(f"""
    <div class="library-header">
        <h1>{t('app_name')}</h1>
        <p>{t('tagline')}</p>
    </div>
    """, unsafe_allow_html=True)

def section_description(icon: str, title: str, desc: str):
    """Display a section description card with icon."""
    st.markdown(f"""
    <div class="section-desc">
        <div class="section-desc-icon">{icon}</div>
        <div class="section-desc-text">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  NOTIFICATION SYSTEM
# ══════════════════════════════════════════════════════════════════════

NOTIFY_ICONS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
}

def notify(message: str, kind: str = "info"):
    """Push a toast notification."""
    notif = {
        "id": time.time(),
        "message": message,
        "kind": kind,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.notifications.append(notif)
    if len(st.session_state.notifications) > 20:
        st.session_state.notifications = st.session_state.notifications[-20:]

def notify_success(msg): notify(msg, "success")
def notify_error(msg): notify(msg, "error")
def notify_warning(msg): notify(msg, "warning")
def notify_info(msg): notify(msg, "info")

def _render_toasts():
    """Render active toast notifications."""
    active = st.session_state.notifications[-5:]
    if not active:
        return
    toasts_html = '<div class="toast-container">'
    for n in active:
        icon = NOTIFY_ICONS.get(n["kind"], "ℹ️")
        safe_msg = html.escape(n['message'])
        toasts_html += f"""
        <div class="toast toast-{n['kind']}">
            <span class="toast-icon">{icon}</span>
            <div>
                <div style="font-weight:600;">{safe_msg}</div>
                <div style="font-size:0.7rem; opacity:0.8;">{n['timestamp']}</div>
            </div>
        </div>
        """
    toasts_html += '</div>'
    st.markdown(toasts_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  INITIALIZATION
# ══════════════════════════════════════════════════════════════════════

db = DatabaseManager()
lm = LibraryManager(db)
stats = LibraryStatistics(db)
viz = LibraryVisualizer(stats)

if lm.refresh_overdue_statuses():
    db.save_all()

def persist():
    """Save all database changes."""
    db.save_all()

# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR & NAVIGATION
# ══════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Sidebar Logo
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0; animation: fadeIn 0.4s ease-out;">
        {LIBRARY_SVG_SMALL}
        <div style="font-size: 1.1rem; font-weight: 700; color: {theme['fg']};
                    margin-top: 0.5rem; letter-spacing: -0.02em;">
            {t('app_name')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"<div style='font-size: 0.7rem; font-weight: 600; color: {theme['fg_muted']}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.06em;'>{t('nav')}</div>", unsafe_allow_html=True)

    page = st.radio(
        "Page",
        ["overview", "catalogue", "members", "circulation", "fines", "analytics"],
        format_func=lambda x: {"overview": "📊  " + t("overview"),
                                "catalogue": "📖  " + t("catalogue"),
                                "members": "👥  " + t("members"),
                                "circulation": "🔄  " + t("circulation"),
                                "fines": "💰  " + t("fines"),
                                "analytics": "📈  " + t("analytics")}[x],
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.divider()

    # Quick Stats
    st.markdown(f"<div style='font-size: 0.7rem; font-weight: 600; color: {theme['fg_muted']}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.06em;'>{t('quick_stats')}</div>", unsafe_allow_html=True)

    counts = lm.dashboard_counts()
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t("titles"), counts["distinct_titles"])
        st.metric(t("members_count"), counts["total_members"])
    with col2:
        st.metric(t("on_loan"), counts["currently_issued"])
        overdue_count = len(stats.overdue_analysis()) if not stats.overdue_analysis().empty else 0
        st.metric(t("overdue"), overdue_count)

    st.divider()

    # Settings
    st.markdown(f"<div style='font-size: 0.7rem; font-weight: 600; color: {theme['fg_muted']}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.06em;'>⚙️ {t('settings')}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        new_theme = st.selectbox(
            t("theme"),
            ["light", "dark"],
            index=0 if st.session_state.theme == "light" else 1,
            label_visibility="collapsed",
        )
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            rerun()

    with col2:
        new_lang = st.selectbox(
            t("language"),
            ["en", "hi"],
            index=0 if st.session_state.language == "en" else 1,
            label_visibility="collapsed",
        )
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            rerun()

    st.divider()

    # System Time
    st.markdown(f"<div style='font-size: 0.7rem; font-weight: 600; color: {theme['fg_muted']}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.06em;'>⏰ {t('system_time')}</div>", unsafe_allow_html=True)

    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%d %b %Y')
    st.markdown(f"""
    <div class="time-widget">
        <div style="font-size: 1.1rem; font-weight: 600;">{current_time}</div>
        <div style="font-size: 0.75rem; color: {theme['fg_muted']}; margin-top: 2px;">{current_date}</div>
    </div>
    """, unsafe_allow_html=True)

# Render Toasts
if st.session_state.get("notifications"):
    _render_toasts()


# ══════════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════

# ── OVERVIEW PAGE ────────────────────────────────────────────────────
if st.session_state.page == "overview":
    # Welcome Banner with Library Illustration
    st.markdown(f"""
    <div class="welcome-banner">
        <div class="welcome-text">
            <h2>{t('welcome_back')}</h2>
            <p>{t('tagline')}. Here's a quick snapshot of your library today.</p>
        </div>
        <div class="welcome-illustration">
            {LIBRARY_SVG_WELCOME}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    overdue_df = stats.overdue_analysis()
    fine_summary = stats.fine_revenue_summary()

    # Metrics Row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.metric("📚 " + t("titles"), counts["distinct_titles"])
    with m2:
        st.metric("📕 " + t("copies"), counts["total_books"])
    with m3:
        st.metric("👥 " + t("members_count"), counts["total_members"])
    with m4:
        st.metric("🔄 " + t("on_loan"), counts["currently_issued"])
    with m5:
        st.metric("⚠️ " + t("overdue"), len(overdue_df))
    with m6:
        st.metric("💰 " + t("fines_due"), fmt_currency(fine_summary["outstanding"]["total"]))

    st.divider()

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("⏰ " + t("overdue_loans"))
        if overdue_df.empty:
            empty_state(t("nothing_here"))
        else:
            st.dataframe(
                overdue_df.rename(columns={
                    "txn_id": "Txn", "book_id": "Book", "member_id": "Member",
                    "due_date": "Due", "days_overdue": "Late", "projected_fine": "Fine",
                }),
                use_container_width=True, hide_index=True, height=300,
            )

    with right:
        st.subheader("📊 " + t("genre_distribution"))
        genre_series = stats.genre_distribution()
        if genre_series.empty:
            empty_state(t("nothing_here"))
        else:
            st.bar_chart(genre_series, height=300, use_container_width=True)


# ── CATALOGUE PAGE ───────────────────────────────────────────────────
elif st.session_state.page == "catalogue":
    library_header()
    section_description("📖", t("catalogue"), t("manage_books"))

    sc, gc, _ = st.columns([2, 1, 0.5])
    keyword = sc.text_input("🔍 " + t("search"), placeholder=t("search") + "…", key="book_search")
    genre_filter = gc.selectbox(t("genre"), ["All"] + config.VALID_GENRES, key="genre_filter")

    results = lm.search_catalogue(keyword) if keyword else db.books.copy()
    if genre_filter != "All":
        results = results[results["genre"] == genre_filter]

    if results.empty:
        empty_state(t("no_books_found"))
    else:
        st.dataframe(
            results[["book_id", "title", "author", "genre", "available_copies", "total_copies", "price", "isbn"]]
            .rename(columns={
                "book_id": "ID", "title": "Title", "author": "Author", "genre": "Genre",
                "available_copies": "Avail", "total_copies": "Total", "price": "Price", "isbn": "ISBN",
            }),
            use_container_width=True, hide_index=True, height=340,
        )

    st.divider()
    tab_add, tab_stock, tab_remove = st.tabs([
        "📝 " + t("add_book"),
        "📦 " + t("stock"),
        "🗑️ " + t("remove"),
    ])

    with tab_add:
        with st.form("add_book_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            title = c1.text_input(t("title"))
            author = c2.text_input(t("author"))
            c3, c4 = st.columns(2)
            genre = c3.selectbox(t("genre"), config.VALID_GENRES)
            year = c4.number_input(t("year"), min_value=1450, max_value=2100, value=date.today().year, step=1)
            c5, c6 = st.columns(2)
            isbn = c5.text_input(t("isbn"))
            copies = c6.number_input(t("copies_count"), min_value=1, value=1, step=1)
            c7, c8 = st.columns(2)
            price = c7.number_input(t("price"), min_value=0.0, value=0.0, step=10.0)
            rating = c8.number_input(t("rating"), min_value=0.0, max_value=5.0, value=0.0, step=0.1)
            submitted = st.form_submit_button("✅ " + t("add"), type="primary")
        if submitted:
            try:
                book = lm.add_book(title=title, author=author, genre=genre,
                                   publication_year=int(year), isbn=isbn,
                                   total_copies=int(copies), price=price, rating=rating)
                persist()
                st.success(f'✅ {t("successfully_added")}: "{book.title}" — {book.book_id}')
                notify_success(f'Book added: "{book.title}" — {book.book_id}')
                rerun()
            except exc.LibraryError as e:
                st.error(f"❌ {str(e)}")
                notify_error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
                notify_error(f"Error: {str(e)}")

    with tab_stock:
        if db.books.empty:
            empty_state(t("no_books_found"))
        else:
            options = [f"{r.book_id} — {r.title} ({r.available_copies}/{r.total_copies})" for r in db.books.itertuples()]
            choice = st.selectbox(t("title"), options, key="stock_choice")
            delta = st.number_input(t("copies_count"), value=1, step=1, key="stock_delta")
            if st.button("✅ " + t("update_stock"), type="primary", key="stock_submit"):
                try:
                    book = lm.update_book_stock(id_from_choice(choice), int(delta))
                    persist()
                    st.success(f"✅ {book.book_id} → {book.available_copies}/{book.total_copies}")
                    notify_success(f"Stock updated: {book.book_id} → {book.available_copies}/{book.total_copies}")
                    rerun()
                except exc.LibraryError as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")

    with tab_remove:
        if db.books.empty:
            empty_state(t("no_books_found"))
        else:
            options = [f"{r.book_id} — {r.title}" for r in db.books.itertuples()]
            choice = st.selectbox(t("title"), options, key="remove_choice")
            confirm = st.checkbox(f'{t("confirm_removal")}: {id_from_choice(choice)}', key="remove_confirm")
            if st.button("🗑️ " + t("remove"), type="primary", disabled=not confirm, key="remove_submit"):
                try:
                    lm.remove_book(id_from_choice(choice))
                    persist()
                    st.success(f"✅ {t('remove')}: {id_from_choice(choice)}")
                    notify_info(f"Book removed: {id_from_choice(choice)}")
                    rerun()
                except exc.LibraryError as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")


# ── MEMBERS PAGE ─────────────────────────────────────────────────────
elif st.session_state.page == "members":
    library_header()
    section_description("👥", t("members"), t("manage_members"))

    with st.expander("📋 Filter Options", expanded=True):
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

        with filter_col1:
            keyword = st.text_input("🔍 " + t("search"), placeholder=t("search") + "…", key="member_search")

        with filter_col2:
            tier_filter = st.multiselect(
                t("filter_by_tier"),
                options=list(config.MEMBERSHIP_TIERS.keys()),
                default=list(config.MEMBERSHIP_TIERS.keys()),
            )

        with filter_col3:
            status_filter = st.multiselect(
                t("filter_by_status"),
                options=["Active", "Inactive"],
                default=["Active", "Inactive"],
            )

        with filter_col4:
            sort_by = st.selectbox(
                t("sort_by"),
                ["name", "member_id", "joined_on", "outstanding_fine"],
                format_func=lambda x: {"name": "Name", "member_id": "ID", "joined_on": "Join Date", "outstanding_fine": "Outstanding Fine"}[x]
            )

    results = lm.search_members(keyword) if keyword else db.members.copy()

    if tier_filter:
        results = results[results["tier"].isin(tier_filter)]

    status_bool = [s == "Active" for s in status_filter]
    results = results[results["active"].isin(status_bool)]

    results = results.sort_values(sort_by, ascending=True)

    if results.empty:
        empty_state(t("nothing_here"))
    else:
        st.markdown(f"<h3>👥 {t('members')} ({len(results)})</h3>", unsafe_allow_html=True)

        for idx, row in results.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                status_emoji = "✅" if row["active"] else "❌"
                st.markdown(f"""
                <div class="member-card">
                    <div style="font-weight: 600; font-size: 1.05rem; margin-bottom: 0.4rem;">
                        {status_emoji} {row['name']}
                    </div>
                    <div style="font-size: 0.82rem; color: {theme['fg_muted']}; margin-bottom: 0.35rem;">
                        ID: {row['member_id']} &nbsp;|&nbsp; Tier: {row['tier'].title()}
                    </div>
                    <div style="font-size: 0.78rem; color: {theme['fg_muted']};">
                        📧 {row['email']} &nbsp;|&nbsp; 📱 {row['phone']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.metric("💰 Fine", fmt_currency(row["outstanding_fine"]))

            with col3:
                st.metric("📅 Joined", row['joined_on'])

    st.divider()
    tab_add, tab_deact = st.tabs(["✍️ " + t("register"), "❌ " + t("deactivate")])

    with tab_add:
        with st.form("add_member_form", clear_on_submit=True):
            name = st.text_input(t("member_name"))
            c1, c2 = st.columns(2)
            email = c1.text_input(t("email"))
            phone = c2.text_input(t("phone"), placeholder="+91-9876543210")
            tier = st.selectbox(
                t("tier"), list(config.MEMBERSHIP_TIERS.keys()),
                format_func=lambda tier_val: f"{tier_val.title()} — {config.MEMBERSHIP_TIERS[tier_val]['max_books']} books, {config.MEMBERSHIP_TIERS[tier_val]['loan_days']} days",
            )
            submitted = st.form_submit_button("✅ " + t("register"), type="primary")
        if submitted:
            try:
                member = lm.register_member(name=name, email=email, phone=phone, tier=tier)
                persist()
                st.success(f"✅ {t('successfully_added')}: {member.name} — {member.member_id}")
                notify_success(f"👤 New member registered: {member.name}")
                rerun()
            except exc.LibraryError as e:
                st.error(f"❌ {str(e)}")
                notify_error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
                notify_error(f"Error: {str(e)}")

    with tab_deact:
        active = db.members[db.members["active"] == True] if not db.members.empty else db.members
        if active.empty:
            empty_state(t("no_active_members"))
        else:
            options = [f"{r.member_id} — {r.name}" for r in active.itertuples()]
            choice = st.selectbox(t("name"), options, key="deactivate_choice")
            if st.button("❌ " + t("deactivate"), type="primary", key="deactivate_submit"):
                try:
                    lm.deactivate_member(id_from_choice(choice))
                    persist()
                    st.success(f"✅ {t('deactivate')}: {id_from_choice(choice)}")
                    notify_warning(f"Member deactivated: {id_from_choice(choice)}")
                    rerun()
                except exc.LibraryError as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")


# ── CIRCULATION PAGE ─────────────────────────────────────────────────
elif st.session_state.page == "circulation":
    library_header()
    section_description("🔄", t("circulation"), t("borrow_return"))

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📤 " + t("issue"))
        available = db.books[db.books["available_copies"] > 0] if not db.books.empty else db.books
        active_m = db.members[db.members["active"] == True] if not db.members.empty else db.members
        if available.empty or active_m.empty:
            empty_state(t("no_available_books"))
        else:
            book_choice = st.selectbox(
                t("title"),
                [f"{r.book_id} — {r.title} ({r.available_copies} left)" for r in available.itertuples()],
                key="issue_book_choice",
            )
            member_choice = st.selectbox(
                t("member_name"),
                [f"{r.member_id} — {r.name} ({r.tier})" for r in active_m.itertuples()],
                key="issue_member_choice",
            )
            if st.button("📤 " + t("issue"), type="primary", key="issue_submit"):
                try:
                    txn = lm.issue_book(id_from_choice(book_choice), id_from_choice(member_choice))
                    persist()
                    st.success(f"✅ {t('issue')}: {txn.book_id} → {txn.member_id} · {t('due')} {txn.due_date}")
                    notify_success(f"📤 Book issued: {txn.book_id} → {txn.member_id}")
                    rerun()
                except exc.LibraryError as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")

    with c2:
        st.subheader("📥 " + t("return") + " / 🔄 " + t("renew"))
        active_txns = db.transactions[db.transactions["status"] != "RETURNED"] if not db.transactions.empty else db.transactions
        if active_txns.empty:
            empty_state(t("no_active_loans"))
        else:
            txn_choice = st.selectbox(
                t("transaction"),
                [f"{r.txn_id} — {r.book_id} → {r.member_id} ({t('due')} {r.due_date})" for r in active_txns.itertuples()],
                key="txn_choice",
            )
            b1, b2 = st.columns(2)
            if b1.button("📥 " + t("return"), type="primary", key="return_submit"):
                try:
                    result = lm.return_book(id_from_choice(txn_choice))
                    persist()
                    if result["days_late"] > 0:
                        st.warning(f'⚠️ {result["days_late"]} {t("days_late")} — {fmt_currency(result["fine_incurred"])} {t("fine_incurred")}')
                        notify_warning(f"Book returned late! Fine: {fmt_currency(result['fine_incurred'])}")
                    else:
                        st.success(f"✅ {t('returned_on_time')}")
                        notify_success("Book returned on time!")
                    rerun()
                except exc.LibraryError as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")
            if b2.button("🔄 " + t("renew"), key="renew_submit"):
                try:
                    txn = lm.renew_loan(id_from_choice(txn_choice))
                    persist()
                    st.success(f"✅ {t('renew')} · {t('due')} {txn.due_date} ({txn.renewals}/{config.MAX_RENEWALS})")
                    notify_info(f"🔄 Loan renewed · Due: {txn.due_date}")
                    rerun()
                except exc.LibraryError as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    notify_error(f"Error: {str(e)}")

    st.divider()

    st.subheader("🔄 " + t("active_loans"))
    active_all = db.transactions[db.transactions["status"] != "RETURNED"] if not db.transactions.empty else db.transactions
    if active_all.empty:
        empty_state(t("no_active_loans"))
    else:
        st.dataframe(
            active_all.rename(columns={
                "txn_id": "Txn", "book_id": "Book", "member_id": "Member",
                "issue_date": "Issued", "due_date": "Due", "status": "Status",
            })[["Txn", "Book", "Member", "Issued", "Due", "Status"]],
            use_container_width=True, hide_index=True, height=280,
        )


# ── FINES PAGE ───────────────────────────────────────────────────────
elif st.session_state.page == "fines":
    library_header()
    section_description("💰", t("fines"), t("track_fines"))

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🔍 " + t("look_up"))
        with st.form("fine_lookup_form"):
            member_id_lookup = st.text_input(t("member_id"), placeholder="MB0001", key="fine_lookup_id")
            submitted = st.form_submit_button("🔍 " + t("look_up"), type="primary")
        if submitted and member_id_lookup:
            member = db.get_member(member_id_lookup.strip())
            if member is None:
                st.error(f"❌ {t('nothing_here')}: '{member_id_lookup}'")
                notify_error(f"Member not found: '{member_id_lookup}'")
            else:
                st.metric(member.name, fmt_currency(member.outstanding_fine))
                notify_info(f"Looked up fines for: {member.name}")

    with c2:
        st.subheader("💳 " + t("record_payment"))
        with st.form("pay_fine_form"):
            pay_member_id = st.text_input(t("member_id"), placeholder="MB0001")
            pay_amount = st.number_input(t("amount"), min_value=0.0, value=0.0, step=10.0)
            pay_submitted = st.form_submit_button("💳 " + t("pay"), type="primary")
        if pay_submitted and pay_member_id.strip():
            try:
                member = lm.pay_fine(pay_member_id.strip(), pay_amount)
                persist()
                st.success(f"✅ {t('pay')} · {t('balance')}: {fmt_currency(member.outstanding_fine)}")
                notify_success(f"💰 Payment recorded. Balance: {fmt_currency(member.outstanding_fine)}")
                rerun()
            except exc.LibraryError as e:
                st.error(f"❌ {str(e)}")
                notify_error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
                notify_error(f"Error: {str(e)}")

    st.divider()

    st.subheader("💰 " + t("outstanding_balances"))
    fines_df = db.members[db.members["outstanding_fine"] > 0] if not db.members.empty else db.members
    if fines_df.empty:
        empty_state(t("nothing_here"))
    else:
        st.dataframe(
            fines_df[["member_id", "name", "outstanding_fine"]]
            .rename(columns={"member_id": "ID", "name": t("name"), "outstanding_fine": t("balance")})
            .sort_values(t("balance"), ascending=False),
            use_container_width=True, hide_index=True,
        )


# ── ANALYTICS PAGE ───────────────────────────────────────────────────
elif st.session_state.page == "analytics":
    library_header()
    section_description("📈", t("analytics"), t("insights"))

    st.subheader("📚 " + t("catalogue_circulation"))
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.image(str(viz.plot_genre_distribution()), use_container_width=True)
    with r1c2:
        st.image(str(viz.plot_top_circulating_books()), use_container_width=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.image(str(viz.plot_stock_utilisation()), use_container_width=True)
    with r2c2:
        st.image(str(viz.plot_genre_demand_ratio()), use_container_width=True)

    st.divider()

    st.subheader("📈 " + t("demand_forecast"))
    periods_ahead = st.slider(t("forecast_months"), min_value=1, max_value=6, value=3, key="forecast_horizon")

    fc1, fc2 = st.columns(2)
    with fc1:
        st.image(str(viz.plot_demand_forecast(periods_ahead=periods_ahead)), use_container_width=True)
        forecast_data = stats.monthly_demand_forecast(periods_ahead)
        forecast = forecast_data["forecast"]
        if not forecast.empty:
            direction = "📈" if forecast_data["slope"] > 0 else ("📉" if forecast_data["slope"] < 0 else "➡️")
            st.metric(f"⏭️ {t('overview')} ({forecast.index[0]})", int(forecast.iloc[0]), delta=f"{direction} trending")

    with fc2:
        top_n = st.slider(t("books_to_rank"), min_value=3, max_value=15, value=8, key="predicted_top_n")
        st.image(str(viz.plot_top_predicted_books(n=top_n)), use_container_width=True)

    predicted_df = stats.top_predicted_books(top_n)
    if not predicted_df.empty:
        st.dataframe(
            predicted_df.rename(columns={
                "book_id": "ID", "title": t("title"), "genre": t("genre"),
                "predicted_next_month": "Predicted", "trend": "Trend",
            }),
            use_container_width=True, hide_index=True,
        )
