import streamlit as st
import data_generator as dg
import network_plot as np
from datetime import timedelta

if "team" not in st.session_state:
    st.session_state.team = None
if "interactions" not in st.session_state:
    st.session_state.interactions = None
if "team_generated" not in st.session_state:
    st.session_state.team_generated = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

st.title("Zoo Keeper Exploration")

num_zoo_keepers = st.number_input("How many Zoo Keepers:", min_value=1, step=5, value=30)
num_assigned_animals = st.number_input("How many animals are they responsible for:", min_value=1, step=5, value=20)
num_malicious = st.number_input("How many of those Zoo Keepers are over zealous animal lovers:", min_value=1, step=1,
                                value=1)
num_days_worked = st.number_input("How many days were the Zoo Keepers working?", min_value=1, step=1, value=7)

if st.button("Create Team"):
    st.session_state.team = dg.generate_team(team_size=num_zoo_keepers, num_malicious=num_malicious)
    st.session_state.interactions = dg.generate_interactions(team=st.session_state.team,
                                                             num_team_animals=num_assigned_animals,
                                                             num_days=num_days_worked)
    st.session_state.team_generated = True
    st.markdown("***")

if st.session_state.team_generated:
    st.session_state.selected_option = st.selectbox(
        "Select a zoo keeper to review",
        st.session_state.team.keys())
    st.markdown(f"Rendering animal interactions for: **{st.session_state.selected_option}**")
    st.markdown("***")

# Display content for the selected zoo keeper
if st.session_state.selected_option is not None:
    start_date = min([i[2] for i in st.session_state.interactions])
    end_date = max([i[2] for i in st.session_state.interactions])

    current_date = start_date
    while current_date <= end_date:
        st.write(f"#### {current_date.strftime('%b %d, %Y')}")
        day_interactions = [i for i in st.session_state.interactions if i[2].date() == current_date.date()]
        pruned_interactions = dg.prune_interactions(day_interactions)
        st.plotly_chart(np.create_plotly_plot(pruned_interactions, selected_member=st.session_state.selected_option))
        current_date += timedelta(days=1)  # Move to the next day

    st.write(f"#### Entire Time Span")
    pruned_interactions = dg.prune_interactions(st.session_state.interactions)
    st.plotly_chart(np.create_plotly_plot(pruned_interactions, selected_member=st.session_state.selected_option))
