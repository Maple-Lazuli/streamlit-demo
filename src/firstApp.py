import streamlit as st

# Title of the app
st.title("Number Repeater")

# Prompt user for a number
num = st.number_input("Enter a number:", min_value=1, step=1)

# Display the repeated number
if st.button("Display"):
    if num == 6:
        st.write("Whoa, how did you know???")
    else:
        st.write("Try again....")