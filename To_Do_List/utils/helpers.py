from datetime import datetime

# Luminous Flow Color Palette mapped to (Light, Dark)
COLORS = {
    "background": ("#FAFAFA", "#121212"),
    "surface": ("#FFFFFF", "#1E1E1E"),
    "primary": ("#006A68", "#4FBDBA"),
    "primary_hover": ("#00504E", "#3AA09D"),
    "text": ("#1A1C1C", "#E8E0EA"),
    "text_secondary": ("#6D7979", "#978D9D"),
    "outline": ("#E3E2E2", "#37333B"),
    "error": ("#BA1A1A", "#FFB4AB"),
    
    # Priority Colors
    "priority_high": ("#BA1A1A", "#FFB4AB"), # Coral/Red
    "priority_medium": ("#944A27", "#D4CA38"), # Warm Orange/Yellow
    "priority_low": ("#006A68", "#4FBDBA") # Teal
}

def format_date(date_str: str) -> str:
    """Format YYYY-MM-DD to a more readable format, e.g., Oct 24."""
    if not date_str:
        return "No date"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except ValueError:
        return date_str
