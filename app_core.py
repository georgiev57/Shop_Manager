import streamlit as st
import requests
from datetime import datetime, date
import time
from collections import Counter
from sales_manager import SalesManager

API_URL = "https://web-production-e4e6d.up.railway.app"
today = date.today().strftime('%Y-%m-%d')
now = datetime.now().strftime("%H:%M")
thin_space = "\u2009"

products = {
    "\ud83d\udcf1 Phone Bag": "Phone Bag",
    "\ud83d\udc5c Ital MK": "Ital MK",
    "\ud83c\udf92 CrossBody": "CrossBody Bag",
    "\ud83d\udcbc Wallet": "Wallet",
    "\ud83d\udc5b MK Purse": "MK Purse",
    "\ud83e\uddf5 Leather Purse": "Leather Purse"
}

price_ranges = {
    "\ud83d\udcf1 Phone Bag": list(range(15, 27)),
    "\ud83d\udc5c Ital MK": list(range(35, 46)),
    "\ud83c\udf92 CrossBody": list(range(20, 41)),
    "\ud83d\udcbc Wallet": list(range(10, 31)),
    "\ud83d\udc5b MK Purse": list(range(15, 21)),
    "\ud83e\uddf5 Leather Purse": list(range(30, 41)),
}

def spacer(px=20):
    st.markdown(f"<div style='height: {px}px;'></div>", unsafe_allow_html=True)

def format_time(ts):
    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

def run_app(shop_name):
    sales_manager = SalesManager(API_URL)

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "selected_item" not in st.session_state:
        st.session_state.selected_item = None
    if "selected_price" not in st.session_state:
        st.session_state.selected_price = None
    if "selected_quantity" not in st.session_state:
        st.session_state.selected_quantity = None

    with st.sidebar:
        st.markdown(f"## \ud83c\udfea {shop_name}")
        st.markdown(f"### \u2705 Logged in")
        st.write(f"\ud83d\uddd5\ufe0f {today}")
        st.write(f"\ud83d\udd52 {now}")
        st.markdown("---")
        if st.button("\ud83d\udd01 Switch Shop"):
            st.session_state.logged_in = False
            st.session_state.shop_name = ""
            st.rerun()

    if st.session_state.page == "Dashboard":
        st.markdown(f"""
            <div style='display:flex; justify-content:flex-end; margin-top:-2.5rem; margin-bottom:0.5rem;'>
                <span style='font-size:1.4rem; color:gray;'>\ud83d\udd52 {now}</span>
            </div>
        """, unsafe_allow_html=True)
        spacer(20)

        sales = sales_manager.get_today_sales(today)
        total_sales = sum(s["price"] * s["quantity"] for s in sales)
        last_sales = sorted(sales, key=lambda s: s["timestamp"], reverse=True)[:3]

        for i, sale in enumerate(reversed(last_sales)):
            sale_time = format_time(sale["timestamp"])
            st.markdown(
                f"""
                <div style='display:flex; justify-content:space-between; font-size:0.8rem; color:#999;'>
                    <span>{sale['product']}</span>
                    <span>{sale['price']} лв. × {sale['quantity']}</span>
                    <span>{sale_time}</span>
                </div>
                """, unsafe_allow_html=True
            )

        spacer(30)

        item_totals = {}
        for s in sales:
            item_totals[s["product"]] = item_totals.get(s["product"], 0) + s["price"] * s["quantity"]

        button_texts = []
        max_length = 0
        for label, db_value in products.items():
            total = f"{item_totals.get(db_value, 0)} лв."
            combined = f"{label} {total}"
            button_texts.append((label, db_value, total, combined))
            max_length = max(max_length, len(combined))

        cols = st.columns(3)
        for idx, (label, db_value, total, combined) in enumerate(button_texts):
            with cols[idx % 3]:
                pad_len = max_length - len(combined) + 2
                padded_label = label + ('\u2002' * pad_len)
                if st.button(f"{padded_label} {total}", key=f"btn_{db_value}"):
                    st.session_state.selected_item = label
                    st.session_state.page = "Select Price"
                    st.rerun()

        spacer(20)

        with st.expander(f"\ud83d\udccb Full Sales Today {thin_space} \ud83c\udf3f {thin_space} **{total_sales} лв**"):
            for s in reversed(sales):
                st.markdown(
                    f"<div style='display:flex; justify-content:space-between; font-size:0.85rem;'>"
                    f"<span>{s['product']}</span>"
                    f"<span>{s['price']} лв. × {s['quantity']}</span>"
                    f"<span>{format_time(s['timestamp'])}</span></div>",
                    unsafe_allow_html=True
                )

    if st.session_state.page == "Select Price":
        label = st.session_state.selected_item
        item_key = products[label]
        st.subheader(label)
        st.session_state.selected_quantity = st.number_input("Select Quantity", min_value=1, max_value=10, step=1)

        freq = sales_manager.get_price_frequency(item_key)
        for price in sorted(freq, key=freq.get, reverse=True):
            if st.button(f"{price} лв.", key=f"price_btn_{price}"):
                st.session_state.selected_price = price
                st.session_state.page = "Confirm Sale"
                st.rerun()

        st.markdown("### Or choose a new price:")
        price_opt = st.radio("\ud83d\udcb0 Select Price", price_ranges.get(label, range(5, 56)), horizontal=True)
        if st.button("\u27a1\ufe0f Use This Price"):
            st.session_state.selected_price = price_opt
            st.session_state.page = "Confirm Sale"
            st.rerun()

        if st.button("\u2b05\ufe0f Back"):
            st.session_state.page = "Dashboard"
            st.rerun()

    if st.session_state.page == "Confirm Sale":
        label = st.session_state.selected_item
        item_key = products[label]
        price = st.session_state.selected_price
        quantity = st.session_state.selected_quantity

        st.subheader("\u2705 Confirm Sale")
        st.markdown(f"**\ud83d\udcbc Item:** {label}")
        st.markdown(f"**\ud83d\udccf Quantity:** {quantity}")
        st.markdown(f"**\ud83d\udcb0 Price:** {price} лв.")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("\u2705 Confirm"):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                success = sales_manager.add_sale(item_key, price, quantity, timestamp)
                if success:
                    st.success("Sale recorded.")
                else:
                    st.error("Failed to record sale.")
                time.sleep(1)
                st.session_state.page = "Dashboard"
                st.rerun()

        with col2:
            if st.button("\u270f\ufe0f Edit"):
                st.session_state.page = "Select Price"
                st.rerun()

        with col3:
            if st.button("\u274c Cancel"):
                st.session_state.page = "Dashboard"
                st.session_state.selected_item = None
                st.session_state.selected_price = None
                st.session_state.selected_quantity = None
                st.rerun()

if __name__ == "__main__":
    st.set_page_config(page_title="Simple Shop App", layout="centered")
    st.title("🛍️ Simple Shop Dashboard")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        shop_name = st.text_input("Enter your shop name to log in:")
        if st.button("🔓 Log In") and shop_name.strip():
            st.session_state.shop_name = shop_name.strip()
            st.session_state.logged_in = True
            st.rerun()
    else:
        run_app(st.session_state.shop_name)