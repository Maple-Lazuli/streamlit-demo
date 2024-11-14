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


@st.cache_data
def render_plots(interactions, selected_zoo_keeper):
    start_date = min([i[2] for i in interactions])
    end_date = max([i[2] for i in interactions])

    current_date = start_date
    while current_date <= end_date:
        day_interactions = [i for i in interactions if i[2].date() == current_date.date()]
        pruned_interactions = dg.prune_interactions(day_interactions)
        st.plotly_chart(np.create_plotly_plot(pruned_interactions, selected_member=selected_zoo_keeper,
                                              title=current_date.strftime('%b %d, %Y')))
        current_date += timedelta(days=1)  # Move to the next day

    pruned_interactions = dg.prune_interactions(interactions)
    st.plotly_chart(np.create_plotly_plot(pruned_interactions, selected_member=selected_zoo_keeper,
                                          title="Entire Span"))


st.title("Zoo Manager Cost Cutting Tool")

st.write("""
You are a manager for a local zoo. Recently the marketing team ran a hiring ad campaign that was hyper effective and 
resulted in several animal loving zoo keepers being hired. Some of the zoo keepers are over zealous and are covering
for too many animals. This is a problem for you, as the extra work by the zoo keepers means higher wages due to their
hiring contract. Use the widgets below to model the staff and find the overly zealous animal lover that is going to
bankrupt the zoo. 
""")

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
    st.markdown("***")
    st.session_state.selected_option = st.selectbox(
        "Select a zoo keeper to review",
        st.session_state.team.keys())
    st.markdown(f"Rendering animal interactions for: **{st.session_state.selected_option}**")


# Display content for the selected zoo keeper

if st.session_state.selected_option is not None:
    render_plots(st.session_state.interactions, st.session_state.selected_option)

if st.session_state.team_generated:
    selection = st.selectbox(
        "Overly Zealous Zoo Keeper?",
        st.session_state.team.keys())

    if not st.session_state.team[selection]['legitimate']:
        st.write("You found an overly zealous zoo keeper doing too much work! They need to be fired before"
                 " they improve moral too much and make the zoo go bankrupt.")
    else:
        st.write("You found an average zoo keeper who periodically covers for others. They're a good person, but seem"
                 " too happy. They should probably be paid less.")
