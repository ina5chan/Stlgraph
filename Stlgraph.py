import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Streamlitアプリのタイトルを設定
st.title('Time Series Data Viewer')

# データをアップロードするためのファイルアップロードウィジェットを追加
uploaded_file = st.file_uploader(
    "CSVまたはExcelファイルをアップロードしてください", type=["csv", "xlsx"])

# ファイルがアップロードされた場合
if uploaded_file is not None:
    # データを読み込む
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file, engine='openpyxl')

    # データフレームの最初の5行を表示
    st.write("データの最初の5行:")
    st.write(df.head())

    # データフレームの列を選択するためのマルチセレクトウィジェットを追加
    selected_columns = st.multiselect("列を選択してください", df.columns)

    # 選択された列のデータを一つのグラフに重ねて表示
    if selected_columns:
        st.subheader("選択された列のグラフ:")
        fig = go.Figure()
        for column in selected_columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df[column], mode='lines', name=column))

        # 縦カーソルを追加
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1d", step="day",
                             stepmode="backward"),
                        dict(count=7, label="1w", step="day",
                             stepmode="backward"),
                        dict(count=1, label="1m", step="month",
                             stepmode="backward"),
                        dict(count=3, label="3m", step="month",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
            ),
            yaxis=dict(
                fixedrange=False,  # 縦に拡大縮小を有効にする
            )
        )

        # # Y軸の拡大縮小を有効にする
        # fig.update_yaxes(
        #     scaleanchor="x",  # x軸を基準に拡大縮小
        #     scaleratio=1,  # 拡大縮小比率
        # )
        st.plotly_chart(fig)

        for column in selected_columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, y=df[column], mode='lines', name=column))
            
            # グラフのレイアウトを設定
            fig.update_layout(
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1d", step="day",
                                stepmode="backward"),
                            dict(count=7, label="1w", step="day",
                                stepmode="backward"),
                            dict(count=1, label="1m", step="month",
                                stepmode="backward"),
                            dict(count=3, label="3m", step="month",
                                stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    # rangeslider=dict(visible=True),
                ),
                yaxis=dict(
                    fixedrange=False,  # 縦に拡大縮小を有効にする
                )
            )

            st.write(column)  # 列の名前を表示
            st.plotly_chart(fig)

st.write("© 2023 T.Inagawa")