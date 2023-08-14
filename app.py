# -*- coding: utf-8 -*-
"""
Created on Sat Jun 6, 2023

Designed By: Ayodele Ayodeji
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun 6, 2023

Designed By: Ayodele Ayodeji
"""


import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page


page = st.sidebar.selectbox("Use the dropdown button bellow to Explore Or Predict", ("Predict", "Explore"))

if page == "Predict":
    show_predict_page()
else:
    show_explore_page()
    