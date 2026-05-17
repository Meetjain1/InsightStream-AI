"""Shared sidebar content shown on every dashboard page."""
import streamlit as st

_QUICK_START_TEXT = """
1. Load our awesome sample data or upload your own
2. Dive into dazzling visualizations
3. Run powerful SQL queries (no tech skills needed!)
4. Group customers and discover hidden patterns
5. Get brilliant ideas to boost your business
"""


def render_quick_start_guide(*, in_sidebar: bool = False):
    """Render the Quick Start Guide in the sidebar."""

    def _render():
        st.subheader("Quick Start Guide")
        st.markdown(_QUICK_START_TEXT)

    if in_sidebar:
        _render()
    else:
        with st.sidebar:
            _render()
