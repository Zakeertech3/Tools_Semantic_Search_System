import streamlit as st
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Tool Semantic Search",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    .stTextInput > div > div > input {
        background-color: #16213e;
        color: #e4e4e7;
        border: 1px solid #0f3460;
        border-radius: 8px;
    }
    .stTextArea > div > div > textarea {
        background-color: #16213e;
        color: #e4e4e7;
        border: 1px solid #0f3460;
        border-radius: 8px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e94560 0%, #533483 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(233, 69, 96, 0.4);
    }
    .result-card {
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border-left: 4px solid #e94560;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .result-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 12px rgba(233, 69, 96, 0.2);
    }
    .metric-container {
        background: linear-gradient(135deg, #533483 0%, #e94560 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .tag-badge {
        background: linear-gradient(90deg, #533483 0%, #0f3460 100%);
        color: #e4e4e7;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
    }
    h1 {
        background: linear-gradient(90deg, #e94560 0%, #533483 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #16213e;
        border-radius: 8px 8px 0 0;
        color: #94a3b8;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #e94560 0%, #533483 100%);
        color: white;
    }
    .stExpander {
        background-color: #16213e;
        border: 1px solid #0f3460;
        border-radius: 8px;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #e94560 0%, #533483 100%);
    }
    .stSlider > div > div > div {
        background-color: #0f3460;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Tool Semantic Search System")

tab1, tab2, tab3 = st.tabs(["Search Tools", "Add Tool", "Manage Tools"])

with tab1:
    st.markdown("### Discover Tools with AI-Powered Search")
    
    query = st.text_input(
        "Search Query",
        placeholder="e.g., machine learning framework, database for caching...",
        label_visibility="collapsed"
    )
    
    limit = st.slider("Results", min_value=1, max_value=20, value=5)
    
    if st.button("Search", use_container_width=True):
        if query:
            with st.spinner("Searching through tools..."):
                try:
                    response = requests.post(
                        f"{API_URL}/search/",
                        json={"query": query, "limit": limit}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"""<div class="metric-container">
                                <h3>{data['result_count']}</h3>
                                <p>Results Found</p>
                            </div>""", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""<div class="metric-container">
                                <h3>{data['response_time_ms']}ms</h3>
                                <p>Response Time</p>
                            </div>""", unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"""<div class="metric-container">
                                <h3>{datetime.now().strftime('%H:%M')}</h3>
                                <p>Search Time</p>
                            </div>""", unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        if data['results']:
                            for idx, result in enumerate(data['results'], 1):
                                st.markdown(f"""
                                <div class="result-card">
                                    <h3 style="color: #e94560; margin: 0;">#{idx} {result['name']}</h3>
                                    <p style="color: #cbd5e1; margin: 0.5rem 0;">{result['description']}</p>
                                    <div style="margin: 1rem 0;">
                                        {''.join([f'<span class="tag-badge">{tag}</span>' for tag in result['tags']])}
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="color: #94a3b8; font-size: 0.9rem;">Relevance Score</span>
                                        <span style="color: #e94560; font-weight: 700; font-size: 1.2rem;">{result['score']:.4f}</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No results found. Try a different query.")
                    else:
                        st.error("Search failed. Please try again.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Please enter a search query")

with tab2:
    st.markdown("### Add New Tool to Database")
    
    with st.form("add_tool_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Tool Name", placeholder="e.g., TensorFlow")
            tags_input = st.text_input("Tags", placeholder="ml, ai, framework (comma-separated)")
        
        with col2:
            description = st.text_area("Description", height=100, placeholder="Describe the tool...")
            metadata_input = st.text_area("Metadata (JSON)", value='{"category": "", "difficulty": "", "popularity": ""}', height=100)
        
        submitted = st.form_submit_button("Add Tool", use_container_width=True)
        
        if submitted:
            if name and description:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                
                try:
                    metadata = json.loads(metadata_input)
                except:
                    metadata = {}
                
                tool_data = {
                    "name": name,
                    "description": description,
                    "tags": tags,
                    "metadata": metadata
                }
                
                try:
                    response = requests.post(f"{API_URL}/tools/", json=tool_data)
                    
                    if response.status_code == 200:
                        st.success(f"Tool '{name}' added successfully!")
                        st.balloons()
                    else:
                        st.error("Failed to add tool")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
            else:
                st.warning("Please fill in name and description")

with tab3:
    st.markdown("### Manage Your Tools")
    
    if st.button("Refresh Tools List", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/tools/")
            
            if response.status_code == 200:
                tools = response.json()
                st.info(f"Total tools in database: {len(tools)}")
                
                for tool in tools:
                    with st.expander(f"{tool['name']}", expanded=False):
                        st.markdown(f"**Description:** {tool['description']}")
                        st.markdown(f"**Tags:** {', '.join(tool['tags'])}")
                        st.markdown(f"**ID:** `{tool['id']}`")
                        st.markdown(f"**Created:** {tool['created_at']}")
                        
                        if st.button(f"Delete", key=f"delete_{tool['id']}"):
                            delete_response = requests.delete(f"{API_URL}/tools/{tool['id']}")
                            if delete_response.status_code == 200:
                                st.success("Tool deleted")
                                st.rerun()
                            else:
                                st.error("Failed to delete tool")
            else:
                st.error("Failed to load tools")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")