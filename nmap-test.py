import streamlit as st
import subprocess

def run_nmap(target):
    try:
        # Run the Nmap command and capture the output
        result = subprocess.run(['nmap', target], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title("Nmap Streamlit App")
    
    # Get the target from the user
    target = st.text_input("Enter target IP or domain:", "")

    if st.button("Run Nmap"):
        # Display the Nmap output
        st.text("Running Nmap...")
        output = run_nmap(target)
        st.text("Nmap Output:")
        st.text(output)

if __name__ == "__main__":
    main()
