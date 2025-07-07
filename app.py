import json
import streamlit as st
from pathlib import Path

DATA_FILE = Path("communities.json")

def load_communities():
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_communities(data):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# --- Page Setup ---
st.set_page_config(page_title="Digital Community Vault", page_icon="🌱")

# Tagline rotation
TAGLINES = [
    "Your local farmers market, in your pocket",
    "Connecting regenerative communities worldwide",
    "Sharing skills and abundance together",
]
if "tagline_index" not in st.session_state:
    st.session_state.tagline_index = 0

# Navigation
tab = st.sidebar.radio(
    "Navigation",
    ("Home", "Community Directory", "Submit a Community", "About / Vision", "Dashboard"),
)

# Load data
communities = load_communities()

# --- Home ---
if tab == "Home":
    st.title("Digital Community Vault")
    tagline = TAGLINES[st.session_state.tagline_index % len(TAGLINES)]
    st.session_state.tagline_index += 1
    st.write(f"*{tagline}*")
    st.write("""
Welcome to the Digital Community Vault. This platform enables regenerative, land-based communities to share resources, skills, goods and services across a decentralized network.
Use the directory to discover hubs around the world or submit your community to get involved.
    """)

# --- Directory ---
elif tab == "Community Directory":
    st.header("Community Directory")
    query = st.text_input("Search by name or location")
    if query:
        results = [c for c in communities if query.lower() in c["name"].lower() or query.lower() in c["location"].lower()]
    else:
        results = communities

    for comm in results:
        st.markdown("---")
        st.subheader(comm["name"])
        st.markdown(f"**Location:** {comm['location']}")
        st.write(comm["description"])

        st.markdown("**What We Offer**")
        for item in comm["offers"]:
            st.markdown(f"- {item}")

        st.markdown("**What We Seek**")
        for item in comm["needs"]:
            st.markdown(f"- {item}")

# --- Submit Form ---
elif tab == "Submit a Community":
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

# --- About ---
elif tab == "About / Vision":
    st.header("About the Digital Community Vault")
    st.write("""
The Digital Community Vault is a grassroots project inspired by the vision of a decentralized network of healing hubs. Like a mycelial web, we aim to connect communities that share ecological and spiritual values. Future iterations may include tokenized exchange, member profiles, and integrated DAO governance.
    """)

# --- Placeholder Dashboard ---
else:
    st.header("Community Dashboard")
    st.write("This section will host future features such as user profiles and exchanges.")