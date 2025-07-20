import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from dotenv import load_dotenv
import requests

load_dotenv()

FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")
ORGANIZER_PHONE = os.getenv("ORGANIZER_PHONE")  # e.g., "9876543210"
UPI_ID = os.getenv("UPI_ID") or "dummy@upi"
PAYEE_NAME = os.getenv("PAYEE_NAME") or "Ganpati Utsav"

st.title("🕉️ Ganpati Utsav Donation Portal")

st.markdown("🙏 Your support helps us organize the Ganpati festival in our community.")

amount = st.number_input("Enter donation amount (₹)", min_value=1, step=1)
if st.button("Donate via UPI"):
    upi_link = f"upi://pay?pa={UPI_ID}&pn={PAYEE_NAME}&am={amount}&cu=INR"
    st.markdown(
    f'<a href="{upi_link}" target="_blank" style="font-size:18px;color:green;text-decoration:underline;">Click here to Donate ₹{amount}</a>',
    unsafe_allow_html=True
)

st.markdown("---")
st.header("✅ Confirm Your Donation")

with st.form("donor_form"):
    name = st.text_input("Your Name")
    mobile = st.text_input("Your Mobile Number")
    donated_amount = st.number_input("Donated Amount (₹)", min_value=1, step=1)
    txn_id = st.text_input("UPI Transaction ID (optional)")

    submitted = st.form_submit_button("Submit Confirmation")
    if submitted:
        # Save to CSV
        donor_data = {
            "name": name,
            "mobile": mobile,
            "amount": donated_amount,
            "transaction_id": txn_id
        }
        df = pd.DataFrame([donor_data])
        csv_file = "donors.csv"
        if os.path.exists(csv_file):
            df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_file, index=False)

        # Send SMS to donor
        donor_msg = f"Thank you {name} for donating ₹{donated_amount} to Ganpati Utsav. Your support means a lot!"
        organizer_msg = f"New donation from {name}: ₹{donated_amount}. Phone: {mobile}"

        headers = {
            'authorization': FAST2SMS_API_KEY,
            'Content-Type': "application/x-www-form-urlencoded"
        }

        def send_sms(message, phone):
            payload = f"sender_id=FSTSMS&message={message}&language=english&route=p&numbers={phone}"
            try:
                requests.post("https://www.fast2sms.com/dev/bulkV2", data=payload, headers=headers)
            except Exception as e:
                st.error(f"Error sending SMS: {e}")

        send_sms(donor_msg, mobile)
        send_sms(organizer_msg, ORGANIZER_PHONE)

        st.success("🎉 Thank you! Your confirmation has been received and SMS sent.")