import pandas as pd
import streamlit as st
from my_dataloader import get_data as gd
from base_setup import MyTraderBacktesting
from time_measure import timeit


# TITLE
st.title("Money Tree by Bhushan")
st.header("Fun with Money")
st.image("https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_960_720.jpg", caption="P&B Money Tree",)


# Loading data
scripts = None  # initial value
db = pd.DataFrame()
period_years = 3  # 1 year of data


@st.cache
def load_data(tickers):
    print(f"Selected tickers are: {tickers}")
    if len(tickers) > 0:
        return gd.GetData.get_data_from_list(tickers, period=f'{period_years}y')


def load_data_callback(tickers):
    global db
    db = load_data(tickers)


# def load_pdr_data(tickers):
#     global db
#     db = gd.GetData.get_data_pdr(tickers, period='1y')

# SCRIPT SELECTION CONTAINER


scriptSelection = st.container()
scriptSelection.subheader("Enter comma separated scripts")
with scriptSelection:
    new_scripts = scriptSelection.text_input(label="Scripts list", value=scripts)
    if new_scripts != scripts:
        scripts = new_scripts
        load_new = True
    st.text("For Indian Stocks, enter '.NS' at the end. Ex: TATAMOTORS.NS")
    st.button(label="Submit", on_click=load_data_callback(scripts))

# Display CONTAINER
display = st.container()
with display:
    if st.checkbox("Show Data"):
        st.write(db)

    db.columns = db.columns.to_flat_index()  # Convert the indices to flat
    headers = db.columns

    if len(headers) > 6:
        close = []
        for head in headers:
            if 'Close' in head:
                close.append(head)
        st.subheader(f"Closing prices for {scripts}")
        st.line_chart(db[close])
    else:
        st.subheader(f"Close price for {scripts}")
        st.line_chart(db['Close'])


# CEREBRO Container
trader = st.container()
with trader:
    st.title("Trader Runs")
    myTrader = MyTraderBacktesting(data=db)

    if st.button("Run Backtesting"):
        print("Running Backtest...")

        stats = myTrader.run_backtest()

        st.subheader("Summary of Trade")
        st.code(stats)

        st.subheader("Plot of Trades")
        st.write(myTrader.get_plot_of_trades())

        st.subheader("Optimize SMA")
        optimize_stats = myTrader.optimize_sma()

        st.subheader("Best strategy")
        st.code(optimize_stats['_strategy'])

        st.subheader("All Trades")
        with st.expander("Open to see all trades"):
            st.code(optimize_stats['_trades'])






    # Metric Display
    # col1, col2, col3 = st.columns(3)
    # initial_value = myTrader.initial_cash
    # current_value = myTrader.portfolio_value()
    # with col1:
    #     st.metric(label="Current Portfolio($)", value=current_value.__round__(2),
    #               delta=(current_value - initial_value).__round__(2))
    # with col2:
    #     per = (current_value - initial_value) * 100 / initial_value
    #     st.metric(label="Percentage Change(%)", delta=per.__round__(2), value=(per + 100).__round__(2))
    #
    # with col3:
    #     st.metric(label=scripts + "(yrs)", value=period_years)






# if isinstance(headers, pandas.core.indexes.multi.MultiIndex):