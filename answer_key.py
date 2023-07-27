import streamlit as st
import pandas as pd

def answer_key_setter(num_columns, num_rows):
    # Generate column names (A, B, C, ..., Z, AA, AB, ...)
    def generate_column_names(n):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = []
        while n >= 0:
            result.append(letters[n % 26])
            n = n // 26 - 1
        return ''.join(result[::-1])

    columns = [generate_column_names(i) for i in range(num_columns)]
    data = [[f"-" for col in columns] for row in range(num_rows)]
    df = pd.DataFrame(data, columns=columns)
    st.data_editor(df,width=1000,height=500)
    # return pd.DataFrame(data, columns=columns)

# Example usage:
# num_columns = 3
# num_rows = 5
# df = answer_key_setter(num_columns, num_rows)
# print(df)
