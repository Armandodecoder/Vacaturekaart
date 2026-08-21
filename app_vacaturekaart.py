import math
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Vacature Kaart — Finance & Controlling", layout="wide")

# ---------------------------------------------------------------------------
# Dataset: handmatig verzamelde vacatures (momentopname, geen live feed)
# ---------------------------------------------------------------------------
JOBS = [
    # Overijssel / Twente
    {"title": "Financial- of Business Controller", "company": "Randstad (diverse opdrachtgevers)", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": 4000, "salary_max": 7000, "url": "https://www.randstad.nl/vacatures/697632/financial--of-business-controller,-vast-dienstverband"},
    {"title": "Assistent Controller", "company": "Theaterhotel Almelo", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-overijssel-vacatures.html"},
    {"title": "Assistent Financial Controller (24–32u)", "company": "Werkgever in Almelo", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-overijssel-vacatures.html"},
    {"title": "Financial Controller | Finance & Automatisering", "company": "SKOR", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://www.werkzoeken.nl/vacature/13620250-financial-controller-finance-automatisering/"},
    {"title": "Financial Controller", "company": "Cogas", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://vacatures-almelo.nl/vacature/financial-controller-cogas-almelo/"},
    {"title": "Senior Business Controller", "company": "Opdrachtgever via CareerValue", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": 6500, "url": "https://www.careervalue.nl/vacatures/finance/vacature-in-almelo-senior-business-controller-tot-e-6500/"},
    {"title": "Controller Projectadministratie en Facturatie", "company": "Kader Group", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-overijssel-vacatures.html"},
    {"title": "Financial Controller (landelijke retailer)", "company": "Profilink-bemiddeling", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://profilink.nl/vacature/financial-controller-almelo/"},
    {"title": "Junior Controller", "company": "Universal Corrugated", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://nl.jooble.org/vacatures-financial-controller/Almelo"},
    {"title": "Business Controller", "company": "VDL ETG Almelo", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-twente-vacatures.html"},
    {"title": "Business Controller (vastgoedonderhoud)", "company": "Werkgever in Almelo", "city": "Almelo", "lat": 52.3569, "lon": 6.6622, "salary_min": 5900, "salary_max": 7500, "url": "https://www.adzuna.nl/overijssel/controller"},
    {"title": "Controller (big4-achtergrond gewenst)", "company": "4Sourcing / internationale organisatie", "city": "Zwolle", "lat": 52.5168, "lon": 6.0830, "salary_min": None, "salary_max": None, "url": "https://www.adzuna.nl/overijssel/controller"},
    {"title": "Senior Business Controller", "company": "Baker Tilly (Netherlands) B.V.", "city": "Zwolle", "lat": 52.5168, "lon": 6.0830, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-overijssel-vacatures.html"},
    {"title": "Parttime Controller (24–28u)", "company": "Werkgever in Zwolle", "city": "Zwolle", "lat": 52.5168, "lon": 6.0830, "salary_min": None, "salary_max": None, "url": "https://profilink.nl/vacatures/provincie-overijssel/functie-controller/"},
    {"title": "Financial Controller (Junior/Medior)", "company": "Webasto", "city": "Kampen", "lat": 52.5550, "lon": 5.9111, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-overijssel-vacatures.html"},
    {"title": "Assistent Controller", "company": "Werkgever in Raalte", "city": "Raalte", "lat": 52.3897, "lon": 6.2833, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-overijssel-vacatures.html"},
    {"title": "Financial Controller", "company": "Werkgever in Steenwijk/Wolvega", "city": "Steenwijk", "lat": 52.7864, "lon": 6.1197, "salary_min": 4000, "salary_max": 5500, "url": "https://profilink.nl/vacatures/provincie-overijssel/functie-controller/"},
    {"title": "Assistent Controller", "company": "Werkgever in Enschede", "city": "Enschede", "lat": 52.2215, "lon": 6.8937, "salary_min": None, "salary_max": None, "url": "https://profilink.nl/vacatures/provincie-overijssel/functie-controller/"},
    {"title": "Assistent Controller", "company": "Werkgever in Haaksbergen", "city": "Haaksbergen", "lat": 52.1517, "lon": 6.7439, "salary_min": None, "salary_max": None, "url": "https://financerecruitmentpartners.nl/vacatures/functie-financial-controller/provincie-overijssel/"},
    {"title": "Administrateur (financiële administratie)", "company": "Werkgever in Deventer", "city": "Deventer", "lat": 52.2550, "lon": 6.1639, "salary_min": None, "salary_max": None, "url": "https://financerecruitmentpartners.nl/vacatures/functie-financial-controller/provincie-overijssel/"},

    # Friesland / regio Sneek
    {"title": "Business Controller", "company": "Thuiszorg Het Friese Land", "city": "Leeuwarden", "lat": 53.2012, "lon": 5.7999, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/Controller-vacatures-in-Friesland"},
    {"title": "Junior Controller / Finance Manager", "company": "Sidijk", "city": "Heerenveen", "lat": 52.9594, "lon": 5.9181, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/Controller-vacatures-in-Friesland"},
    {"title": "Project Controller", "company": "SPIE Energies", "city": "Heerenveen", "lat": 52.9594, "lon": 5.9181, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/Controller-vacatures-in-Friesland"},
    {"title": "Business Controller Operations", "company": "Continental Candy Industries", "city": "Drachten", "lat": 53.1139, "lon": 6.0989, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-friesland-vacatures.html"},
    {"title": "Financieel Controller", "company": "Vakantiepark Westerbergen", "city": "Echten (Fr.)", "lat": 52.8494, "lon": 5.8686, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-friesland-vacatures.html"},
    {"title": "Credit Controller", "company": "Brunswick Corporation (Lankhorst)", "city": "Heerenveen", "lat": 52.9594, "lon": 5.9181, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-controller-l-friesland-vacatures.html"},
    {"title": "Financieel Controller", "company": "Beach Resort Makkum", "city": "Makkum", "lat": 53.0567, "lon": 5.4092, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-projectcontroller-l-friesland-vacatures.html"},
    {"title": "Assistent Financial Controller (24u)", "company": "Comecer", "city": "Joure", "lat": 52.9647, "lon": 5.7994, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-projectcontroller-l-friesland-vacatures.html"},
    {"title": "Senior Projectcontroller", "company": "NHL Stenden", "city": "Leeuwarden", "lat": 53.2012, "lon": 5.7999, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-project-controller-l-friesland-vacatures.html"},
    {"title": "Financieel Medewerker", "company": "Bureau Schmidt Ingenieurs en Adviseurs", "city": "Leeuwarden", "lat": 53.2012, "lon": 5.7999, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/Financial-Controller-vacatures-in-Friesland"},
    {"title": "Financial Controller", "company": "Van der Heide", "city": "Drachten", "lat": 53.1139, "lon": 6.0989, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/Financial-Controller-vacatures-in-Friesland"},
    {"title": "Project Controller", "company": "Van der Heide", "city": "Drachten", "lat": 53.1139, "lon": 6.0989, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/Financial-Controller-vacatures-in-Friesland"},
    {"title": "Business Controller", "company": "Epplejeck Horse & Rider Superstores", "city": "Heerenveen", "lat": 52.9594, "lon": 5.9181, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-business-controller-l-friesland-vacatures.html"},
    {"title": "Financieel Controller", "company": "Wagenborg Passagiersdiensten", "city": "Nes (Ameland)", "lat": 53.4381, "lon": 5.7681, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-financial-controller-l-friesland-vacatures.html"},
    {"title": "Project Controller", "company": "Fijn Wonen", "city": "Heerenveen", "lat": 52.9594, "lon": 5.9181, "salary_min": None, "salary_max": None, "url": "https://nl.indeed.com/q-financial-controller-l-friesland-vacatures.html"},
]

CITY_COORDS = {
    "almelo": (52.3569, 6.6622), "zwolle": (52.5168, 6.0830), "enschede": (52.2215, 6.8937),
    "hengelo": (52.2659, 6.7930), "deventer": (52.2550, 6.1639), "kampen": (52.5550, 5.9111),
    "raalte": (52.3897, 6.2833), "steenwijk": (52.7864, 6.1197), "wolvega": (52.8814, 6.0022),
    "haaksbergen": (52.1517, 6.7439), "nijverdal": (52.3625, 6.4667), "rijssen": (52.3086, 6.5106),
    "oldenzaal": (52.3125, 6.9286), "borne": (52.2508, 6.7522), "wierden": (52.3597, 6.5947),
    "goor": (52.2447, 6.5992), "denekamp": (52.3853, 7.0106), "vroomshoop": (52.4436, 6.5867),
    "amsterdam": (52.3676, 4.9041), "utrecht": (52.0907, 5.1214), "rotterdam": (51.9244, 4.4777),
    "den haag": (52.0705, 4.3007), "arnhem": (51.9851, 5.8987), "nijmegen": (51.8425, 5.8528),
    "groningen": (53.2194, 6.5665), "apeldoorn": (52.2112, 5.9699), "sneek": (53.0331, 5.6553),
    "leeuwarden": (53.2012, 5.7999), "heerenveen": (52.9594, 5.9181), "drachten": (53.1139, 6.0989),
    "joure": (52.9647, 5.7994), "makkum": (53.0567, 5.4092), "bolsward": (53.0619, 5.5253),
    "workum": (52.9819, 5.4394), "ijlst": (53.0089, 5.6864), "franeker": (53.1875, 5.5406),
    "harlingen": (53.1739, 5.4183), "stavoren": (52.8853, 5.3564), "grou": (53.0919, 5.8422),
}


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def salary_label(row):
    if row["salary_min"] and row["salary_max"]:
        return f"€ {row['salary_min']:,.0f} – € {row['salary_max']:,.0f} / mnd".replace(",", ".")
    if row["salary_max"]:
        return f"tot € {row['salary_max']:,.0f} / mnd".replace(",", ".")
    if row["salary_min"]:
        return f"vanaf € {row['salary_min']:,.0f} / mnd".replace(",", ".")
    return "salaris niet vermeld"


df = pd.DataFrame(JOBS)

# ---------------------------------------------------------------------------
# Sidebar: filters
# ---------------------------------------------------------------------------
st.sidebar.title("Vacature Kaart")
st.sidebar.caption("Finance & Controlling · Overijssel + Friesland · momentopname 21 aug 2026")

address = st.sidebar.text_input("Jouw adres / plaats", placeholder="bv. Sneek, Almelo, Zwolle...")

user_loc = None
key = address.strip().lower()
if key:
    match = next((c for c in CITY_COORDS if key in c or c in key), None)
    if match:
        user_loc = CITY_COORDS[match]
        st.sidebar.success(f"📍 Locatie gevonden: {match.title()}")
    else:
        st.sidebar.warning("Plaats niet herkend — afstandsfilter staat uit.")

max_distance = st.sidebar.slider("Max. afstand (km)", 0, 150, 150, step=5, disabled=user_loc is None)

functie = st.sidebar.text_input("Functie / trefwoord", placeholder="bv. junior, credit, treasury...")

companies = ["Alle bedrijven"] + sorted(df["company"].unique().tolist())
company_choice = st.sidebar.selectbox("Bedrijf", companies)

salary_min_input = st.sidebar.number_input("Min. salaris (€/mnd)", min_value=0, value=0, step=250)
salary_max_input = st.sidebar.number_input("Max. salaris (€/mnd)", min_value=0, value=0, step=250,
                                            help="0 = geen bovengrens")

if st.sidebar.button("Filters resetten"):
    st.rerun()

# ---------------------------------------------------------------------------
# Filteren
# ---------------------------------------------------------------------------
filtered = df.copy()

if company_choice != "Alle bedrijven":
    filtered = filtered[filtered["company"] == company_choice]

if functie:
    f = functie.lower()
    filtered = filtered[
        filtered["title"].str.lower().str.contains(f) | filtered["company"].str.lower().str.contains(f)
    ]

if salary_min_input > 0:
    filtered = filtered[filtered["salary_max"].isna() | (filtered["salary_max"] >= salary_min_input)]

if salary_max_input > 0:
    filtered = filtered[filtered["salary_min"].isna() | (filtered["salary_min"] <= salary_max_input)]

if user_loc:
    filtered["distance_km"] = filtered.apply(
        lambda r: haversine(user_loc[0], user_loc[1], r["lat"], r["lon"]), axis=1
    )
    filtered = filtered[filtered["distance_km"] <= max_distance]
else:
    filtered["distance_km"] = None

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
st.title("Vacature Kaart — Finance & Controlling")
st.caption(f"{len(filtered)} vacature(s) gevonden · verzameld via internetzoekopdrachten, geen live feed")

col_map, col_list = st.columns([2, 1])

with col_map:
    center = user_loc if user_loc else (52.6, 6.0)
    zoom = 9 if user_loc else 8
    m = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron")

    for _, row in filtered.iterrows():
        popup_html = f"""
        <b>{row['title']}</b><br>
        <span style='color:#0ea5a5'>{row['company']}</span><br>
        📍 {row['city']}<br>
        💰 {salary_label(row)}<br>
        <a href="{row['url']}" target="_blank">Bekijk bron ↗</a>
        """
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color="#0ea5a5",
            fill=True,
            fill_color="#5eead4",
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=250),
        ).add_to(m)

    if user_loc:
        folium.CircleMarker(
            location=user_loc,
            radius=9,
            color="#f59e0b",
            fill=True,
            fill_color="#f59e0b",
            fill_opacity=0.9,
            popup="📍 Jouw locatie",
        ).add_to(m)

    st_folium(m, width=None, height=560, returned_objects=[])

with col_list:
    st.subheader("Resultaten")
    if filtered.empty:
        st.info("Geen vacatures binnen de huidige filters.")
    for _, row in filtered.iterrows():
        with st.container(border=True):
            st.markdown(f"**{row['title']}**")
            st.caption(f"{row['company']} · {row['city']}")
            st.markdown(f":green[{salary_label(row)}]")
            if row["distance_km"] is not None:
                st.caption(f"± {row['distance_km']:.0f} km")
            st.link_button("Bekijk bron ↗", row["url"])

st.divider()
st.caption(
    "Deze set is handmatig samengesteld op basis van een gerichte internetzoekopdracht "
    "(Indeed, LinkedIn, Randstad, Adzuna, Profilink, FinanceRecruitmentPartners e.a.) — "
    "geen live-koppeling met vacaturesites. Salarisranges en locaties zijn indicaties "
    "zoals vermeld door de bron."
)
