import streamlit as st 
from streamlit.components.v1 import html

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


# from https://gist.github.com/treuille/2ce0acb6697f205e44e3e0f576e810b7
def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.
        
    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % str(int(i) + 1)
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    import itertools
    return itertools.islice(enumerate(items), min_index, max_index)



def render_header() -> None:
    st.set_page_config(layout="wide", page_title="PICO-db contact renders")
    st.markdown("## PICO-db contact renders")
    # st.write("Use the sidebar to change page to load other resources.")
    # st.markdown("#### ")
    st.write("Use the filters to narrow down the results. Switch pages on the sidebar.")
    st.markdown("#### ")
    return None


def render_webpage():
    render_header()

    # render sidebar
    with st.sidebar:
        page_size = st.slider("Items per page", min_value=5, max_value=100, value=10, step=5)


    # read list of lines from the file
    with open("../done_images.txt", "r") as f:
        allrows = f.readlines()
    allrows = [x.strip() for x in allrows]
    allrows = [x for x in allrows if x]

    # Object categories
    object_cats = [x.split("__")[0] for x in allrows]
    # Selectbox for object category with reset logic
    option_obj = st.selectbox(
        "Filter for object category:",
        [""] + sorted(set(object_cats)),
        index=0,
        key='option_obj',
        on_change=lambda: st.session_state.update(search_filenames="")
    )

    # Text input for searching specific image with reset logic
    search_filenames = st.text_input(
        "OR search for a specific image ID:", 
        "", 
        key='search_filenames',
        on_change=lambda: st.session_state.update(option_obj="")
    )

    # Filtering logic
    if search_filenames:
        allrows_filtered = [x for x in allrows if search_filenames in x]
    elif option_obj:
        allrows_filtered = [x for x in allrows if x.startswith(option_obj + "__")]
    else:
        allrows_filtered = allrows


    st.write(f"Total of **{len(allrows)}** annotations, **{len(allrows_filtered)}** matching the current filter.")
    st.markdown("---")

    URL_PREFIX = 'https://hoirec.s3.eu-central-1.amazonaws.com/dataset_contact_renders'

    # Display all annotations
    for ind, imagename in paginator("Jump to a page", allrows_filtered, items_per_page=page_size):
        st.write(f"*Image:* **{imagename}**")
        # st.image(f"{URL_PREFIX}/{imagename}", use_container_width=True)
        zoomable_image(f"{URL_PREFIX}/{imagename}")
        st.markdown("---")
    

render_webpage()
