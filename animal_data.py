# Curated featured animals (English UI).
# This is a "featured" collection, not the full world encyclopedia.
# The global coverage is provided by GBIF in the app.

ANIMAL_CATEGORIES = {
    "mammals": {
        "name": "Mammals",
        "description": (
            "Warm-blooded vertebrates typically covered in hair or fur. "
            "Most give live birth and feed young with milk. Mammals occupy "
            "nearly every habitat on Earth and include highly social and "
            "intelligent species."
        ),
        "count": 5500,
    },
    "birds": {
        "name": "Birds",
        "description": (
            "Feathered, warm-blooded vertebrates with beaks. Many can fly, "
            "while others are adapted for running or swimming. Birds play "
            "major roles in pollination, seed dispersal, and insect control."
        ),
        "count": 10000,
    },
    "reptiles": {
        "name": "Reptiles",
        "description": (
            "Ectothermic vertebrates usually covered in scales. Most lay eggs, "
            "though some give live birth. Reptiles range from small lizards to "
            "large crocodilians and are important predators in many ecosystems."
        ),
        "count": 10000,
    },
    "amphibians": {
        "name": "Amphibians",
        "description": (
            "Moist-skinned vertebrates that often begin life in water and "
            "transition to land. Many undergo metamorphosis and are sensitive "
            "to environmental change, making them key indicators of ecosystem health."
        ),
        "count": 7000,
    },
    "fish": {
        "name": "Fish",
        "description": (
            "Aquatic vertebrates that typically breathe through gills. They include "
            "jawless, cartilaginous, and bony fish. Fish are foundational to "
            "freshwater and marine food webs."
        ),
        "count": 32000,
    },
    "insects": {
        "name": "Insects",
        "description": (
            "Six-legged arthropods with exoskeletons and segmented bodies. "
            "They are the most diverse animal group on Earth and are essential "
            "for pollination, decomposition, and food webs."
        ),
        "count": 1000000,
    },
}


def _animal(
    name,
    category,
    scientific_name,
    status,
    image,
    description,
    habitat,
    distribution,
    population="Varies",
    facts=None,
    characteristics=None,
    threats=None,
    aliases=None,
):
    return {
        "name": name,
        "category": category,
        "scientific_name": scientific_name,
        "conservation_status": status,
        "image": image,
        "description": description,
        "habitat": habitat,
        "distribution": distribution,
        "population": population,
        "facts": facts or [],
        "characteristics": characteristics or [],
        "threats": threats or [],
        # Aliases can include non-English inputs; UI will not display them.
        "aliases": aliases or [],
    }


ANIMALS_DATA = {
    # Mammals
    "ferret": _animal(
        "Ferret",
        "mammals",
        "Mustela putorius furo",
        "Domesticated",
        "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=800",
        "A domesticated mustelid known for a slender body, curiosity, and playful behavior.",
        "Human care; derived from European polecats",
        "Worldwide (domesticated)",
        facts=[
            "Often confused with weasels, mink, and polecats in photos.",
            "Highly inquisitive and capable of learning routines and tricks.",
        ],
        aliases=["ferret", "pet ferret", "Mustela putorius furo", "雪貂", "貂"],
    ),
    "giant_panda": _animal(
        "Giant Panda",
        "mammals",
        "Ailuropoda melanoleuca",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=800",
        "A bamboo specialist endemic to China with distinctive black-and-white fur.",
        "Temperate mountain forests with bamboo",
        "China",
        facts=["Consumes large amounts of bamboo daily."],
        aliases=["giant panda", "panda", "Ailuropoda melanoleuca", "大熊猫"],
    ),
    "tiger": _animal(
        "Tiger",
        "mammals",
        "Panthera tigris",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=800",
        "The largest cat species, a powerful solitary predator with unique stripe patterns.",
        "Forests, grasslands, wetlands",
        "Asia",
        threats=["Poaching", "Habitat loss"],
        aliases=["tiger", "Panthera tigris", "老虎"],
    ),
    "sea_otter": _animal(
        "Sea Otter",
        "mammals",
        "Enhydra lutris",
        "Endangered (regional)",
        "https://images.unsplash.com/photo-1540573133985-4d7d1a1f5c1f?w=800",
        "A marine otter famous for tool use and exceptionally dense fur.",
        "Coastal kelp forests",
        "North Pacific",
        aliases=["sea otter", "Enhydra lutris", "海獭"],
    ),
    "river_otter": _animal(
        "North American River Otter",
        "mammals",
        "Lontra canadensis",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1540573133985-4d7d1a1f5c1f?w=800",
        "A freshwater otter with playful behavior, often confused with sea otters in photos.",
        "Rivers, lakes, wetlands",
        "North America",
        aliases=["river otter", "Lontra canadensis", "水獭"],
    ),
    "raccoon": _animal(
        "Raccoon",
        "mammals",
        "Procyon lotor",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "An adaptable omnivore known for a mask-like face and dexterous paws.",
        "Forests, wetlands, urban areas",
        "North America; introduced elsewhere",
        aliases=["raccoon", "Procyon lotor", "浣熊"],
    ),
    "red_panda": _animal(
        "Red Panda",
        "mammals",
        "Ailurus fulgens",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1526336024174-7c8d9e0f1a2b?w=800",
        "A small forest mammal often confused with raccoons due to facial markings.",
        "Temperate forests with bamboo",
        "Himalayas and southwestern China",
        aliases=["red panda", "Ailurus fulgens", "小熊猫"],
    ),

    # Birds
    "snowy_owl": _animal(
        "Snowy Owl",
        "birds",
        "Bubo scandiacus",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1540573133985-2b3c4d5e6f7a?w=800",
        "A large Arctic owl with white plumage adapted to tundra environments.",
        "Tundra; wintering on open fields and coastal areas",
        "Arctic regions",
        facts=[
            "Females and juveniles typically show more dark barring than adult males.",
            "A charismatic predator of lemmings in the Arctic food web.",
        ],
        aliases=["snowy owl", "Bubo scandiacus", "snow owl", "雪鸮", "雪雕"],
    ),
    "golden_eagle": _animal(
        "Golden Eagle",
        "birds",
        "Aquila chrysaetos",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1611689342806-0863700ce1e4?w=800",
        "A powerful raptor with exceptional vision and hunting skill.",
        "Mountains and open country",
        "Northern Hemisphere",
        aliases=["golden eagle", "Aquila chrysaetos", "金雕"],
    ),
    "emperor_penguin": _animal(
        "Emperor Penguin",
        "birds",
        "Aptenodytes forsteri",
        "Near Threatened (NT)",
        "https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=800",
        "The largest penguin species, breeding during the Antarctic winter.",
        "Antarctic sea ice",
        "Antarctica",
        aliases=["emperor penguin", "Aptenodytes forsteri", "帝企鹅"],
    ),

    # Reptiles
    "komodo_dragon": _animal(
        "Komodo Dragon",
        "reptiles",
        "Varanus komodoensis",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800",
        "The largest living lizard and an apex predator on a few Indonesian islands.",
        "Dry forests and savannas",
        "Indonesia",
        aliases=["komodo dragon", "Varanus komodoensis", "科莫多巨蜥"],
    ),
    "nile_crocodile": _animal(
        "Nile Crocodile",
        "reptiles",
        "Crocodylus niloticus",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=800",
        "A formidable freshwater predator with a powerful bite.",
        "Rivers, lakes, wetlands",
        "Sub-Saharan Africa",
        aliases=["nile crocodile", "Crocodylus niloticus", "尼罗鳄"],
    ),

    # Amphibians
    "axolotl": _animal(
        "Axolotl",
        "amphibians",
        "Ambystoma mexicanum",
        "Critically Endangered (CR)",
        "https://images.unsplash.com/photo-1583511655942-70c5d7b0e0d4?w=800",
        "A neotenic salamander that retains larval traits throughout life.",
        "Freshwater canals and lakes",
        "Mexico",
        aliases=["axolotl", "Ambystoma mexicanum", "美西螈", "六角恐龙"],
    ),

    # Fish
    "great_white_shark": _animal(
        "Great White Shark",
        "fish",
        "Carcharodon carcharias",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1560275619-4662e36fa65c?w=800",
        "A powerful marine predator important for ocean ecosystem balance.",
        "Temperate coastal and offshore waters",
        "Worldwide",
        aliases=["great white shark", "Carcharodon carcharias", "大白鲨"],
    ),

    # Insects
    "monarch_butterfly": _animal(
        "Monarch Butterfly",
        "insects",
        "Danaus plexippus",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=800",
        "Famous for long-distance migration and dependence on milkweed.",
        "Fields, gardens, grasslands",
        "North America and beyond",
        aliases=["monarch butterfly", "Danaus plexippus", "帝王蝶"],
    ),
}


def get_animals_by_category(category):
    return {k: v for k, v in ANIMALS_DATA.items() if v["category"] == category}


def get_animal_detail(animal_id):
    return ANIMALS_DATA.get(animal_id)
