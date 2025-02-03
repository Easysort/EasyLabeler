DEFAULT_CLASS_NAMES = {
    # ---- # Hard plastics # ---- #
    0: "Coffee cup lid",
    1: "Bottle cap",
    2: "PS styrofoam",
    3: "Light blue pet bottle",
    4: "Clear pet bottle food covered", # Juice, soda with branding
    5: "Clear pet bottle non food convered", #Shampoo, detergent, cleaning
    6: "Clear pet bottle",
    7: "Brown pet bottle",
    8: "Coloured pet bottle",
    9: "Dark blue pet bottle",
    10: "Green pet bottle",
    11: "White pet bottle",
    12: "Pet bottle other colour",
    13: "Coloured hdpe bottle",
    14: "Coloured yoghurt plastic bottle", 
    15: "Coloured hdpe bottle",
    16: "Natural hdpe bottle",
    17: "Natural yoghurt plastic bottle",
    18: "Natural hdpe bottle",
    19: "Black container",
    20: "Black plastic bottle",
    21: "Other black plastic",
    22: "Clear container",
    23: "Coloured container",
    24: "White container",
    25: "Other plastic",
    # ---- # Flexible plastics # ---- #
    40: "Bottle label film",
    41: "Film bubble wrap",
    42: "Clear film",
    43: "Clear printed film",
    44: "Coloured film",
    45: "Filled bag",
    46: "Coloured printed film",
    47: "Metallised film", # Chips bags, coffee packets
    48: "Black film",
    # ---- # Metals # ---- #
    60: "Aluminium Aerosol", # Hairspray cans, deodorant, spray paint
    61: "Aluminium cans", # Soda cans
    62: "Aluminium other", # Foil, caps, etc.
    63: "Steel cans",
    64: "Metal other", # Food container, coffee cans, pet food cans
    # ---- # Paper/Cardboard # ---- #
    70: "Cardboard packaging",
    71: "Paper packaging",
    72: "Clean paper sheet (Can be written on, but no food)",
    73: "Dirty paper (Food, etc.)",
    74: "Wipes",
    # ---- # Composite # ---- #
    80: "Tetra Pak Carton (Milk, juice cartons, etc.)",
    81: "Cup drink (Disposable cups)",
    82: "Cup food (Disposable food containers)",
    # ---- # Electronics # ---- #
    90: "Weee (Waste Electrical and Electronic Equipment)",
    91: "Batteries",
    # ---- # Glass # ---- #
    100: "Clear glass bottle",
    101: "Green glass bottle",
    102: "Brown glass bottle",
    103: "Clear glass cullet (broken)",
    104: "Green glass cullet (broken)",
    105: "Brown glass cullet (broken)",
    106: "Glass with plastic",
    107: "Other glass",
    # ---- # Clothes # ---- #
    120: "Clothes/Fabric",
    # ---- # Other # ---- #
    130: "Fine (small granular material)",
    131: "Sanitary",
    132: "Other (General waste)"
}

DEFAULT_FRACTIONS = {
    0: 0, # Hard plastics
    1: 40, # Flexible plastics
    2: 60, # Metals
    3: 70, # Paper/Cardboard
    4: 80, # Composite
    5: 90, # Electronics
    6: 100, # Glass
    7: 120, # Clothes
    8: 130, # Other
}

FRACTIONS_NAMES = {
    0: "Hard plastics",
    1: "Flexible plastics", 
    2: "Metals",
    3: "Paper/Cardboard",
    4: "Composite",
    5: "Electronics",
    6: "Glass",
    7: "Clothes",
    8: "Other",
}

DEFAULT_CLASS_TO_FRACTION = {
    **{i: 0 for i in range(40)},  # Hard plastics (0-25)
    **{i: 1 for i in range(40, 60)},  # Flexible plastics (26-34)
    **{i: 2 for i in range(60, 70)},  # Metals (35-39)
    **{i: 3 for i in range(70, 80)},  # Paper/Cardboard (40-44)
    **{i: 4 for i in range(80, 90)},  # Composite (45-47)
    **{i: 5 for i in range(90, 100)},  # Electronics (48-49)
    **{i: 6 for i in range(100, 120)},  # Glass (50-57)
    **{i: 7 for i in range(120, 130)},  # Clothes (58)
    **{i: 8 for i in range(130, 140)}   # Other (59-61)
}

DEFAULT_COLORS = {
    **{i: (255, 128, 128) for i in range(40)},
    **{i: (255, 192, 128) for i in range(40, 60)},
    **{i: (192, 192, 192) for i in range(60, 70)},
    **{i: (128, 255, 128) for i in range(70, 80)},
    **{i: (255, 255, 128) for i in range(80, 90)},
    **{i: (128, 128, 255) for i in range(90, 100)},
    **{i: (192, 255, 255) for i in range(100, 120)},
    **{i: (255, 128, 255) for i in range(120, 130)},
    **{i: (192, 192, 128) for i in range(130, 140)}
}

if __name__ == "__main__":
    print(len(DEFAULT_CLASS_NAMES))
