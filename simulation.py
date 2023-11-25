import hmac
import streamlit as st
import subprocess

####### Authentication ########

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.success("Logout Successful")
    return False

def logout():
    st.session_state["password_correct"] = False
    st.session_state["logout_clicked"] = True

####### Main App ##########

def run_vegeta_attack(user_input, rate, duration):
    command = f"echo 'GET {user_input}' | vegeta attack -header 'User-Agent: Fastly-CSOC' -rate {rate} -duration={duration}s | vegeta report --type=text"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def login_page():

    if check_password():
        st.button("Logout", on_click=logout)
    # else:
    #     st.warning("Invalid credentials. Please log in.")

def main():

    st.title("Readiness Simulator")

    # Check for logout
    if st.session_state.get("password_correct", False):
        if st.button("Logout", on_click=logout):
            st.session_state["password_correct"] = False

    # If not logged in, show the login page
    if not st.session_state.get("password_correct", False):
        login_page()
        st.stop()

    user_input = st.text_input("Enter the URL:")
    rate = st.number_input("Enter rate (requests per second):", min_value=1, value=10000, step=5)
    duration = st.number_input("Enter duration (seconds):", min_value=1, value=60)

    if st.button("Run simulator"):
        st.text("Running simulator...")
        output = run_vegeta_attack(user_input, rate, duration)
        st.text("Simulation Completed!")
        st.text("Simulation Output:")

        st.text_area("Report", value=output, height=400, max_chars=None)

if __name__ == "__main__":
    main()
