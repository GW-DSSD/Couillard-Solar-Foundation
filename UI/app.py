import streamlit as st
import pandas as pd
import numpy as np
import mapping
import address_conversion



# Streamlit app
def main():
    st.title("Address to Coordinates Converter")

    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
    
    if uploaded_file is not None:
        df = address_conversion.convert_address_to_coords(uploaded_file)
        st.write("Coordinates DataFrame:", df)
        mapping.main(df)

        

        if st.button("Save as CSV"):
            df.to_csv("streamlit-test-coordinates_output.csv", index=False)
            st.success("CSV file saved successfully")

if __name__ == "__main__":
    main()