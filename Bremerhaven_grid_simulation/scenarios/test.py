test = {4:
    {"Industry": [
        "Weddewarden Industrielast",
        "Lehe Industrielast",
        "Geestemünde Industrielast",
        "Schiffdorferdamm Industrielast",
        "Leherheide Industrielast",
        "Surheide Industrielast",
        "Fischereihafen Industrielast",
        "Wulsdorf Industrielast",
        "Erdgas Kronos Titan GmbH",
    ]},
    3:
        {"Households": [
            "Geestemünde Households - 0",
            "Geestemünde Households - 1",
            "Geestemünde Households - 2",
            "Mitte Households - 0",
            "Mitte Households - 1",
            "Lehe Households - 0",
            "Lehe Households - 1",
            "Lehe Households - 2",
            "Lehe Households - 3",
            "Lehe Households - 4",
            "Leherheide Households - 0",
            "Leherheide Households - 1",
            "Schiffdorferdamm Households",
            "Weddewarden Households",
            "Surheide Households",
            "Wulsdorf Households - 0",
            "Wulsdorf Households - 1",
            "Fischereihafen Households",
            "Fischereihafen - 4",
            "Fischereihafen - 3",
            "Fischereihafen - 2",
            "Fischereihafen - 1",
            "Fischereihafen - 0", ]},

    2: {"Hospital": [
        "Klinikum Bremerhaven - Reinkenheide gGmbH",
        "AMEOS Klinikum Am Bürgerpark Bremerhaven",
        "AMEOS Klinikum Mitte Bremerhaven",
    ],
        "Public": [
            "Bremerhaven Eisarena, Stadthalle etc.",
            "Bremerhaven Süd",
            "Zoo",
            "Bremerhaven Innenstadt",
        ]},
    1: {"PV":
            ["PV Fischereihafen",
             "PV Geestemünde - 0",
             "PV Geestemünde - 1",
             "PV Geestemünde - 2",
             "PV Lehe - 0",
             "PV Lehe - 1",
             "PV Lehe - 2",
             "PV Lehe - 3",
             "PV Lehe - 4",
             "PV Leherheide - 0",
             "PV Leherheide - 1",
             "PV Mitte - 0",
             "PV Mitte - 1",
             "PV Schiffdorferdamm",
             "PV Surheide",
             "PV Weddewarden",
             "PV Wulsdorf - 0",
             "PV Wulsdorf - 1", ],
        "Wind": [
            "Windpark Speckenbüttel 2",
            "Windpark Speckenbüttel 1",
            "Windpark Multibrid",
            "Windpark Repower",
            "Windpark Lehe", ]}}

ethics_values = list(test.keys())
name = "Leherheide Industrielast"
for value in ethics_values:
    print(list(test[value].values()))
    for index in range(len(test[value].values())):
        if any(string in name for string in list(test[value].values())[index]):
            print(value)
print(min(ethics_values))

ethics_score_list = {}
for key in test.keys():
    ethics_score_list[key] = [0.0, 0, 0]

ethics_score_tiers = list(ethics_score_list.keys())
for tier in ethics_score_tiers:
    if tier <= 2.0 < tier + 1.0:
        ethics_score_list[tier][0] = ethics_score_list[tier][0] + 2.0
        ethics_score_list[tier][2] += 1
        if True:
            ethics_score_list[tier][1] += 1
