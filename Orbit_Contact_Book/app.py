import streamlit as st
import pandas as pd
import base64
import random
from PIL import Image
import io
import datetime

# --- Database & Service Imports ---
from database import init_db
from contact_service import (
    add_contact, get_all_contacts, get_contact_by_id,
    update_contact, delete_contact, search_contacts,
    toggle_favorite, generate_sample_contacts
)

# Initialize Database on startup
init_db()

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Orbit · Contact Book",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Global CSS — Stitch-inspired light theme
# ─────────────────────────────────────────────
def load_css():
    st.markdown("""
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Force ALL text to be dark by default */
    .stApp, .stApp * {
        color: #111827;
    }

    /* ── App background ── */
    .stApp {
        background-color: #F3F4F6;
    }

    /* ── Reduce default Streamlit top padding ── */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 1200px;
    }

    /* ══════════════════════════
       SIDEBAR
    ══════════════════════════ */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB;
    }
    /* All sidebar text: force dark */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small {
        color: #111827 !important;
    }
    /* Sidebar nav buttons */
    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #374151 !important;
        border: none !important;
        border-radius: 8px;
        padding: 0.45rem 0.75rem;
        font-weight: 500;
        font-size: 0.875rem;
        width: 100%;
        text-align: left;
        transition: background 0.15s ease;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #F3F4F6 !important;
        color: #DC2626 !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #FEE2E2 !important;
        color: #DC2626 !important;
        font-weight: 600;
    }

    /* ══════════════════════════
       FORM LABELS & HEADINGS
    ══════════════════════════ */
    /* All labels inside the main area */
    label, .stTextInput label, .stTextArea label,
    .stSelectbox label, .stSlider label,
    .stFileUploader label, .stDateInput label,
    .stCheckbox label, .stRadio label {
        color: #374151 !important;
        font-size: 0.8125rem !important;
        font-weight: 500 !important;
    }
    /* Headings */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #111827 !important;
        font-weight: 700 !important;
    }
    h2 { font-size: 1.375rem !important; }
    h3 { font-size: 1.1rem !important; }
    /* Caption / small text */
    .stCaption, small, caption {
        color: #6B7280 !important;
        font-size: 0.78rem !important;
    }

    /* ══════════════════════════
       FORM INPUTS
    ══════════════════════════ */
    /* Text inputs */
    .stTextInput input,
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        font-size: 0.875rem !important;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #DC2626 !important;
        box-shadow: 0 0 0 3px rgba(220,38,38,0.12) !important;
        outline: none !important;
    }
    /* Placeholder */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #9CA3AF !important;
    }
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        color: #111827 !important;
    }
    /* Date input */
    .stDateInput > div > div input {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }
    /* Slider track */
    .stSlider [data-testid="stSlider"] div[role="slider"] {
        background-color: #DC2626 !important;
    }

    /* ══════════════════════════
       BUTTONS
    ══════════════════════════ */
    /* Primary button — red accent */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #DC2626, #B91C1C) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 1.25rem !important;
        transition: opacity 0.15s ease, transform 0.1s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }
    /* Secondary / default buttons */
    .stButton > button {
        border-radius: 7px;
        font-size: 0.8rem;
        font-weight: 500;
        padding: 0.3rem 0.65rem;
        border: 1px solid #D1D5DB;
        background-color: #FFFFFF;
        color: #374151;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        background-color: #F9FAFB;
        border-color: #DC2626;
        color: #DC2626;
    }

    /* ══════════════════════════
       CONTACT CARD
    ══════════════════════════ */
    .orbit-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: box-shadow 0.18s ease, transform 0.18s ease;
    }
    .orbit-card:hover {
        box-shadow: 0 4px 14px rgba(0,0,0,0.09);
        transform: translateY(-1px);
    }
    /* Avatar circle */
    .avatar {
        width: 42px; height: 42px;
        border-radius: 50%;
        background: linear-gradient(135deg, #DC2626, #7C3AED);
        display: flex; align-items: center; justify-content: center;
        font-size: 1rem; font-weight: 700; color: #ffffff;
        flex-shrink: 0;
    }
    .avatar-img {
        width: 42px; height: 42px;
        border-radius: 50%; object-fit: cover; flex-shrink: 0;
    }
    .card-header {
        display: flex; align-items: center; gap: 12px; margin-bottom: 10px;
    }
    .card-name {
        font-size: 0.9375rem; font-weight: 600;
        color: #111827 !important; margin: 0; line-height: 1.2;
    }
    .card-badge {
        display: inline-block; padding: 2px 9px;
        border-radius: 999px; font-size: 0.7rem; font-weight: 500;
        background-color: #FEE2E2; color: #DC2626; margin-top: 3px;
    }
    .fav-star { margin-left: auto; font-size: 0.875rem; color: #F59E0B; }
    .card-info {
        font-size: 0.8125rem; color: #4B5563 !important;
        line-height: 1.9; margin-bottom: 10px;
        border-top: 1px solid #F3F4F6; padding-top: 8px;
    }
    .card-info span { margin-right: 6px; }
    /* Health bar */
    .health-label {
        display: flex; justify-content: space-between;
        font-size: 0.7rem; color: #6B7280; margin-bottom: 3px;
    }
    .health-track {
        background: #E5E7EB; border-radius: 999px;
        height: 5px; width: 100%; margin-bottom: 12px;
    }
    .health-fill {
        height: 5px; border-radius: 999px;
        background: linear-gradient(90deg, #DC2626, #7C3AED);
    }

    /* ══════════════════════════
       SEARCH INPUT
    ══════════════════════════ */
    [data-testid="stTextInput"] input {
        border-radius: 8px;
        border: 1px solid #D1D5DB;
        background-color: #FFFFFF;
        color: #111827;
        font-size: 0.875rem;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #DC2626;
        box-shadow: 0 0 0 3px rgba(220,38,38,0.1);
    }

    /* ══════════════════════════
       EMPTY STATE
    ══════════════════════════ */
    .empty-state {
        text-align: center; padding: 3rem 2rem;
        background: #FFFFFF; border-radius: 12px;
        border: 1px dashed #D1D5DB; margin-top: 1rem;
    }
    .empty-state h3 { color: #374151 !important; font-size: 1.1rem; margin-bottom: 0.5rem; }
    .empty-state p  { color: #6B7280 !important; font-size: 0.875rem; }

    /* ══════════════════════════
       ROAST BOX
    ══════════════════════════ */
    .roast-box {
        background: #FFFBEB; border: 1px solid #FDE68A;
        border-radius: 8px; padding: 10px 14px;
        font-size: 0.825rem; color: #92400E !important; margin-top: 6px;
    }

    /* ══════════════════════════
       DIVIDERS & MISC
    ══════════════════════════ */
    hr { border-color: #E5E7EB; }

    /* Streamlit info/success/error banners — keep readable */
    .stAlert { border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

# Pre-built palette for avatar gradient variety
AVATAR_GRADIENTS = [
    ("135deg,#6366F1,#8B5CF6"),
    ("135deg,#0EA5E9,#6366F1"),
    ("135deg,#10B981,#0EA5E9"),
    ("135deg,#F59E0B,#EF4444"),
    ("135deg,#EC4899,#8B5CF6"),
]

ROASTS = [
    "I'd agree with you, but then we'd both be wrong.",
    "You're like a software update — whenever I see you I think 'not now'.",
    "You bring everyone so much joy… when you leave the room.",
    "You're proof that evolution can go in reverse.",
    "If laughter is the best medicine, your face must be curing the world.",
    "I'd roast you harder, but my mom said I'm not allowed to burn trash.",
    "You have the energy of someone who puts the milk in before the cereal.",
    "I'd say you're one in a million, but I've met you before.",
]


def process_image(uploaded_file):
    """Compress and encode uploaded image as base64 JPEG."""
    if uploaded_file:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            img.thumbnail((200, 200))
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=80)
            return base64.b64encode(buf.getvalue()).decode()
        except Exception as e:
            st.error(f"Image error: {e}")
    return None


def avatar_html(name, b64_img=None, contact_id=0):
    """Return HTML for an avatar circle or image."""
    if b64_img:
        return f'<img class="avatar-img" src="data:image/jpeg;base64,{b64_img}" />'
    initial = name[0].upper() if name else "?"
    grad = AVATAR_GRADIENTS[contact_id % len(AVATAR_GRADIENTS)]
    return f'<div class="avatar" style="background:linear-gradient({grad});">{initial}</div>'


def health_bar_html(score):
    """Return an inline SVG-style health bar."""
    score = max(0, min(100, score or 0))
    return f"""
    <div class="health-label"><span>Relationship Health</span><span>{score}%</span></div>
    <div class="health-track"><div class="health-fill" style="width:{score}%;"></div></div>
    """


def category_color(cat):
    colors = {
        "Work":       ("#EEF2FF", "#4F46E5"),
        "Family":     ("#FEF3C7", "#D97706"),
        "Friends":    ("#ECFDF5", "#059669"),
        "Networking": ("#F0F9FF", "#0284C7"),
        "Other":      ("#F1F5F9", "#64748B"),
    }
    return colors.get(cat, ("#F1F5F9", "#64748B"))


def build_card_html(contact):
    """Build the static (non-interactive) part of a contact card."""
    bg, fg = category_color(contact.get("category") or "Other")
    cat_label = contact.get("category") or "Uncategorized"
    fav_star = "★" if contact.get("is_favorite") else ""
    phone = contact.get("phone") or "—"
    email = contact.get("email") or "—"
    av = avatar_html(contact["name"], contact.get("profile_image"), contact.get("id", 0))
    hbar = health_bar_html(contact.get("health_score", 50))

    return f"""
    <div class="orbit-card">
        <div class="card-header">
            {av}
            <div style="flex:1; min-width:0;">
                <div class="card-name">{contact['name']}
                    <span class="fav-star">{fav_star}</span>
                </div>
                <span class="card-badge" style="background:{bg};color:{fg};">{cat_label}</span>
            </div>
        </div>
        <div class="card-info">
            <span>📞</span> {phone}<br/>
            <span>✉️</span> {email}
        </div>
        {hbar}
    </div>
    """


# ─────────────────────────────────────────────
# Session State defaults
# ─────────────────────────────────────────────
for key, default in {
    "current_view": "dashboard",
    "edit_contact_id": None,
    "search_query": "",
    "view_mode": "Cards",
    "roast_id": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def set_view(view, contact_id=None):
    st.session_state.current_view = view
    st.session_state.edit_contact_id = contact_id
    st.session_state.roast_id = None


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Branding
        st.markdown("""
        <div style="padding:8px 0 16px;">
            <div style="font-size:1.35rem;font-weight:700;color:#0F172A;">🪐 Orbit</div>
            <div style="font-size:0.8rem;color:#64748B;margin-top:2px;">Your minimal contact hub</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        # Navigation
        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:#94A3B8;letter-spacing:.06em;margin-bottom:6px;">NAVIGATION</div>', unsafe_allow_html=True)

        dash_type = "primary" if st.session_state.current_view == "dashboard" else "secondary"
        add_type  = "primary" if st.session_state.current_view in ("add", "edit") else "secondary"

        if st.button("📋  Dashboard", use_container_width=True, type=dash_type, key="nav_dash"):
            set_view("dashboard"); st.rerun()

        if st.button("➕  Add Contact", use_container_width=True, type=add_type, key="nav_add"):
            set_view("add"); st.rerun()

        st.divider()

        # Quick stats
        all_contacts = get_all_contacts()
        total = len(all_contacts)
        favs  = sum(1 for c in all_contacts if c.get("is_favorite"))
        st.markdown(f"""
        <div style="display:flex;gap:12px;margin-bottom:16px;">
            <div style="flex:1;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:1.25rem;font-weight:700;color:#4F46E5;">{total}</div>
                <div style="font-size:0.7rem;color:#94A3B8;">Contacts</div>
            </div>
            <div style="flex:1;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:1.25rem;font-weight:700;color:#F59E0B;">⭐{favs}</div>
                <div style="font-size:0.7rem;color:#94A3B8;">Favorites</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:#94A3B8;letter-spacing:.06em;margin-bottom:6px;">TOOLS</div>', unsafe_allow_html=True)

        if st.button("🎲  Generate Sample Data", use_container_width=True, key="gen_data"):
            with st.spinner("Generating 8 contacts…"):
                generate_sample_contacts(8)
            st.toast("8 sample contacts added!", icon="✅")
            st.rerun()


# ─────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────
def render_empty_state():
    st.markdown("""
    <div class="empty-state">
        <div style="font-size:2.5rem;margin-bottom:12px;">🪐</div>
        <h3>No contacts yet</h3>
        <p>Add your first contact or generate sample data from the sidebar.</p>
    </div>
    """, unsafe_allow_html=True)
    col = st.columns([2, 1, 2])[1]
    with col:
        if st.button("➕ Add Contact", type="primary", use_container_width=True, key="empty_add"):
            set_view("add"); st.rerun()


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
def render_dashboard():
    # Page header
    col_title, col_mode = st.columns([3, 1])
    with col_title:
        st.markdown("## Contacts")
    with col_mode:
        mode = st.radio("View mode", ["Cards", "Table"], horizontal=True, key="view_radio", label_visibility="collapsed")
        st.session_state.view_mode = mode

    # Search bar
    search = st.text_input(
        label="search",
        value=st.session_state.search_query,
        placeholder="🔍  Search by name or phone…",
        label_visibility="collapsed",
        key="search_input"
    )
    if search != st.session_state.search_query:
        st.session_state.search_query = search
        st.rerun()

    # Fetch
    contacts = search_contacts(search) if search else get_all_contacts()

    if not contacts:
        if search:
            st.info("No contacts match your search.")
        else:
            render_empty_state()
        return

    st.caption(f"{len(contacts)} contact{'s' if len(contacts) != 1 else ''} found")

    # ── TABLE VIEW ──────────────────────────────
    if st.session_state.view_mode == "Table":
        df = pd.DataFrame(contacts)
        cols_to_show = ['name', 'phone', 'email', 'category', 'health_score', 'is_favorite', 'follow_up_date']
        df_display = df[[c for c in cols_to_show if c in df.columns]].copy()
        df_display['is_favorite'] = df_display['is_favorite'].apply(lambda x: "⭐ Yes" if x else "No")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        return

    # ── CARD VIEW ────────────────────────────────
    # Render 3 columns; each card is fully contained within its column
    grid = st.columns(3)
    for idx, contact in enumerate(contacts):
        col = grid[idx % 3]
        with col:
            # Static HTML card (avatar, badge, info, health bar)
            st.markdown(build_card_html(contact), unsafe_allow_html=True)

            # Action buttons immediately after the card — still inside the same column
            b1, b2, b3, b4 = st.columns(4)

            with b1:
                if st.button("✏️ Edit", key=f"edit_{contact['id']}", use_container_width=True):
                    set_view("edit", contact["id"]); st.rerun()

            with b2:
                if st.button("🗑️ Del", key=f"del_{contact['id']}", use_container_width=True):
                    delete_contact(contact["id"])
                    st.toast(f"Deleted {contact['name']}", icon="🗑️")
                    st.rerun()

            with b3:
                fav_label = "★ Unfav" if contact["is_favorite"] else "☆ Fav"
                if st.button(fav_label, key=f"fav_{contact['id']}", use_container_width=True):
                    toggle_favorite(contact["id"], contact["is_favorite"]); st.rerun()

            with b4:
                if st.button("🔥 Roast", key=f"roast_{contact['id']}", use_container_width=True):
                    st.session_state.roast_id = contact["id"] if st.session_state.roast_id != contact["id"] else None

            # Roast output inline
            if st.session_state.roast_id == contact["id"]:
                roast_text = random.choice(ROASTS)
                st.markdown(f'<div class="roast-box">🔥 <b>Roast for {contact["name"]}:</b><br/>{roast_text}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ADD / EDIT FORM
# ─────────────────────────────────────────────
def render_contact_form(contact=None):
    # Ensure contact is always a dict — never None — for safe .get() access
    if not isinstance(contact, dict):
        contact = {}
    is_edit = bool(contact.get("id"))
    st.markdown(f"## {'Edit Contact' if is_edit else 'New Contact'}")

    if st.button("← Back", key="back_btn"):
        set_view("dashboard"); st.rerun()

    st.divider()

    with st.form("contact_form", clear_on_submit=not is_edit):
        left, right = st.columns([1, 2])

        with left:
            if is_edit and contact.get("profile_image"):
                av = avatar_html(contact["name"], contact["profile_image"], contact.get("id", 0))
                st.markdown(f'<div style="margin-bottom:12px;">{av}</div>', unsafe_allow_html=True)
            uploaded_image = st.file_uploader("Profile Photo", type=["jpg", "jpeg", "png"])

            is_favorite = st.checkbox(
                "★ Mark as Favorite",
                value=bool(contact.get("is_favorite", False))
            )
            health_score = st.slider(
                "Health Score",
                0, 100,
                int(contact.get("health_score", 50))
            )

        with right:
            name = st.text_input("Full Name *", value=contact.get("name", ""))
            c1, c2 = st.columns(2)
            with c1:
                phone = st.text_input("Phone", value=contact.get("phone", "") or "")
                cats = ["Work", "Family", "Friends", "Networking", "Other"]
                cat_val = contact.get("category") or "Other"
                cat_idx = cats.index(cat_val) if cat_val in cats else 4
                category = st.selectbox("Category", cats, index=cat_idx)
            with c2:
                email = st.text_input("Email", value=contact.get("email", "") or "")
                existing_date = None
                if is_edit and contact.get("follow_up_date"):
                    try:
                        existing_date = datetime.datetime.strptime(contact["follow_up_date"], "%Y-%m-%d").date()
                    except ValueError:
                        pass
                follow_up = st.date_input("Follow-up Date", value=existing_date)

            address = st.text_area("Address", value=contact.get("address", "") or "", height=80)
            notes   = st.text_area("Notes",   value=contact.get("notes",   "") or "", height=80)

        submitted = st.form_submit_button("💾  Save Contact", type="primary", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Name is required.")
            else:
                img_str = (
                    process_image(uploaded_image)
                    if uploaded_image
                    else (contact.get("profile_image") if is_edit else None)
                )
                data = {
                    "name":          name.strip(),
                    "phone":         phone.strip(),
                    "email":         email.strip(),
                    "address":       address.strip(),
                    "notes":         notes.strip(),
                    "follow_up_date": str(follow_up) if follow_up else None,
                    "category":      category,
                    "health_score":  health_score,
                    "is_favorite":   is_favorite,
                    "profile_image": img_str,
                }
                if is_edit:
                    update_contact(contact["id"], data)
                    st.success("Contact updated!")
                else:
                    add_contact(data)
                    st.success("Contact added!")
                set_view("dashboard")
                st.rerun()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    load_css()
    render_sidebar()

    view = st.session_state.current_view

    if view == "dashboard":
        render_dashboard()
    elif view == "add":
        render_contact_form()
    elif view == "edit":
        cid = st.session_state.edit_contact_id
        if cid:
            c = get_contact_by_id(cid)
            if c:
                render_contact_form(c)
            else:
                st.error("Contact not found.")
                set_view("dashboard"); st.rerun()
        else:
            set_view("dashboard"); st.rerun()


if __name__ == "__main__":
    main()
