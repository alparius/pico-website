import streamlit as st
from streamlit.components.v1 import html
import random

def zoomable_image(img_url):
    html(f"""
    <style>
    .zoom-container {{
        position: relative;
        overflow: hidden;
    }}
    .zoom-container img {{
        width: 100%;
        transition: transform 0.2s, transform-origin 0.2s;
        cursor: zoom-in;
    }}
    </style>
    <div class="zoom-container">
      <img src="{img_url}" 
           onmousedown="zoomIn(event, this)" 
           onmouseup="zoomOut(this)" />
    </div>
    <script>
    function zoomIn(e, img) {{
        const rect = img.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        img.style.transformOrigin = `${{x}}% ${{y}}%`;
        img.style.transform = "scale(3)";
    }}
    function zoomOut(img) {{
        img.style.transform = "scale(1)";
    }}
    </script>
    """, height=400)


def render_webpage():
    st.set_page_config(layout="wide", page_title="PICO-db contact renders")
    st.markdown("## PICO-db contact renders")
    st.write("Select an object category and click the button to view 3 random samples.")
    st.write("To zoom into an area, click and hold the left mouse button.")
    st.markdown("#### ")

    with open("../done_images.txt", "r") as f:
        allrows = [x.strip() for x in f if x.strip()]

    object_cats = sorted(set(x.split("__")[0] for x in allrows))
    cols = st.columns([1, 2, 1])
    with cols[0]:
        option_obj = st.selectbox("Select object category:", object_cats)

    if option_obj and st.button("Show random samples"):
        st.markdown("#### ")
        filtered = [x for x in allrows if x.startswith(option_obj + "__")]
        samples = random.sample(filtered, min(3, len(filtered)))
        URL_PREFIX = 'https://hoirec.s3.eu-central-1.amazonaws.com/dataset_contact_renders'
        for imagename in samples:
            st.write(f"*Image:* **{imagename}**")
            zoomable_image(f"{URL_PREFIX}/{imagename}")
            st.markdown("---")

render_webpage()
