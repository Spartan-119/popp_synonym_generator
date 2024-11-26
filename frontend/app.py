import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/generate-synonyms"

st.set_page_config(page_title="Popp Synonym Generator", page_icon=":mag_right:")

st.title("🔍 Popp - Synonym Generator")

st.markdown("""
    Welcome to the **Popp Synonym Generator**!  
    Enter a word below to generate the most relevant synonyms along with their similarity scores.
    This tool will help you explore word alternatives and improve your vocabulary!
""", unsafe_allow_html=True)

word = st.text_input("Type a word to get its synonyms:", "")

if word:
    with st.spinner("Fetching synonyms... Please wait."):
        # Send a POST request to FastAPI server
        response = requests.post(API_URL, json={"word": word})
        
        if response.status_code == 200:
            try:
                # Assuming the API returns a JSON object with a 'synonyms' field
                data = response.json()
                if 'synonyms' in data:
                    synonyms = data['synonyms']
                    
                    # Create a section to display the results
                    st.subheader("📝 Top Synonyms with Similarity Scores:")
                    
                    # Organize results into a nicely formatted table
                    synonym_df = []
                    for synonym, score in synonyms:
                        synonym_df.append([synonym, f"{score:.2f}"])
                    
                    # Display synonyms in a table format
                    st.table(synonym_df)
                else:
                    st.warning("No synonyms found.")
            except ValueError: # if there's something wrong
                st.error("Error decoding the response. Please check the API.")
        else:
            st.error(f"API error: {response.status_code}")

st.markdown("""
    ---
    Created with ❤️ by **Abin**    
    """, unsafe_allow_html=True)

# lousy Custom styling (adapt for dark theme using media queries) 
st.markdown("""
    <style>
        /* Adapt to dark theme */
        .stTextInput input {
            background-color: #f1f1f1;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton button {
            background-color: #007BFF;
            color: white;
            font-size: 14px;
            border-radius: 5px;
        }

        /* Table styling */
        .stTable th, .stTable td {
            color: var(--text-color);
            background-color: var(--primary-background-color);
        }

        /* Theme specific styles */
        @media (prefers-color-scheme: dark) {
            .stTextInput input {
                background-color: #333;
                color: white;
                border: 2px solid #444;
            }
            .stButton button {
                background-color: #0056b3;
                color: white;
            }
            .stTable th, .stTable td {
                color: #e0e0e0;
                background-color: #333;
            }
        }

        @media (prefers-color-scheme: light) {
            .stTextInput input {
                background-color: #f1f1f1;
                color: black;
                border: 2px solid #ddd;
            }
            .stButton button {
                background-color: #007BFF;
                color: white;
            }
            .stTable th, .stTable td {
                color: #333;
                background-color: #f0f0f0;
            }
        }
    </style>
""", unsafe_allow_html=True)
