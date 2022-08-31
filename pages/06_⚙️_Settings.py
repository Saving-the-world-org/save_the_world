import logging
import streamlit as st
from src.utils.dataio import get_data
import streamlit.components.v1 as components
from src.utils.dataio import init_data

# Begin Streamlit calls
st.set_page_config(layout="wide")

def main(df):
    #Header information 
    st.title("System Settings", anchor=None)
    st.markdown("Manage database, users, etc.")
    st.markdown("---")
    st.markdown("#### Recent Transactions:")

    st.markdown(f"  ```{df} ```")
    st.markdown("---")

    # st.write("coming soon")

    hvar = """
            <script>
                var elements = window.parent.document.querySelectorAll('.css-1q8dd3e')
                elements[0].innerText = 'done';
                elements[0].disabled = true;
            </script>
            """
    btn =  st.button("Reload Database Tables from CSV files")
    if btn:
        init_data()
        components.html(hvar, height=0, width=0)
        org_query="SELECT * FROM ORGANIZATIONS;"
        org_df = get_data(org_query)
        donations_query="SELECT * FROM DONATIONS;"
        donations_df = get_data(donations_query)
        transactions_query="SELECT * FROM TRANSACTIONS;"
        transactions_df = get_data(transactions_query)
        cities_query="SELECT * FROM CITIES;"
        cities_df = get_data(cities_query)
        st.write("---")
        st.write(org_df)
        st.write(donations_df)
        st.write(transactions_df)
        st.write(cities_df)


def load_data():
    transaction_query = "SELECT * FROM TRANSACTIONS LIMIT 10;"
    df = get_data(transaction_query)
    """TODO: reorder columns and sort rows by recent timestamp
    """
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)


# # @st.cache
# def load_data():
#     query_str = "SELECT * FROM DONATIONS;"
#     df = get_data(query_str)
#     return df

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.CRITICAL)
#     df = load_data()
#     main(df)