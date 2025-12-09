import os
import uuid
import base64
from datetime import datetime

import streamlit as st
from PIL import Image
import requests
from openai import OpenAI

import config
from animal_data import (
    ANIMAL_CATEGORIES,
    ANIMALS_DATA,
    get_animals_by_category,
    get_animal_detail
)

# ------------------------------------
# Page config
# ------------------------------------
st.set_page_config(
    page_title="Global Animal Explorer",
    page_icon="🐾",
    layout="wide"
)

# ------------------------------------
# Helpers
# ------------------------------------
def allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in config.ALLOWED_EXTENSIONS


def read_image_as_data_url(uploaded_file) -> str:
    raw = uploaded_file.getvalue()
    b64 = base64.b64encode(raw).decode("utf-8")

    ext = uploaded_file.name.rsplit(".", 1)[1].lower() if "." in uploaded_file.name else "jpeg"
    mime = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "gif": "image/gif",
        "bmp": "image/bmp",
    }.get(ext, "image/jpeg")

    return f"data:{mime};base64,{b64}"


def get_dashscope_api_key() -> str:
    key = st.session_state.get("runtime_dashscope_key", "").strip()
    if key:
        return key

    try:
        if "DASHSCOPE_API_KEY" in st.secrets:
            sec = str(st.secrets["DASHSCOPE_API_KEY"]).strip()
            if sec:
                return sec
    except Exception:
        pass

    return (config.DASHSCOPE_API_KEY or "").strip()


def build_openai_client():
    key = get_dashscope_api_key()
    if not key:
        return None
    return OpenAI(api_key=key, base_url=config.DASHSCOPE_BASE_URL)

# ------------------------------------
# GBIF
# ------------------------------------
@st.cache_data(ttl=60 * 60)
def gbif_species_search(query: str, limit: int = 10):
    url = "https://api.gbif.org/v1/species/search"
    params = {"q": query, "limit": limit}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("results", [])

# ------------------------------------
# Local name matching
# ------------------------------------
def normalize(s: str) -> str:
    return (s or "").strip().lower()


def local_name_search(query: str):
    q = normalize(query)
    if not q:
        return []

    hits = []
    for animal_id, a in ANIMALS_DATA.items():
        fields = [
            a.get("name", ""),
            a.get("scientific_name", ""),
            *a.get("aliases", []),
        ]
        fields_norm = [normalize(x) for x in fields if x]

        # exact or contains match
        if any(q == f for f in fields_norm) or any(q in f for f in fields_norm):
            hits.append((animal_id, a))

    return hits

# ------------------------------------
# Vision (cloud-only, optional)
# ------------------------------------
def identify_animal_cloud(image_url: str) -> str:
    client = build_openai_client()
    if client is None:
        return (
            "Cloud vision is not enabled.\n\n"
            "To identify images with high accuracy (e.g., ferret-level detail), "
            "add a valid DashScope Model Studio API key in Streamlit Secrets "
            "or paste it in the sidebar."
        )

    prompt = (
        "You are an expert wildlife identifier.\n"
        "Carefully analyze the image.\n\n"
        "If an animal is present, produce an ambiguity-aware identification.\n"
        "Return the following format in English:\n\n"
        "Top candidates:\n"
        "1) <Common name> (<scientific name if possible>) — <confidence %>\n"
        "2) <Common name> (<scientific name if possible>) — <confidence %>\n"
        "3) <Common name> (<scientific name if possible>) — <confidence %>\n\n"
        "Rules:\n"
        "- Confidence values should be reasonable and sum to about 100%.\n"
        "- If the animal is very clear, you may provide 1 dominant candidate and 1 minor alternative.\n"
        "- Explicitly handle common look-alike groups:\n"
        "  octopus/squid/cuttlefish, sea otter/river otter,\n"
        "  raccoon/red panda, sea lion/seal/walrus.\n\n"
        "Then provide:\n"
        "• Key visual cues used\n"
        "• Short natural history notes (habitat, behavior)\n"
        "• One interesting fact\n\n"
        "If no animal is present, briefly describe the main content."
    )

    completion = client.chat.completions.create(
        model=config.QWEN_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    return completion.choices[0].message.content

# ------------------------------------
# UI Pages
# ------------------------------------
def render_home():
    st.title("🐾 Global Animal Explorer")

    st.markdown(
        """
This project is designed for GitHub + Streamlit Cloud.

- **Featured Encyclopedia** provides curated examples by category.
- **Global Encyclopedia (GBIF)** covers millions of species worldwide.
- **Animal Name Tester** lets you verify animal names without any API key.
- **Image Identifier** is optional and requires a valid DashScope Model Studio API key for high accuracy.
"""
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Featured animals (local)", len(ANIMALS_DATA))
    with c2:
        st.metric("Global coverage", "Millions (GBIF)")
    with c3:
        st.metric("Image upload", "Up to 16 MB")


def render_featured_categories():
    st.title("🗂️ Featured Animal Categories")
    st.caption("Curated examples to help you explore major animal groups.")

    cols = st.columns(3)
    i = 0
    for cat_id, info in ANIMAL_CATEGORIES.items():
        featured_count = len(get_animals_by_category(cat_id))

        with cols[i % 3]:
            st.markdown(f"### {info.get('name', cat_id.title())}")
            st.write(info.get("description", ""))
            st.write(f"Estimated species count worldwide: **{info.get('count', 'N/A')}**")
            st.write(f"Featured examples here: **{featured_count}**")

            if st.button(f"Open {info.get('name', cat_id.title())}", key=f"open_{cat_id}"):
                st.session_state["page"] = "featured_category"
                st.session_state["category_id"] = cat_id
        i += 1


def render_featured_category_detail(category_id: str):
    if category_id not in ANIMAL_CATEGORIES:
        st.error("Category not found.")
        return

    info = ANIMAL_CATEGORIES[category_id]
    animals = get_animals_by_category(category_id)

    st.title(f"📌 {info.get('name', category_id.title())}")
    st.write(info.get("description", ""))

    if not animals:
        st.info("No featured animals in this category yet.")
        return

    st.markdown("### Featured animals")
    animal_items = list(animals.items())
    cols = st.columns(3)

    for idx, (animal_id, animal) in enumerate(animal_items):
        with cols[idx % 3]:
            st.markdown(f"#### {animal.get('name', animal_id)}")
            if animal.get("image"):
                st.image(animal["image"], use_container_width=True)

            if animal.get("scientific_name"):
                st.caption(animal["scientific_name"])

            short = animal.get("description", "")
            if short:
                st.write(short[:140] + ("..." if len(short) > 140 else ""))

            if st.button("View details", key=f"feat_detail_{animal_id}"):
                st.session_state["page"] = "featured_animal"
                st.session_state["animal_id"] = animal_id


def render_featured_animal_detail(animal_id: str):
    animal = get_animal_detail(animal_id)
    if not animal:
        st.error("Animal not found.")
        return

    category_info = ANIMAL_CATEGORIES.get(animal.get("category", ""), {})

    st.title(f"🦁 {animal.get('name', animal_id)}")
    if animal.get("scientific_name"):
        st.caption(animal["scientific_name"])

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        if animal.get("image"):
            st.image(animal["image"], use_container_width=True)

        st.markdown(f"**Category:** {category_info.get('name', animal.get('category', ''))}")
        st.markdown(f"**Conservation status:** {animal.get('conservation_status', 'N/A')}")
        st.markdown(f"**Habitat:** {animal.get('habitat', 'N/A')}")
        st.markdown(f"**Distribution:** {animal.get('distribution', 'N/A')}")
        st.markdown(f"**Population:** {animal.get('population', 'N/A')}")

    with col2:
        st.markdown("### Overview")
        st.write(animal.get("description", ""))

        if animal.get("aliases"):
            st.markdown("### Known aliases")
            st.write(", ".join(animal["aliases"]))


def render_global_encyclopedia():
    st.title("🌍 Global Animal Encyclopedia (GBIF)")

    query = st.text_input(
        "Search by common name or scientific name",
        placeholder="e.g., snowy owl, Bubo scandiacus, ferret"
    )

    limit = st.slider("Max results", 5, 20, 10)

    if not query:
        st.info("Type a name to start searching.")
        return

    try:
        with st.spinner("Searching GBIF..."):
            results = gbif_species_search(query, limit=limit)

        if not results:
            st.warning("No results found. Try a different keyword.")
            return

        st.markdown("### Search results")
        for r in results[:limit]:
            canonical = r.get("canonicalName") or r.get("scientificName", "Unknown")
            rank = r.get("rank", "N/A")
            kingdom = r.get("kingdom", "N/A")
            family = r.get("family", "")
            genus = r.get("genus", "")

            with st.expander(f"{canonical}  •  {rank}  •  {kingdom}", expanded=False):
                if family:
                    st.write(f"**Family:** {family}")
                if genus:
                    st.write(f"**Genus:** {genus}")
                st.json(r)

    except Exception as e:
        st.error(f"Global search failed: {e}")


def render_name_tester():
    st.title("✅ Animal Name Tester")
    st.markdown(
        """
Test whether an animal name can be recognized.

This tool works **without any API key**:
1) Checks the **local Featured database** (supports aliases and some Chinese common names).
2) Verifies results using **GBIF global database**.
"""
    )

    query = st.text_input(
        "Enter an animal name (English / scientific name / alias)",
        placeholder="Try: Snowy Owl / Bubo scandiacus / 雪鸮 / 雪雕 / Ferret / 雪貂"
    )

    if not query:
        st.info("Type a name to test.")
        return

    # Local hits
    local_hits = local_name_search(query)

    st.markdown("### Local Featured matches")
    if not local_hits:
        st.write("No local featured match found.")
    else:
        for animal_id, a in local_hits:
            st.success(f"{a.get('name')} — {a.get('scientific_name')}")
            if a.get("image"):
                st.image(a["image"], width=260)
            st.caption(f"Category: {a.get('category')}")
            if a.get("aliases"):
                st.caption(f"Aliases: {', '.join(a['aliases'])}")

    # GBIF verify
    st.markdown("### GBIF global verification")
    try:
        with st.spinner("Searching GBIF..."):
            results = gbif_species_search(query, limit=5)

        if not results:
            st.warning("GBIF: No results found for this query.")
        else:
            for r in results:
                canonical = r.get("canonicalName") or r.get("scientificName", "Unknown")
                st.write(f"- **{canonical}** • {r.get('rank','N/A')} • {r.get('kingdom','N/A')}")
    except Exception as e:
        st.error(f"GBIF lookup failed: {e}")


def render_identifier():
    st.title("🧠 Image Animal Identifier (Cloud Vision Optional)")
    st.markdown(
        """
For high-accuracy image identification (species-level, look-alike confidence),
you need a **valid DashScope Model Studio API key**.

If you only want to test animal names, use **Animal Name Tester** instead.
"""
    )

    uploaded = st.file_uploader(
        "Upload an image",
        type=list(config.ALLOWED_EXTENSIONS),
        accept_multiple_files=False
    )

    if not uploaded:
        return

    if not allowed_file(uploaded.name):
        st.error("Unsupported file type.")
        return

    image = Image.open(uploaded)
    st.image(image, caption="Uploaded image", use_container_width=True)

    image_url = read_image_as_data_url(uploaded)

    with st.spinner("Identifying with cloud model..."):
        result_text = identify_animal_cloud(image_url)

    st.markdown("### Result")
    st.write(result_text)

# ------------------------------------
# Sidebar & routing
# ------------------------------------
def ensure_state():
    st.session_state.setdefault("page", "home")
    st.session_state.setdefault("category_id", None)
    st.session_state.setdefault("animal_id", None)


def sidebar_nav():
    st.sidebar.title("Navigation")

    if st.sidebar.button("🏠 Home"):
        st.session_state["page"] = "home"
    if st.sidebar.button("⭐ Featured Encyclopedia"):
        st.session_state["page"] = "featured_categories"
    if st.sidebar.button("✅ Animal Name Tester"):
        st.session_state["page"] = "name_tester"
    if st.sidebar.button("🌍 Global Encyclopedia (GBIF)"):
        st.session_state["page"] = "global"
    if st.sidebar.button("🧠 Image Identifier"):
        st.session_state["page"] = "identify"

    st.sidebar.markdown("---")


def render_sidebar_key_box():
    st.sidebar.markdown("### 🔑 Optional Key (for image ID)")

    st.sidebar.text_input(
        "DashScope API Key",
        type="password",
        key="runtime_dashscope_key",
        help="Optional. Required only for high-accuracy image identification."
    )

    if get_dashscope_api_key():
        st.sidebar.success("Cloud vision key detected.")
    else:
        st.sidebar.info("No key set. Image ID will show guidance.")


def main():
    ensure_state()
    sidebar_nav()
    render_sidebar_key_box()

    page = st.session_state["page"]

    if page == "home":
        render_home()
    elif page == "featured_categories":
        render_featured_categories()
    elif page == "featured_category":
        render_featured_category_detail(st.session_state.get("category_id"))
    elif page == "featured_animal":
        render_featured_animal_detail(st.session_state.get("animal_id"))
    elif page == "name_tester":
        render_name_tester()
    elif page == "global":
        render_global_encyclopedia()
    elif page == "identify":
        render_identifier()
    else:
        render_home()


if __name__ == "__main__":
    main()
