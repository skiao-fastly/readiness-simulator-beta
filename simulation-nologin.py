import hmac
import streamlit as st
import subprocess

####### Authentication ########


####### Main App ##########

def run_vegeta_attack(user_input, rate, duration):
    command = f"echo 'GET {user_input}' | vegeta attack -header 'User-Agent: Fastly-CSOC' -rate {rate} -duration={duration}s | vegeta report --type=text"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def main():

    st.title("Readiness Simulator")

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
