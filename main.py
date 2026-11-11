from urllib.parse import quote
import streamlit as st
import base64
from pathlib import Path
st.set_page_config(
    page_title="CineMind",
    page_icon="🎬",
    layout="wide"
)


# Movie database (Filipino movie collection)
movies = [
    {
        "title": "Rewind",
        "genre": "Drama",
        "year": 2023,
        "poster": "https://m.media-amazon.com/images/M/MV5BOWI4OTQwOTktNmE5NS00MWU1LTk2ZmEtZDk4NmE4YjUyNGZhXkEyXkFqcGc%40._V1_.jpg",
        "description": "Rewind follows the story of John, a husband and father whose busy career and personal ambitions gradually create distance between him and his wife, Mary. As their relationship struggles, John begins to realize how much he has neglected the people who matter most to him. After a tragic event changes everything, he is unexpectedly given an opportunity to travel back in time and make different choices. With another chance to revisit important moments in his life, John must confront his mistakes, rediscover the meaning of love, and understand the value of time spent with family. The film explores marriage, sacrifice, forgiveness, and the importance of appreciating loved ones before it is too late."
    },
    {
        "title": "Hello, Love, Goodbye",
        "genre": "Romance",
        "year": 2019,
        "poster": "https://m.media-amazon.com/images/M/MV5BN2Y0YTA4N2QtMTkyZi00ZTI5LTgzZWEtY2ZiMTAxMjAzYjk3XkEyXkFqcGc%40._V1_.jpg",
        "description": "Hello, Love, Goodbye tells the story of Joy, a hardworking Filipino domestic helper living in Hong Kong who dreams of building a better future abroad. Focused on earning money and supporting her family, she has little time for relationships or personal happiness. Her life takes an unexpected turn when she meets Ethan, a bartender who is also a Filipino migrant worker trying to find his own direction in life. As the two grow closer, they discover feelings that challenge their individual plans and priorities. However, their different dreams and responsibilities force them to make difficult decisions about love and the future. The film explores the experiences of overseas Filipino workers, personal ambition, sacrifice, and the difficult balance between choosing love and pursuing one's dreams."
    },
    {
        "title": "Four Sisters and a Wedding",
        "genre": "Comedy",
        "year": 2013,
        "poster": "four_sisters.jpg",
        "description": "Four Sisters and a Wedding follows the Salazar siblings, particularly four sisters who are surprised to discover that their younger brother, CJ, is planning to get married. Concerned about his decision, the sisters reunite and attempt to convince him to reconsider the wedding. As they spend time together preparing for the occasion, old arguments, hidden frustrations, and unresolved family issues begin to surface. Each sister has her own struggles, insecurities, and personal expectations, making their reunion more complicated than they imagined. Beneath the humor and heated arguments lies a deeper story about sibling relationships, family pressure, jealousy, forgiveness, and acceptance. The film shows that even families who constantly disagree can still find their way back to one another."
    },
    {
        "title": "Seven Sundays",
        "genre": "Family",
        "year": 2017,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTk1NGYzMjMtZDcxYS00YzBhLTg1ZTUtZDI4NDJkN2MwMDM0XkEyXkFqcGc%40._V1_.jpg",
        "description": "Seven Sundays centers on the Bonifacio family, whose four adult children have grown distant from one another as they pursue their own lives and responsibilities. Their routine changes when their father, Manuel, reveals that he has a serious illness. Worried about his remaining time, the siblings decide to spend their Sundays together as a family. What begins as an attempt to make their father happy soon becomes an opportunity to confront years of misunderstandings, disappointments, and unresolved conflicts. As the family reunites, each sibling must face personal struggles while learning to understand the people they once knew so well. The film highlights the importance of family, forgiveness, communication, and making time for loved ones despite life's challenges."
    },
    {
        "title": "Feng Shui",
        "genre": "Horror",
        "year": 2004,
        "poster": "https://m.media-amazon.com/images/M/MV5BODVmMzA2ZGMtOGE2Mi00Yjk2LWExMTUtYTVjZDA2MWY1NmVjXkEyXkFqcGc%40._V1_FMjpg_UX1000_.jpg",
        "description": "Feng Shui follows Joy Ramirez, a woman whose ordinary life takes an unexpected turn after she discovers an antique Bagua mirror. Believing the mirror may bring good fortune, she takes it home and soon experiences a series of surprising events that appear to improve her family's circumstances. However, the happiness does not last long when strange and frightening incidents begin happening to people connected to the mirror. Joy gradually discovers that the object carries a mysterious curse connected to Chinese zodiac signs. As she investigates its dark history, she realizes that the fortune it offers comes with a terrifying price. The film combines supernatural horror, suspense, and Filipino cultural beliefs to explore greed, superstition, and the consequences of seeking luck without understanding its cost."
    }
]

# Session state
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

# Check if a movie poster was clicked
selected_title = st.query_params.get("movie")

if selected_title:
    for movie in movies:
        if movie["title"] == selected_title:
            st.session_state.selected_movie = movie
            break

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #0b0b0e;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #141418;
    border-right: 1px solid #29292f;
}

h1, h2, h3 {
    color: white;
}

p, label {
    color: #c5c5cc;
}

/* General buttons */
div.stButton > button {
    background-color: #e50914;
    color: white;
    border: none;
    border-radius: 8px;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #ff2934;
    color: white;
}

/* Premium sidebar navigation */
section[data-testid="stSidebar"] div.stButton > button {
    background-color: #1c1c22 !important;
    color: #c5c5cc !important;
    border: 1px solid #303038 !important;
    border-radius: 10px !important;
    text-align: left;
    padding: 12px 16px;
    font-weight: 600;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #29292f !important;
    color: white !important;
    border-color: #e50914 !important;
}

div[data-testid="stTextInput"] input {
    background-color: #19191f;
    color: white;
    border: 1px solid #38383f;
    border-radius: 10px;
}

.hero {
    background: linear-gradient(90deg, #270609, #141418 75%);
    border: 1px solid #4a151b;
    padding: 35px;
    border-radius: 16px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    color: white;
}

.hero p {
    color: #ccccd2;
    font-size: 17px;
}

/* CineMind logo */
.cinemind-logo {
    color: white;
    font-size: 32px;
    font-weight: 800;
    text-decoration: none;
    cursor: pointer;
}

.cinemind-logo:hover {
    color: #e50914;
}
/* Movie poster hover animation */
a:has(img) {
    display: block;
    position: relative;
    z-index: 1;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 10px;
}

a:has(img):hover {
    transform: scale(1.06);
    z-index: 10;
    box-shadow: 0 10px 30px rgba(229, 9, 20, 0.35);
}

a:has(img) img {
    transition: filter 0.3s ease;
}

a:has(img):hover img {
    filter: brightness(1.12);
}
}
</style>
""", unsafe_allow_html=True)

# Sidebar
if "navigation" not in st.session_state:
    st.session_state.navigation = "Home"

with st.sidebar:

    st.markdown("""
    <div class="cinemind-logo">
        🎬 CineMind
    </div>
    """, unsafe_allow_html=True)

    st.caption("DISCOVER YOUR NEXT FAVORITE")

    st.markdown("---")

    pages = ["Home", "My List"]

    for item in pages:
        is_active = st.session_state.navigation == item

        if st.button(
            f"{'▶' if is_active else '　'}  {item}",
            key=f"nav_{item}",
            use_container_width=True
        ):
            st.session_state.navigation = item
            st.rerun()

    page = st.session_state.navigation

    st.markdown("---")
    st.caption("CineMind Movie Recommendation System")
    st.caption("Made with Python")

# Check whether a movie was selected
selected_title = st.query_params.get("movie")

selected_movie = None

if selected_title:
    for movie in movies:
        if movie["title"] == selected_title:
            selected_movie = movie
            break

# MOVIE DETAILS PAGE
if selected_movie:

    if st.button("← Back to Movies"):
        st.query_params.clear()
        st.rerun()

    st.markdown("---")

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.image(
            selected_movie["poster"],
            width="stretch"
        )

    with col2:
        st.title(selected_movie["title"])

        st.markdown(
            f"**{selected_movie['genre']}  •  {selected_movie['year']}**"
        )

        st.markdown("---")

        st.subheader("Movie Overview")

        st.write(selected_movie["description"])

        st.markdown("---")

        if selected_movie["title"] in st.session_state.favorites:
            if st.button("♥ Saved", key="detail_save"):
                st.session_state.favorites.remove(selected_movie["title"])
                st.rerun()
        else:
            if st.button("♡ Add to My List", key="detail_save"):
                st.session_state.favorites.append(selected_movie["title"])
                st.rerun()

# NORMAL MOVIE COLLECTION
else:

    # Search and genre
    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input(
            "Search movies",
            placeholder="Search for a movie..."
        )

    with col2:
        genre = st.selectbox(
            "Choose Genre",
            ["All", "Action", "Sci-Fi", "Drama",
             "Romance", "Comedy", "Family", "Horror"]
        )

    # Choose movies based on page
    if page == "My List":
        st.subheader("♥ My List")

        display_movies = [
            movie for movie in movies
            if movie["title"] in st.session_state.favorites
        ]

    else:
        if page == "Discover":
            st.subheader("Discover Movies")
        else:
            st.subheader("Top Picks For You")

        display_movies = movies

    # Apply filters
    display_movies = [
        movie for movie in display_movies
        if search.lower() in movie["title"].lower()
        and (genre == "All" or movie["genre"] == genre)
    ]

    # Display movies
    if display_movies:

        columns = st.columns(3)

        for index, movie in enumerate(display_movies):

            with columns[index % 3]:

                poster = movie["poster"]

                # Support both online and local posters
                if poster.startswith("http"):
                    image_src = poster
                else:
                    image_data = base64.b64encode(
                        Path(poster).read_bytes()
                    ).decode()

                    image_src = f"data:image/jpeg;base64,{image_data}"

                st.markdown(
                    f"""
                    <a href="?movie={quote(movie['title'])}" target="_self">
                        <img src="{image_src}"
                             style="width:100%; height:420px;
                                    object-fit:cover;
                                    border-radius:10px;
                                    cursor:pointer;">
                    </a>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(f"### {movie['title']}")
                st.caption(f"{movie['genre']} • {movie['year']}")

                if movie["title"] in st.session_state.favorites:
                    button_label = "♥ Saved"
                else:
                    button_label = "♡ Save"

                if st.button(
                    button_label,
                    key=f"save_{movie['title']}"
                ):
                    if movie["title"] in st.session_state.favorites:
                        st.session_state.favorites.remove(movie["title"])
                    else:
                        st.session_state.favorites.append(movie["title"])

                    st.rerun()

                st.divider()

    else:
        st.info("No movies found. Try another search or genre.")
