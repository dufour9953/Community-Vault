import json
from pathlib import Path
import streamlit as st

DATA_FILE = Path("communities.json")

SAMPLE_COMMUNITIES = [
    {
        "name": "Green Meadows Collective",
        "location": "Oregon, USA",
        "description": "A permaculture community cultivating organic produce and hosting learning events.",
        "offers": ["Organic vegetables", "Permaculture workshops", "Farm stays"],
        "needs": ["Seeds", "Volunteer builders", "Gardening tools"],
    },
    {
        "name": "Sunrise Ecovillage",
        "location": "New South Wales, Australia",
        "description": "Off-grid community focused on renewable energy and holistic living.",
        "offers": ["Solar power expertise", "Community gatherings"],
        "needs": ["Permaculture experts", "Solar equipment"],
    },
    {
        "name": "Riverstone Homestead",
        "location": "British Columbia, Canada",
        "description": "Family-run homestead sharing knowledge on natural building and herbal medicine.",
        "offers": ["Herbal tinctures", "Natural building courses"],
        "needs": ["Apprentices", "Building materials"],
    },
]

def load_communities() -> list:
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return SAMPLE_COMMUNITIES.copy()

def save_communities(data):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

st.set_page_config(page_title="Digital Community Vault", page_icon="🌱", layout="wide")

st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] { flex-wrap: wrap; }
    ul { padding-left: 1.2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

TAGLINES = [
    "Your local farmers market, in your pocket",
    "Connecting regenerative communities worldwide",
    "Sharing skills and abundance together",
]
if "tagline_index" not in st.session_state:
    st.session_state.tagline_index = 0

tabs = st.tabs(["🏠 Home", "📖 Directory", "➕ Submit", "🌍 About"])
home_tab, dir_tab, submit_tab, about_tab = tabs

communities = load_communities()

with home_tab:
    st.title("Digital Community Vault")
    tagline = TAGLINES[st.session_state.tagline_index % len(TAGLINES)]
    st.session_state.tagline_index = (st.session_state.tagline_index + 1) % len(TAGLINES)
    st.markdown(f"### *{tagline}*")
    st.write(
        """
Welcome to the Digital Community Vault. This platform enables regenerative, land-based communities to share resources, skills, goods and services across a decentralized network. Use the directory to discover hubs around the world or submit your community to get involved.
        """
    )

with dir_tab:
    st.header("Community Directory")
    query = st.text_input("Search by name or location")
    results = [
        c for c in communities
        if query.lower() in c["name"].lower() or query.lower() in c["location"].lower()
    ] if query else communities

    for comm in results:
        card = f"""
        <div style='background-color:#ffffff;border-radius:8px;padding:1rem;margin-bottom:1rem;box-shadow:0 1px 3px rgba(0,0,0,0.1);'>
            <h3 style='margin-bottom:0;'>{comm['name']}</h3>
            <p style='color:#1f8a70;font-weight:600;margin:0;'>{comm['location']}</p>
            <p>{comm['description']}</p>
            <h4>🌿 What We Offer</h4>
            <ul>{"".join(f"<li>{o}</li>" for o in comm["offers"])}</ul>
            <h4>🙌 What We Seek</h4>
            <ul>{"".join(f"<li>{n}</li>" for n in comm["needs"])}</ul>
        </div>
        """
        st.markdown(card, unsafe_allow_html=True)

with submit_tab:
    st.header("Submit a New Community")
    with st.form("submit_form"):
        name = st.text_input("Name")
        location = st.text_input("Location")
        description = st.text_area("Description")
        offers_text = st.text_area("Offers (one per line)")
        needs_text = st.text_area("Needs (one per line)")
        submitted = st.form_submit_button("Add Community")

    if submitted and name and location:
        new_community = {
            "name": name,
            "location": location,
            "description": description,
            "offers": [o.strip() for o in offers_text.splitlines() if o.strip()],
            "needs": [n.strip() for n in needs_text.splitlines() if n.strip()],
        }
        communities.append(new_community)
        save_communities(communities)
        st.success("Community added!")

with about_tab:
    st.header("About the Digital Community Vault")
    st.write(
        """
The Digital Community Vault is a grassroots project inspired by the vision of a decentralized network of healing hubs. Like a mycelial web, we aim to connect communities that share ecological and spiritual values. Future iterations may include tokenized exchange, member profiles, and integrated DAO governance.
        """
    )