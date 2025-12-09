# Featured Animal Database (English)
# Curated representative animals per category.
# This is NOT meant to cover all animals in the world.
# Global coverage is provided by GBIF in the app.

ANIMAL_CATEGORIES = {
    "mammals": {
        "name": "Mammals",
        "description": (
            "Warm-blooded vertebrates typically covered in hair or fur. "
            "Most give live birth and feed young with milk. Mammals occupy "
            "nearly every habitat on Earth, from deserts to deep oceans, and "
            "include highly social, intelligent, and specialized species."
        ),
        "count": 5500
    },
    "birds": {
        "name": "Birds",
        "description": (
            "Feathered, warm-blooded vertebrates with beaks and lightweight skeletons. "
            "Many are capable of flight, while others have evolved for running or swimming. "
            "Birds are crucial for pollination, seed dispersal, and regulating insect populations."
        ),
        "count": 10000
    },
    "reptiles": {
        "name": "Reptiles",
        "description": (
            "Ectothermic vertebrates usually covered in scales or scutes. "
            "Most reproduce by laying eggs, though some give live birth. "
            "Reptiles range from small geckos to large crocodilians and play "
            "important roles as predators and prey in terrestrial and aquatic ecosystems."
        ),
        "count": 10000
    },
    "amphibians": {
        "name": "Amphibians",
        "description": (
            "Moist-skinned vertebrates that often begin life in water and transition "
            "to land. Many undergo metamorphosis. Their permeable skin makes them "
            "highly sensitive to pollution and climate change, so they are excellent "
            "indicators of ecosystem health."
        ),
        "count": 7000
    },
    "fish": {
        "name": "Fish",
        "description": (
            "Aquatic vertebrates that typically breathe through gills. "
            "They include jawless fish, cartilaginous fish (sharks and rays), "
            "and bony fish. Fish are foundational to freshwater and marine food webs "
            "and show remarkable diversity in form and behavior."
        ),
        "count": 32000
    },
    "insects": {
        "name": "Insects",
        "description": (
            "Six-legged arthropods with exoskeletons and segmented bodies. "
            "They are the most diverse animal group on Earth. Insects pollinate "
            "flowers, recycle nutrients, control pests, and serve as vital food sources "
            "for countless other animals."
        ),
        "count": 1000000
    }
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
    characteristics=None,
    facts=None,
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
        "characteristics": characteristics or [],
        "facts": facts or [],
        "threats": threats or [],
        # aliases are used for name testing/search (can include Chinese)
        "aliases": aliases or [],
    }


ANIMALS_DATA = {
    # -----------------------------
    # Mammals (expanded set)
    # -----------------------------
    "ferret": _animal(
        "Ferret",
        "mammals",
        "Mustela putorius furo",
        "Domesticated",
        "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=800",
        "A domesticated mustelid known for a long, flexible body and playful curiosity.",
        "Human care; derived from European polecats",
        "Worldwide (domesticated)",
        facts=[
            "Often confused with weasels, mink, and polecats in photos.",
        ],
        aliases=["snow ferret", "pet ferret", "雪貂", "貂", "雪鼬"]
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
        threats=["Habitat fragmentation", "Climate impacts on bamboo"],
        aliases=["panda", "大熊猫"]
    ),
    "tiger": _animal(
        "Tiger",
        "mammals",
        "Panthera tigris",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=800",
        "The largest cat species, a powerful solitary predator with unique stripes.",
        "Forests, grasslands, wetlands",
        "Asia",
        threats=["Poaching", "Habitat loss"],
        aliases=["bengal tiger", "siberian tiger", "老虎"]
    ),
    "lion": _animal(
        "Lion",
        "mammals",
        "Panthera leo",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1546182990-1b5e9a5f6c7f?w=800",
        "A social big cat living in prides across open landscapes.",
        "Savannas and grasslands",
        "Africa; small population in India",
        aliases=["狮子"]
    ),
    "african_elephant": _animal(
        "African Bush Elephant",
        "mammals",
        "Loxodonta africana",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "The largest land mammal with complex social behavior and strong memory.",
        "Savannas, forests",
        "Sub-Saharan Africa",
        aliases=["elephant", "非洲象"]
    ),
    "polar_bear": _animal(
        "Polar Bear",
        "mammals",
        "Ursus maritimus",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1525869916826-972885c91c1e?w=800",
        "A sea-ice-dependent Arctic predator superbly adapted to cold.",
        "Arctic sea ice and coasts",
        "Arctic Circle",
        threats=["Sea-ice loss"],
        aliases=["北极熊"]
    ),
    "red_panda": _animal(
        "Red Panda",
        "mammals",
        "Ailurus fulgens",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1526336024174-7c8d9e0f1a2b?w=800",
        "A small forest mammal often confused with raccoons in casual descriptions.",
        "Temperate forests with bamboo",
        "Himalayas and southwestern China",
        aliases=["小熊猫", "firefox"]
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
        aliases=["浣熊"]
    ),
    "sea_otter": _animal(
        "Sea Otter",
        "mammals",
        "Enhydra lutris",
        "Endangered (EN) in some regions",
        "https://images.unsplash.com/photo-1540573133985-4d7d1a1f5c1f?w=800",
        "A marine otter famous for tool use and dense fur.",
        "Coastal kelp forests",
        "North Pacific",
        aliases=["海獭"]
    ),
    "river_otter": _animal(
        "North American River Otter",
        "mammals",
        "Lontra canadensis",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1540573133985-4d7d1a1f5c1f?w=800",
        "A freshwater otter often confused with sea otters in photos.",
        "Rivers, lakes, wetlands",
        "North America",
        aliases=["水獭"]
    ),
    "walrus": _animal(
        "Walrus",
        "mammals",
        "Odobenus rosmarus",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=800",
        "A large marine mammal with tusks and whiskers.",
        "Arctic seas and ice edges",
        "Arctic Circle",
        aliases=["海象"]
    ),
    "harbor_seal": _animal(
        "Harbor Seal",
        "mammals",
        "Phoca vitulina",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1544551763-92b8b3b6f0f5?w=800",
        "A true seal that spends much of life in water but hauls out on land.",
        "Coastal waters",
        "Northern Hemisphere coasts",
        aliases=["seal", "海豹"]
    ),
    "sea_lion": _animal(
        "California Sea Lion",
        "mammals",
        "Zalophus californianus",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
        "An eared seal known for agility and social groups.",
        "Coastal waters",
        "Eastern Pacific",
        aliases=["sea lion", "海狮"]
    ),

    # -----------------------------
    # Birds
    # -----------------------------
    "snowy_owl": _animal(
        "Snowy Owl",
        "birds",
        "Bubo scandiacus",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1540573133985-2b3c4d5e6f7a?w=800",
        "A large Arctic owl with white plumage, often seen on tundra landscapes.",
        "Tundra; wintering on open fields and coasts",
        "Arctic regions",
        aliases=["雪鸮", "雪雕", "snow owl"]
    ),
    "golden_eagle": _animal(
        "Golden Eagle",
        "birds",
        "Aquila chrysaetos",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1611689342806-0863700ce1e4?w=800",
        "A powerful raptor with exceptional flight and hunting skill.",
        "Mountains, open country",
        "Northern Hemisphere",
        aliases=["金雕"]
    ),
    "peregrine_falcon": _animal(
        "Peregrine Falcon",
        "birds",
        "Falco peregrinus",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1540573133985-64c1e8f4c6d0?w=800",
        "The fastest animal in a hunting stoop.",
        "Cliffs, cities, open landscapes",
        "Worldwide",
        aliases=["游隼"]
    ),
    "emperor_penguin": _animal(
        "Emperor Penguin",
        "birds",
        "Aptenodytes forsteri",
        "Near Threatened (NT)",
        "https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=800",
        "The largest penguin species, breeding in the Antarctic winter.",
        "Antarctic sea ice",
        "Antarctica",
        aliases=["帝企鹅"]
    ),
    "ostrich": _animal(
        "Ostrich",
        "birds",
        "Struthio camelus",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1526336024174-9b1c2d3e4f5a?w=800",
        "The largest living bird, flightless and extremely fast on land.",
        "Savannas and semi-deserts",
        "Africa",
        aliases=["鸵鸟"]
    ),

    # -----------------------------
    # Reptiles
    # -----------------------------
    "komodo_dragon": _animal(
        "Komodo Dragon",
        "reptiles",
        "Varanus komodoensis",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800",
        "The largest living lizard, a top predator on a few Indonesian islands.",
        "Dry forests and savannas",
        "Indonesia",
        aliases=["科莫多巨蜥"]
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
        aliases=["尼罗鳄"]
    ),

    # -----------------------------
    # Amphibians
    # -----------------------------
    "red_eyed_tree_frog": _animal(
        "Red-Eyed Tree Frog",
        "amphibians",
        "Agalychnis callidryas",
        "Least Concern (LC)",
        "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=800",
        "A rainforest frog known for vivid colors that can startle predators.",
        "Tropical rainforests",
        "Central America",
        aliases=["红眼树蛙"]
    ),
    "axolotl": _animal(
        "Axolotl",
        "amphibians",
        "Ambystoma mexicanum",
        "Critically Endangered (CR)",
        "https://images.unsplash.com/photo-1583511655942-70c5d7b0e0d4?w=800",
        "A neotenic salamander that retains larval traits throughout life.",
        "Freshwater canals and lakes",
        "Mexico",
        aliases=["美西螈", "六角恐龙"]
    ),

    # -----------------------------
    # Fish / marine invertebrate-like lookalikes handled by name tester & AI
    # -----------------------------
    "great_white_shark": _animal(
        "Great White Shark",
        "fish",
        "Carcharodon carcharias",
        "Vulnerable (VU)",
        "https://images.unsplash.com/photo-1560275619-4662e36fa65c?w=800",
        "A powerful apex predator important for ocean ecosystem balance.",
        "Temperate coastal and offshore waters",
        "Worldwide",
        aliases=["大白鲨"]
    ),
    "seahorse": _animal(
        "Seahorse",
        "fish",
        "Hippocampus (genus)",
        "Varies by species",
        "https://images.unsplash.com/photo-1526336024174-33cc44dd55ee?w=800",
        "Unique fish known for male pregnancy and upright posture.",
        "Seagrass beds and reefs",
        "Worldwide",
        aliases=["海马"]
    ),

    # -----------------------------
    # Insects
    # -----------------------------
    "monarch_butterfly": _animal(
        "Monarch Butterfly",
        "insects",
        "Danaus plexippus",
        "Endangered (EN)",
        "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=800",
        "Famous for long-distance migration and dependence on milkweed.",
        "Fields, gardens, grasslands",
        "North America and beyond",
        aliases=["帝王蝶"]
    ),
    "honey_bee": _animal(
        "Western Honey Bee",
        "insects",
        "Apis mellifera",
        "Managed/Domesticated",
        "https://images.unsplash.com/photo-1472141521881-95d0e87e2e39?w=800",
        "A key pollinator essential to agriculture and natural ecosystems.",
        "Varied",
        "Worldwide",
        aliases=["蜜蜂"]
    ),
}


def get_animals_by_category(category):
    return {k: v for k, v in ANIMALS_DATA.items() if v["category"] == category}


def get_animal_detail(animal_id):
    return ANIMALS_DATA.get(animal_id)
