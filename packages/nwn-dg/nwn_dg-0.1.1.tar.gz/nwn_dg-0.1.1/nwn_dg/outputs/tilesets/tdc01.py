K_BASEDATA = {
    "ChanceLightning": {"type": "int", "value": 0},
    "ChanceRain": {"type": "int", "value": 0},
    "ChanceSnow": {"type": "int", "value": 0},
    "Comments": {"type": "cexostring", "value": ""},
    "Creator_ID": {"type": "int", "value": -1},
    "DayNightCycle": {"type": "byte", "value": 0},
    "Expansion_List": {"type": "list", "value": []},
    "Flags": {"type": "dword", "value": 3},
    "FogClipDist": {"type": "float", "value": 45},
    "Height": {"type": "int", "value": 15},
    "ID": {"type": "int", "value": -1},
    "IsNight": {"type": "byte", "value": 1},
    "LightingScheme": {"type": "byte", "value": 13},
    "LoadScreenID": {"type": "word", "value": 0},
    "ModListenCheck": {"type": "int", "value": 0},
    "ModSpotCheck": {"type": "int", "value": 0},
    "MoonAmbientColor": {"type": "dword", "value": 2960685},
    "MoonDiffuseColor": {"type": "dword", "value": 6457991},
    "MoonFogAmount": {"type": "byte", "value": 5},
    "MoonFogColor": {"type": "dword", "value": 0},
    "MoonShadows": {"type": "byte", "value": 0},
    "Name": {
        "type": "cexolocstring",
        "value": {"0": "Unnamed"},
    },
    "NoRest": {"type": "byte", "value": 0},
    "OnEnter": {"type": "resref", "value": ""},
    "OnExit": {"type": "resref", "value": ""},
    "OnHeartbeat": {"type": "resref", "value": ""},
    "OnUserDefined": {"type": "resref", "value": ""},
    "PlayerVsPlayer": {"type": "byte", "value": 3},
    "ResRef": {"type": "resref", "value": "new_resref"},
    "ShadowOpacity": {"type": "byte", "value": 60},
    "SkyBox": {"type": "byte", "value": 0},
    "SunAmbientColor": {"type": "dword", "value": 0},
    "SunDiffuseColor": {"type": "dword", "value": 0},
    "SunFogAmount": {"type": "byte", "value": 0},
    "SunFogColor": {"type": "dword", "value": 0},
    "SunShadows": {"type": "byte", "value": 0},
    "Tag": {"type": "cexostring", "value": "NewTag"},
    "TileBrdrDisabled": {"type": "byte", "value": 0},
    "Tile_List": {
        "type": "list",
        "value": [],
    },
    "Tileset": {"type": "resref", "value": "tdc01"},
    "Version": {"type": "dword", "value": 3},
    "Width": {"type": "int", "value": 15},
    "WindPower": {"type": "int", "value": 0},
    "__data_type": "ARE ",
}

# Center, N, E, S, W for an orientation of 0
# Tile orientations are:
#     0 = Normal orientation
#     1 = 90 degrees counterclockwise
#     2 = 180 degrees counterclockwise
#     3 = 270 degrees counterclockwise
K_PATTERNS = {
    "W": {"Tile_ID": [5]},
    # Corridor
    "CCWWW": {"Tile_ID": [41]},
    "CWWCC": {"Tile_ID": [127]},
    "CCWCC": {"Tile_ID": [130]},
    "CCWCW": {"Tile_ID": [118]},
    "CCCCC": {"Tile_ID": [40]},
    # ---
    # Corridor next to rooms
    "CRWCW": {"Tile_ID": [129]},
    "CRWRW": {"Tile_ID": [118]},
    # ---
    # Rooms
    "RWWRR": {"Tile_ID": [0]},
    "RRWRR": {"Tile_ID": [117]},
    "RRRRR": {"Tile_ID": [101]},
    # ---
    # Rooms + Corridor exits
    "RCWRR": {"Tile_ID": [125]},
    "RRCCR": {"Tile_ID": [19]},
    "RRWCR": {"Tile_ID": [126]},
    "RRCRR": {"Tile_ID": [18]},
}

K_TILES = {
    # fmt: off
      0: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 0}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
      4: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 4}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
      5: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 5}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
     18: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 18}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     19: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 19}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 0}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
     21: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 21}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
     30: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 117}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     38: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 38}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     65: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 65}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     40: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 40}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
     41: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 41}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
     71: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 71}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    101: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 101}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    102: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 102}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 0}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
    109: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 109}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 0}, "Tile_SrcLight2": { "type": "byte", "value": 0}},
    114: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 114}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    115: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 115}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    116: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 116}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    117: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 117}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    118: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 118}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 0}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    119: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 119}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    125: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 125}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    126: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 126}, "Tile_MainLight1": { "type": "byte", "value": 0}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    127: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 127}, "Tile_MainLight1": { "type": "byte", "value": 30}, "Tile_MainLight2": { "type": "byte", "value": 0}, "Tile_Orientation": { "type": "int", "value": 1}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    129: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 129}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 14}, "Tile_Orientation": { "type": "int", "value": 3}, "Tile_SrcLight1": { "type": "byte", "value": 2}, "Tile_SrcLight2": { "type": "byte", "value": 2}},
    130: { "__struct_id": 1, "Tile_AnimLoop1": { "type": "byte", "value": 1}, "Tile_AnimLoop2": { "type": "byte", "value": 1}, "Tile_AnimLoop3": { "type": "byte", "value": 1}, "Tile_Height": { "type": "int", "value": 0}, "Tile_ID": { "type": "int", "value": 130}, "Tile_MainLight1": { "type": "byte", "value": 4}, "Tile_MainLight2": { "type": "byte", "value": 13}, "Tile_Orientation": { "type": "int", "value": 2}, "Tile_SrcLight1": { "type": "byte", "value": 3}, "Tile_SrcLight2": { "type": "byte", "value": 3}},
    # fmt: on
}
