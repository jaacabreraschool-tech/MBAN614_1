import streamlit as st

def render(df, df_raw, selected_year):

    st.markdown("""
    ### Our Mission
    We aim to provide clear, actionable HR analytics that empower stakeholders to make data-driven decisions.

    ### What This Dashboard Offers
    - Workforce trends and demographics
    - Attrition and retention insights
    - Career progression metrics
    - Survey and feedback analytics

    ### Why It Matters
    By combining academic rigor with practical business logic, this dashboard helps organizations
    understand employee journeys and optimize retention strategies.
    """)

    st.markdown("""
    ### Team & Acknowledgments
    This dashboard was developed as part of an advanced HR analytics project.
    Special thanks to mentors, colleagues, and stakeholders who provided guidance and feedback.
    """)

    st.info("This dashboard is a continuous project — feedback and collaboration are always welcome!")

    # Optional: add a logo or image
    # st.image("logo.png", width=200)

    # Optional: add contact info
    st.markdown("""
    **Contact Us**  
    📧 Email: adagustin@mymail.mapua.edu.ph, mcpacheco@mymail.mapua.edu.ph, jaacabrera@mymail.mapua.edu.ph

    📍 Location: 191 Pablo Ocampo Sr. Extension, Brgy. Sta. Cruz, Makati City, 1205 Metro Manila, Philippines
    """)
