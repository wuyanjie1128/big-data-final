import os
import re
import base64
import uuid
from pathlib import Path

import streamlit as st
import requests
import numpy as np
from PIL import Image

import onnxruntime as ort

import config
from animal_data import ANIMAL_CATEGORIES, ANIMALS_DATA, get_animals_by_category, get_animal_detail


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Global Animal Explorer",
    page_icon="🐾",
    layout="wide"
)


# -----------------------------
# Utility
# -----------------------------
def allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in config.ALLOWED_EXTENSIONS


def normalize(s: str) -> str:
    return (s or "").strip().lower()


def is_ascii_text(s: str) -> bool:
    try:
        s.encode("ascii")
        return True
    except Exception:
        return False


def safe_aliases_for_display(aliases):
    # Do not display non-English aliases to ensure zero Chinese in UI
    return [a for a in (aliases or []) if is_ascii_text(a)]


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


# -----------------------------
# GBIF (Global)
# -----------------------------
@st.cache_data(ttl=60 * 60)
def gbif_species_search(query: str, limit: int = 10):
    url = "https://api.gbif.org/v1/species/search"
    params = {"q": query, "limit": limit}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("results", [])


@st.cache_data(ttl=60 * 60)
def gbif_species_match(name: str):
    url = "https://api.gbif.org/v1/species/match"
    params = {"name": name, "verbose": "true"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()


# -----------------------------
# Local name search (Featured)
# -----------------------------
def local_name_search(query: str):
    q = normalize(query)
    if not q:
        return []

    hits = []
    for animal_id, a in ANIMALS_DATA.items():
        fields = [
            a.get("name", ""),
            a.get("scientific_name", ""),
            *(a.get("aliases", []) or []),
        ]
        fields_norm = [normalize(x) for x in fields if x]

        if any(q == f for f in fields_norm) or any(q in f for f in fields_norm):
            hits.append((animal_id, a))
    return hits


# -----------------------------
# No-key ImageNet classifier via ONNX
# -----------------------------
MODEL_DIR = Path(".cache/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Public model/labels sources.
# ONNX Model Zoo stopped LFS availability after July 1, 2025,
# so we use Hugging Face public hosting instead. :contentReference[oaicite:2]{index=2}
MOBILENET_ONNX_URL = (
    "https://huggingface.co/qualcomm/MobileNet-v2/resolve/main/MobileNet-v2.onnx"
)
IMAGENET_LABELS_URL = (
    "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
)  # common labels source used in ORT tutorials. :contentReference[oaicite:3]{index=3}

MODEL_PATH = MODEL_DIR / "mobilenet_v2.onnx"
LABELS_PATH = MODEL_DIR / "imagenet_classes.txt"


def download_file(url: str, path: Path):
    if path.exists() and path.stat().st_size > 0:
        return
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    path.write_bytes(r.content)


@st.cache_resource
def load_onnx_session():
    try:
        download_file(MOBILENET_ONNX_URL, MODEL_PATH)
        sess = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
        return sess
    except Exception:
        return None


@st.cache_resource
def load_imagenet_labels():
    try:
        download_file(IMAGENET_LABELS_URL, LABELS_PATH)
        labels = LABELS_PATH.read_text(encoding="utf-8").splitlines()
        return labels
    except Exception:
        return []


def preprocess_imagenet(pil_image: Image.Image) -> np.ndarray:
    # MobileNetV2 ImageNet preprocessing
    img = pil_image.convert("RGB").resize((224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    # Normalize to ImageNet mean/std
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    arr = (arr - mean) / std
    arr = np.transpose(arr, (2, 0, 1))  # CHW
    arr = np.expand_dims(arr, axis=0)   # NCHW
    return arr


def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)


def imagenet_classify(pil_image: Image.Image, topk: int = 5):
    sess = load_onnx_session()
    labels = load_imagenet_labels()
    if sess is None or not labels:
        return []

    inp = preprocess_imagenet(pil_image)
    input_name = sess.get_inputs()[0].name
    out = sess.run(None, {input_name: inp})[0][0]
    probs = softmax(out)

    idxs = np.argsort(probs)[::-1][:topk]
    results = []
    for i in idxs:
        label = labels[i] if i < len(labels) else f"class_{i}"
        results.append((label, float(probs[i])))
    return results


def map_imagenet_to_featured(label: str):
    l = normalize(label)
    # Very small heuristic mapping for better UX
    mappings = {
        "snowy owl": "snowy_owl",
        "great white shark": "great_white_shark",
        "tiger": "tiger",
        "lion": "lion",
        "giant panda": "giant_panda",
        "red panda": "red_panda",
        "raccoon": "raccoon",
        "monarch butterfly": "monarch_butterfly",
        "crocodile": "nile_crocodile",
        "komodo dragon": "komodo_dragon",
    }
    for k, v in mappings.items():
        if k in l:
            return v
    return None


def render_imagenet_result_block(results):
    # Always English text
    lines = []
    lines.append("Top candidates (no-key onboard model):")
    for i, (label, p) in enumerate(results, start=1):
        lines.append(f"{i}) {label} — {round(p * 100, 1)}%")
    return "\n".join(lines)


# -----------------------------
# UI Pages
# -----------------------------
def render_home():
    st.title("🐾 Global Animal Explorer")

    st.markdown(
        """
A GitHub-friendly, Streamlit Cloud-ready animal project.

This app includes:
- **Featured Encyclopedia** (curated examples)
- **Animal Name Explorer** (type a name, get facts + image)
- **Global Animal Encyclopedia (GBIF)** (millions of species)
- **Image Animal Identifier** (no API key required)
"""
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Featured animals", len(ANIMALS_DATA))
    with c2:
        st.metric("Global coverage", "Millions (GBIF)")
    with c3:
        st.metric("No-key image ID", "Enabled")


def render_featured_categories():
    st.title("🗂️ Featured Animal Categories")
    cols = st.columns(3)
    i = 0
    for cat_id, info in ANIMAL_CATEGORIES.items():
        animals = get_animals_by_category(cat_id)
        with cols[i % 3]:
            st.markdown(f"### {info['name']}")
            st.write(info["description"])
            st.write(f"Estimated species count worldwide: **{info['count']}**")
            st.write(f"Featured examples here: **{len(animals)}**")
            if st.button(f"Open {info['name']}", key=f"open_{cat_id}"):
                st.session_state["page"] = "featured_category"
                st.session_state["category_id"] = cat_id
        i += 1


def render_featured_category_detail(category_id: str):
    info = ANIMAL_CATEGORIES.get(category_id)
    if not info:
        st.error("Category not found.")
        return

    st.title(f"📌 {info['name']}")
    st.write(info["description"])

    animals = get_animals_by_category(category_id)
    if not animals:
        st.info("No featured animals in this category yet.")
        return

    items = list(animals.items())
    cols = st.columns(3)
    for idx, (animal_id, a) in enumerate(items):
        with cols[idx % 3]:
            st.markdown(f"#### {a['name']}")
            if a.get("image"):
                st.image(a["image"], use_container_width=True)
            if a.get("scientific_name"):
                st.caption(a["scientific_name"])
            st.write((a.get("description") or "")[:140] + "...")
            if st.button("View details", key=f"detail_{animal_id}"):
                st.session_state["page"] = "featured_animal"
                st.session_state["animal_id"] = animal_id


def render_featured_animal_detail(animal_id: str):
    a = get_animal_detail(animal_id)
    if not a:
        st.error("Animal not found.")
        return

    cat = ANIMAL_CATEGORIES.get(a["category"], {"name": a["category"]})

    st.title(a["name"])
    st.caption(a.get("scientific_name", ""))

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        if a.get("image"):
            st.image(a["image"], use_container_width=True)
        st.markdown(f"**Category:** {cat['name']}")
        st.markdown(f"**Conservation status:** {a.get('conservation_status', 'N/A')}")
        st.markdown(f"**Habitat:** {a.get('habitat', 'N/A')}")
        st.markdown(f"**Distribution:** {a.get('distribution', 'N/A')}")
        st.markdown(f"**Population:** {a.get('population', 'N/A')}")

    with col2:
        st.markdown("### Overview")
        st.write(a.get("description", ""))

        if a.get("characteristics"):
            st.markdown("### Key characteristics")
            for c in a["characteristics"]:
                st.write(f"- {c}")

        if a.get("facts"):
            st.markdown("### Interesting facts")
            for f in a["facts"]:
                st.write(f"- {f}")

        if a.get("threats"):
            st.markdown("### Main threats")
            for t in a["threats"]:
                st.write(f"- {t}")


def render_name_explorer():
    st.title("🔎 Animal Name Explorer")
    st.markdown(
        """
Type an animal name and get an instant info card.

This works without any API key:
1) Searches the **Featured** collection.
2) Uses **GBIF** to validate and broaden results. :contentReference[oaicite:4]{index=4}
"""
    )

    query = st.text_input(
        "Enter a common name or scientific name",
        placeholder="Try: Snowy Owl, Bubo scandiacus, Ferret, Panthera tigris"
    )

    if not query:
        st.info("Type a name to begin.")
        return

    # 1) Local featured match
    hits = local_name_search(query)

    if hits:
        st.markdown("### Featured match")
        # If multiple hits, show the first as primary
        animal_id, a = hits[0]
        render_featured_animal_detail(animal_id)

        # Show additional matches (if any) without showing non-English aliases
        if len(hits) > 1:
            st.markdown("### More featured matches")
            for animal_id, a in hits[1:]:
                st.write(f"- {a['name']} ({a.get('scientific_name','')})")
        return

    # 2) GBIF fallback
    st.markdown("### Global lookup (GBIF)")
    try:
        match = gbif_species_match(query)
        usage_key = match.get("usageKey")
        sci = match.get("scientificName") or match.get("canonicalName") or "Unknown"
        rank = match.get("rank", "N/A")
        kingdom = match.get("kingdom", "N/A")
        family = match.get("family", "")
        genus = match.get("genus", "")

        if usage_key:
            st.success(f"Best GBIF match: {sci}")
            st.write(f"**Rank:** {rank}")
            st.write(f"**Kingdom:** {kingdom}")
            if family:
                st.write(f"**Family:** {family}")
            if genus:
                st.write(f"**Genus:** {genus}")

            # A simple generated "pop-science" style blurb without LLM
            st.markdown("### Quick natural history note")
            blurb = (
                f"This taxon is listed in the GBIF backbone as **{sci}**. "
                f"It belongs to the **{kingdom}** kingdom"
            )
            if family:
                blurb += f" and the **{family}** family"
            blurb += ". "
            blurb += (
                "For full ecological details and regional variation, "
                "you can explore occurrence records and curated sources."
            )
            st.write(blurb)
        else:
            # If match endpoint doesn't yield a clean hit, fall back to search list
            results = gbif_species_search(query, limit=5)
            if not results:
                st.warning("No global match found. Try another spelling.")
            else:
                for r in results:
                    canonical = r.get("canonicalName") or r.get("scientificName", "Unknown")
                    st.write(f"- **{canonical}** • {r.get('rank','N/A')} • {r.get('kingdom','N/A')}")
    except Exception as e:
        st.error(f"GBIF lookup failed: {e}")


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
            st.warning("No results found.")
            return

        st.markdown("### Search results")
        for r in results:
            canonical = r.get("canonicalName") or r.get("scientificName", "Unknown")
            rank = r.get("rank", "N/A")
            kingdom = r.get("kingdom", "N/A")
            with st.expander(f"{canonical} • {rank} • {kingdom}", expanded=False):
                st.json(r)
    except Exception as e:
        st.error(f"Global search failed: {e}")


def render_identifier():
    st.title("🧠 Image Animal Identifier (No API Key Required)")
    st.markdown(
        """
Upload an image and get an animal guess.

This page uses a lightweight onboard ImageNet classifier via ONNX.
It always returns **top candidates** when the model and labels are reachable.
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
