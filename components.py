import streamlit as st


def page_card(title, description):
    """A card to be used in a page"""

    st.markdown("""
    <style>
        .card {
            /* Add shadows to create the "card" effect */
            background-color: rgba(58, 58, 58, 0.5);
            border-radius: 10px;
            padding: 10px;
            margin-block: 5px;
            width: 200px;
            height: 200px;
        }
        
        /* On mouse-over, add a deeper shadow */
        .card:hover {
            background-color: rgba(58, 58, 58, 0.3);
            transition: 0.1s ease-out all;
            border: 2px solid #3a1ca4;
        }
        
        .page {
            cursor: pointer;
            text-decoration: none;
            display: flex;
            flex-direction: column;
            align-items: center;  
        }
        .page:hover {
            text-decoration: none;
        }
        
        p{
            font-size: 12px;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    card = st.markdown(
        f"""
        <div class="card">
            <a class="page" target="_self" href="{'/'+ title.replace(' ', '%20')}">
                    <h5>{title}</h5>
                    <p>{description}</p>
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )

    return card
