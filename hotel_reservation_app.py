# Import required libraries
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import time
import pandas as pd
import uuid

# Import helper and pinata functions
from pinata import pin_json_to_ipfs, convert_data_to_json
from functions import get_location, get_hotels

load_dotenv()

# Create instance of web3.py for communication to the Blockchain smart contract
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path("./contracts/compiled/hotel_reservation_registry_abi.json")) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Calling the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    return contract


contract = load_contract()

# Helper functions to pin files and json to Pinata


def pin_hotel_reservation(hotel_name):
    # Build a token metadata file for the Hotel Reservation
    token_json = {"name": hotel_name}
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_historical_price_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


# Function to display background image from a URL for frontend User friendly visualization
def add_bg_from_url():

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://cdn.galaxy.tf/unit-media/tc-default/uploads/images/room_photo/001/597/271/king-room-resort-tower-1600x1067-wide.jpg");
            background-attachement: fixed;
            background-size: cover
        }} 

        </style>
        """,
        unsafe_allow_html=True,
    )

add_bg_from_url()


### SECTION TO SET RESERVATION DETAILS ### 
st.title("Hotel Reservation NFT System")

# Create blank dataframes for Streamlit
selectable_hotel_dict = {}
chosen_total_price = 0
d = {'Hotel Name': ['name'], 'Average Price': [0], 'Total Price': [0]}
hotel_price_df = pd.DataFrame(data=d, columns=['Hotel Name', 'Average Price', 'Total Price'])

# Room input details
city = st.text_input('Which city would you like to search?')                    # Set city variable
col1top, col2top = st.columns(2)
with col1top:
    checkin_date = st.date_input('Check-In')                                    # Set check out variable
with col2top:
    checkout_date = st.date_input('Check-Out')                                  # Set check out variable

col1bottom, col2bottom = st.columns(2)
with col1bottom:
    adults_number = st.number_input('Number of Adults', min_value = 1, step=1)  # Set number of adults variable
with col2bottom:
    room_number = st.number_input('Number of Rooms', min_value = 1, step=1)     # Set number of rooms variable


# Format the values for input into API
adults_number = str(adults_number)
room_number = str(room_number)
checkin_date = str(checkin_date)
checkout_date = str(checkout_date)


# Search Locations
if st.checkbox('Set Location'):
    destination_id = get_location(city)


# Search hotels
if st.checkbox('Search'):
    hotel_response = get_hotels(destination_id, checkin_date, checkout_date, adults_number, room_number)


# Checkbox to display the dataframe
if st.checkbox('Display Dataframe'):
    hotel_data = hotel_response.json()
    # Create empty lists for json values to be populated in
    hotel_list = []
    total_price_list = []
    average_price_list = []
    picklist_label = []

    # Loop through all queried hotels in a given page to populate the values in the lists
    i = 0
    while i < 20:
        hotel_list.append(hotel_data['result'][i]['hotel_name'])
        total_price_list.append(hotel_data['result'][i]['price_breakdown']['all_inclusive_price'])
        average_price_list.append(hotel_data['result'][i]['composite_price_breakdown']['gross_amount_per_night']['value'])
        picklist_label.append(hotel_data['result'][i]['hotel_name'] + ' - $' + str(round(hotel_data['result'][i]['composite_price_breakdown']['gross_amount_per_night']['value'],2)) + ' per night - $' + str(round(hotel_data['result'][i]['price_breakdown']['all_inclusive_price'],2)) + ' total cost')
        i += 1

    # Create the final hotel list as a list of lists
    final_hotel_list = [hotel_list, average_price_list, total_price_list]
    selectable_hotel_dict = dict(zip(hotel_list, picklist_label))

    # Create the hotel price dataframe
    hotel_price_df = pd.DataFrame(final_hotel_list).transpose()
    hotel_price_df.columns = ['Hotel Name', 'Average Price', 'Total Price']
    hotel_price_df = hotel_price_df.set_index('Hotel Name')


# Set chosen values
chosen_hotel = st.selectbox('Select a Hotel', selectable_hotel_dict, format_func = lambda x: selectable_hotel_dict.get(x))
if bool(chosen_hotel):
    chosen_average_price = hotel_price_df.loc[chosen_hotel , 'Average Price']
    chosen_total_price = hotel_price_df.loc[chosen_hotel , 'Total Price']
st.markdown('_List Ordered by Popularity_')


# Set accounts variable
accounts = w3.eth.accounts

### SECTION TO INPUT WALLET ADDRESS AND FINALIZE BOOKING ###
st.write("### Input an Wallet Address to Continue")
address = st.text_input("Input Account Address")
st.markdown("---")


# Generate confirmation number
confirmation_code = uuid.uuid4()


st.markdown("## Confirm and Tokenize Hotel Reservation")


# Display final room booking details
if chosen_hotel != None:
    hotel_name = st.markdown(f'### {chosen_hotel}')
    hotel_room_value = st.markdown(f'### ${chosen_total_price} USD')
    st.markdown(f'#### Your confirmation code is: {confirmation_code}')

# hotel_confirmation = st.text_input("Enter the reservation confirmation")


# Finalize the hotel room booking
if st.button("Finalize Hotel Reservation"):
    hotel_reservation_ipfs_hash = pin_hotel_reservation(chosen_hotel)
    hotel_reservation_uri = f"ipfs://{hotel_reservation_ipfs_hash}"
    tx_hash = contract.functions.registerHotelReservation(
        address,
        str(chosen_hotel),
        str(checkin_date),
        str(checkout_date),
        str(confirmation_code),
        int(chosen_total_price),
        hotel_reservation_uri,
    ).transact({"from": address, "gas": 1000000})
    with st.spinner("Tokenizing Reservation ..."):
        time.sleep(10)
    st.success("Success!")
    st.balloons()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write(
        "You can view the pinned metadata file with the following IPFS Gateway Link"
    )
    st.markdown(
        f"[Hotel Reservation IPFS Gateway Link](https://ipfs.io/ipfs/{hotel_reservation_ipfs_hash})"
    )
st.markdown("---")


# Updated Price for Hotel Reservation Token/NFT
st.markdown("## Current Price of Tokenized IDs")
if st.checkbox(
    "Do you want to see the current market value of your Tokenized IDs at this time"
):
    tokens = contract.functions.totalSupply().call()
    token_id = st.selectbox("Choose a Reservation Token ID", list(range(tokens)))
    current_price = contract.functions.roomconfirmation(token_id).call()[-1]
    st.text(f" Current Price on BlockChain $ {current_price}")
    # .call("hotelRoomValue"))
    updated_room_price = st.text_input(
        "API Call for updated room price"
    )  # **Will update functionality - An API call will be made to get updated Price**
    updated_price_report = f"Updated Price on ?today's date: {updated_room_price} "  # **Need to update code to put the current date when ever function is called**
    if st.button("Update Price on BlockChain"):

        # Use Pinata to pin an updated price report for the report URI
        updated_price_report_ipfs_hash = pin_historical_price_report(
            updated_price_report
        )
        report_uri = f"ipfs://{updated_price_report_ipfs_hash}"

        # Use the token_id and the report_uri to record the updated price of token/nft
        tx_hash = contract.functions.updatedPriceOfReservation(
            token_id, int(updated_room_price), report_uri
        ).transact({"from": w3.eth.accounts[0]})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write(receipt)
    st.markdown("---")
