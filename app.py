import streamlit as st

st.set_page_config(page_title="Digital Community Vault")

st.title("Digital Community Vault")
st.write(
    """Welcome to the Digital Community Vault. This platform enables regenerative, land-based
communities to share resources, skills, goods, and services across a decentralized network.
Use the search box below to find communities by name or location."""
)

search_query = st.text_input("Search communities by name or location")

communities = [
    {
        "name": "Green Meadows Collective",
        "location": "Oregon, USA",
        "description": "A permaculture community cultivating organic produce and hosting learning events.",
        "offers": ["Organic vegetables", "Permaculture workshops", "Farm stays"],
        "seeks": ["Seeds", "Volunteer builders", "Gardening tools"],
    },
    {
        "name": "Sunrise Ecovillage",
        "location": "New South Wales, Australia",
        "description": "Off‑grid community focused on renewable energy and holistic living.",
        "offers": ["Solar power expertise", "Community gatherings"],
        "seeks": ["Permaculture experts", "Solar equipment"],
    },
    {
        "name": "Riverstone Homestead",
        "location": "British Columbia, Canada",
        "description": "Family‑run homestead sharing knowledge on natural building and herbal medicine.",
        "offers": ["Herbal tinctures", "Natural building courses"],
        "seeks": ["Apprentices", "Building materials"],
    },
]

if search_query:
    filtered = [
        c
        for c in communities
        if search_query.lower() in c["name"].lower()
        or search_query.lower() in c["location"].lower()
    ]
else:
    filtered = communities

for comm in filtered:
    st.markdown("---")
    st.markdown(f"### {comm['name']}")
    st.markdown(f"**Location:** {comm['location']}")
    st.write(comm["description"])

    st.markdown("**What We Offer**")
    for offer in comm["offers"]:
        st.markdown(f"- {offer}")

    st.markdown("**What We Seek**")
    for seek in comm["seeks"]:
        st.markdown(f"- {seek}")

st.markdown("---")
