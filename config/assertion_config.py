#Community anchors assertion
#1
COMMUNITY_ANCHOR_LABELS = [
        "Library",
        "College/University",
        "School",
        "Government Office",
        "Hospital/Polyclinic"
    ]
#2
OPPORTUNITY_ANALYSIS_LABELS = [
        "No",
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
#3
ROAD_DENSITY_LABELS = [
        "≤ 10",
        "11-20",
        "21-30",
        "31-40",
        "41-50",
        "> 50"
    ]
#4
AREA_DENSITY_LABELS = [
        "No Data",
        "0-10",
        "11-50",
        "51-200",
        "201-500",
        "501+"
    ]
#5
HOME_VALUE_LABELS = [
        "≤ $10,000",
        "≤ $10,001 - ≤ $100,000",
        "≤ $100,001 - ≤ $200,000",
        "≤ $200,001 - ≤ $300,000",
        "≤ $300,001 - ≤ $400,000",
        "≤ $400,001 - ≤ $500,000",
        "≤ $500,001 - ≤ $2,000,000",
        "> $2,000,000"
    ]
#6
UTILITY_BOUNDARIES_LABELS = [
        "Single Utility Provider",
        "Multi Utility Provider",
    ]
#7
ENVIRONMENT_RISK_LABELS = [
        "Very High",
        "Relatively High",
        "Relatively Moderate",
        "Relatively Low",
        "Very Low"
    ]
#8
ERATE_AWARDS_LABELS = [
        "Active E-Rate",
        "Inactive E-Rate",
        "E-Rate Not filed"
    ]
#9
MIDDLE_MILE_LABELS = [
        "Underground",
        "Aerial"
    ]

MIDDLE_MILE_LABELS_ETHERNIC = [
        "Aerial"
]

MIDDLE_MILE_LABELS_OTHER_PROVIDERS = [
        "Underground"
]
#10
CELL_TOWERS_LABELS = [
        "Constructed",
        "Granted",
        "Antennas",
        "Towers/Antennas",
        "Silos",
        "Water Tanks"
    ]

#Cell tower by default off for maricopa county AZ
CELL_TOWERS_LABELS_DEFAULT_OFF_CAMPBELL = [
        "Silos"
]

CELL_TOWERS_LABELS_CAMPBELL = [
        "Constructed",
        "Granted",
        "Antennas",
        "Towers/Antennas",
        "Water Tanks"
    ]
#11
AREA_BOUNDARIES_LABELS = [
        "Zip Codes",
        "Municipal Areas",
        "City/Town/CDP",
        "Congressional Districts",
        "State Leg. Dists(L)",
        "State Leg. Dists(U)"
    ]
#12
BEAD_BOUNDARY_LABELS = [
        "BEAD Boundaries"
    ]
#13
HOUSEHOLD_INCOME_LABELS = [
        "$1 to $29,999",
        "$30,000 to $74,999",
        "$75,000 to $124,999",
        "$125,000 to $200,000",
        "> $200,000"
    ]
#14
RAIL_ROADS_LABELS = [
        "Roads",
        "Rail Road",
        "Rail Crossing",
        "Bridges"
    ]
#15
FIBER_GROWTH_LABELS = [
        "1 – 25%",
        "26 – 50%",
        "51 – 75%",
        "76 – 99%",
        "≥ 100%"
    ]
#16
FWA_COVERAGE_LABELS = [
        "0 %",
        "1 - 20 %",
        "21 - 40 %",
        "41 - 60 %",
        "61 - 80 %",
        "81 - 100 %"
    ]
#17
GRANT_OPPORTUNITY_LABELS = [
        "No",
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
#18
PALISTAR_LABELS = [
        "Towers"
    ]
#19
CONTERRA_LABELS = [
        "Splice Points",
        "Connected Buildings",
        "Manhole"
]
#20
ETHERIC_LABELS = [
        "Splice Points"
]
#21
FIRSTLIGHT_LABELS = [
        "Splice Points"
]
#22
DOBSON_LABELS = [
        "Splice Points"
]
#23
LOCATION_LENS_LABELS = [
        "Residential(SDU)",
        "Residential(MDU)",
        "Commercial (GeoResults)",
        "Commercial",
        "Agriculture",
        "Institutional",
        "Unclassified"
    ]
#24
ISP_FIBER_LABELS1 = [
        'CenturyLink',
        'Quantum Fiber',
        'Xfinity',
        'Great Plains Broadband LLC',
        'Metronet Holdings',
        'FASTWYRE BROADBAND',
        'Cogent Communication',
        'Google Fiber',
        'Aureon Communications, L.L.C.',
        'UPN'
]

#25.COX
COX_LENS_LABELS = [
        'Cable Locations',
        'Fiber Locations',
        'Network',
        'Splice Points'
]

#26.SKYWIRE
SKYWIRE_LENS_LABLES = [
        'Locations',
        'Hubs',
        'LoS Boundaries',
        'Lit Buildings',
        'Line of Sight',
]


#27.CABLE-ONE
CABLE_ONE_LABELS = [
        "VCTI Identified AOI's",
        "Boundaries",
        "Networks"
]

POLE_OWNER_LABELS = [
    "ILEC Boundaries",
    "Utility Boundaries (Single)",
    "Utility Boundaries (Multiple)"
]

AREA_BOUNDARIES_LABELS_TOGGLE_OFF = [
        "Zip Codes",
        "Congressional Districts",
        "State Leg. Dists(L)",
        "State Leg. Dists(U)"
    ]

#31.
FABRIC_LOCATION_LABELS = [
        "Residential",
        "Business",
        "Institutional",
        "Underserved",
        "Unserved"
]

#32.
FABRIC_LOCATION_LABELS_TOGGLE_OFF = [
        "Residential",
        "Business",
        "Institutional"
]

#33.
EXPECTED_COUNTS = {
        "Underserved": 1017,
        "Unserved": 4874
    }

#34
FABRIC_LOCATION_LABELS_DEFAULT_OFF = [
        "Underserved",
        "Unserved"
]

RITTER_LABELS = [
    "Areas"
]

FIBERLIGHT_LABELS = [
    "Network",
    "Boundaries",
    "Splice Points"
]

MASTER_PACKAGE_LAYERS = [
    "Grant Opportunity Areas",
    "Broadband Funding",
    "BEAD Project Areas",
    "Locations",
    "Fiber Growth",
    "Road Density",
    "Area Density",
    "Household Income",
    "Home Value",
    "Electric Utility Providers",
    "Local Exchange Carriers",
    "Community Anchor Institutions",
    "Cellular Towers",
    "National Risk Index",
    "E-Rate Funding",
    "Data Centers",
    "Roads",
    "Middle Mile",
    "HOA",
    "Low Income Housing",
    "FWA Coverage Only",
    "Area Boundaries",
    "Conterra",
    "FirstLight Fiber",
    "Skywire",
    "Cable One",
    "Fabric Locations",
    "Ritter Communications",
    "Hotwire",
    "Permit Data"
]

RITTER_LAYERS = [
    "Grant Opportunity Areas", "Locations", "Road Density", "Area Density",
    "Household Income", "Home Value", "Community Anchor Institutions", "Cellular Towers",
    "National Risk Index", "E-Rate Funding", "Roads", "HOA", "Ritter Communications"
]

SALES_PROFILE_LAYERS = [
    "Community Anchor Institutions", "Cellular Towers", "E-Rate Funding",
    "Data Centers", "Middle Mile", "HOA", "Conterra"
]

POLE_OWNER_LABELS = [
    "ILEC Boundaries",
    "Utility Boundaries (Single)",
    "Utility Boundaries (Multiple)"
]

HOTWIRE_LABELS = [
    "Grant Opportunity Areas",
    "Broadband Funding",
    "BEAD Project Areas",
    "Locations",
    "Fiber Growth",
    "Road Density",
    "Area Density",
    "Household Income",
    "Home Value",
    "Electric Utility Providers",
    "Local Exchange Carriers",
    "Cellular Towers",
    "National Risk Index",
    "E-Rate Funding",
    "Data Centers",
    "Roads",
    "Middle Mile",
    "HOA",
    "Low Income Housing",
    "FWA Coverage Only",
    "Area Boundaries"
]

BEAD_ROUND1_AND_ROUND2 = [
    "Round1",
    "Round2"
]

RITTER_LABELS = [
    "Areas"
]

LOGS_STATUS_FAILURE_LABELS = 'failure'
LOGS_STATUS_SUCCESS_LABEL = 'success'
LOGS_ADDRESS_LABEL = 'TEXAS'
LOGS_CO_ORDINATES_LABEL = "30.1556, -95.1604"
LOGS_REGION_LABEL = 'Maricopa County, AZ'

########

HOTWIRE_TOGGLE_LABELS = [
        "Network",
        "Cabinets",
        "0 - 1 Mile",
        "1 - 2 Miles",
        "2 - 5 Miles",
        "> 5 Miles"
]

HOTWIRE_TOGGLE_DEFAULT_OFF = [
        "0 - 1 Mile",
        "1 - 2 Miles",
        "2 - 5 Miles",
        "> 5 Miles",
        "Cabinets"
]

HOT_WIRE_CABINET_LABEL = [
        "Cabinets"
]


ALASKA_TOGGLE_LABELS = [
        "Copper",
        "Fiber",
        "Unknown",
        "Manhole",
        "Handhole",
        "Building Terminal",
        "Cross Connect",
        "Ready Access Terminal",
        "Splice",
        "Pedestal",
        "DLC",
        "Remote",
        "Pedestal W/Stub Pole",
        "Cabinet Location",
        "Cut Cap",
        "Virtual",
        "Fiber Terminal",
        "Dead End",
        "Main Distribution Frame"
]

#
ALASKA_TOGGLE_LABELS_DEFAULT_OFF = [
        "Building Terminal",
        "Cross Connect",
        "Ready Access Terminal",
        "Pedestal",
        "DLC",
        "Remote",
        "Pedestal W/Stub Pole",
        "Cabinet Location",
        "Cut Cap",
        "Virtual",
        "Fiber Terminal",
        "Dead End",
        "Main Distribution Frame"

]

#
ALASKA_TOGGLE_LABELS_OFF = [
        "Copper",
        "Fiber",
        "Unknown",
        "Manhole",
        "Handhole",
        "Splice"
]


#Alaska
ALASKA_NETWORK_TOGGLE_LABEL = [
        "Copper",
        "Fiber",
        "Unknown"
]

ALASKA_NETWORK_TOGGLE_EXPECTED_LABEL = [
        "Copper",
        "Fiber",
        "Unknown"
]

#Alaska junctions toggle
ALASKA_JUNCTION_TOGGLE_LABEL = [
        "Manhole",
        "Handhole",
        "Building Terminal",
        "Cross Connect",
        "Ready Access Terminal",
        "Splice",
        "Pedestal",
        "DLC",
        "Remote",
        "Pedestal W/Stub Pole",
        "Cabinet Location",
        "Cut Cap",
        "Virtual",
        "Fiber Terminal",
        "Dead End",
        "Main Distribution Frame"
]


ALASKA_JUNCTION_TOGGLE_EXPECTED_LABEL = [
        "Manhole",
        "Handhole",
        "Building Terminal",
        "Cross Connect",
        "Ready Access Terminal",
        "Splice",
        "Pedestal",
        "DLC",
        "Remote",
        "Pedestal W/Stub Pole",
        "Cabinet Location",
        "Cut Cap",
        "Virtual",
        "Fiber Terminal",
        "Dead End",
        "Main Distribution Frame"
]

#lcp toggle
LCP_TOGGLE_LABEL = [
        "LCP Locations"
]

#new dev units
NEW_DEV_UNITS_TOGGLE_LABELS = [
        "No Data",
        "1-25",
        "26-75",
        "76-250",
        "251-1000",
        ">1000"
]

POINT_LABELS = [
    "Lateral Network",
    "Backbone Network",
    "Splice Points",
    "Boundaries",
    "Coverage Area",
    "0-1 Mile",
    "1-2 Miles",
    ">2 Miles"
]

#KINETIC LENS
KINETIC_TOGGLE_LABELS = [
        "Network",
        "Splice Points"
]


RITTER_LABELS = [
        "Areas",
        "Fiber",
        "Coax"
]

# NEW_DEV_CABLE_ONE = [
#     "Within Cable One Coverage Area",    #"Coverage Area",
#     "1 Mile",
#     "2 Mile",
#     ">2 Mile"
# ]
NEW_DEV_CABLE_ONE = [
        # "Within Cable One Coverage Area",   #"Coverage Area",
        "Coverage Area",
        "0-1 Mile",    #newly added
        "1-2 Miles", #1 Mile", #"2 Miles",  removed
        ">2 Miles"
]

CSPIRE_LABELS = [
    "Network",
    "Splice Points"
]

