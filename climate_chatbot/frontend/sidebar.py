import streamlit as st
from static_components import LOGO

def sidebar():
    with st.sidebar:
        st.image(LOGO, width=50)
        st.markdown(
            "## How to use\n"
            "1. Ask Perspicue a question about a climate reporting framework such as TCFD💬\n"
            "2. Use Perspicue's deep knowledge of climate reporting to assist in compiling your company's climate related disclosures📜\n"
         )

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖Perspicue Climate is a purpose-built chat assistant designed to help you compile climate-related disclosures."
            "It has deep domain-specific knowledge of many prominent climate reporting frameworks such as TCFD"
            "and helps to digest long and difficult documentation into succinct and precise answers, telling you only"
            "exactly what you need to know."
        )
        st.markdown("---")
