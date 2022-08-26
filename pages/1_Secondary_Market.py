################################################################################
# Imports
from lib2to3.pgen2 import token
import os
import csv
import pandas as pd
import json
from pathlib import Path
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from web3 import Web3
from dotenv import load_dotenv
# w3_wallet below defined to connect to Ganache wallet only, to distinguish from the other w3 below
w3_wallet = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
################################################################################

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

from functions import get_location, get_hotels

load_dotenv()

# Create an instance of web3.py for communicationn to the Blockchain smart contract
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

## Load the smart contract from remix

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
def pin_hotel_reservation(hotel_name, hotel_confirmation_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(hotel_confirmation_file.getvalue())

    # Build a token metadata file for the Hotel Reservation
    token_json = {"name": hotel_name, "image": ipfs_file_hash}
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_historical_price_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

################################################################################


from crypto_wallet import generate_account, get_balance, send_transaction

################################################################################

## Below are database stored with fake/stock hotel infor & images for website display purpose (not usefule real codes)
hotel_database = {
    "1 Hotel Toronto": ["1 Hotel Toronto", "0x05d38543486F918D1d0fFB73E074e90445dD9E5D", "4.3", .20, "Images/1 Hotel Toronto.jpeg"],
    "The Omni King Edward Hotel": ["The Omni King Edward Hotel", "0x2422858F9C4480c2724A309D58Ffd7Ac8bF65396", "5.0", .33, "Images/The Omni King Edward Hotel.jpeg"],
    "The Ritz-Carlton Toronto": ["The Ritz-Carlton Toronto", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.7", .19, "Images/The Ritz-Carlton Toronto.jpeg"],
    "The Yorkville Royal Sonesta Hotel Toronto": ["The Yorkville Royal Sonesta Hotel Toronto", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.1", .16, "Images/The Yorkville Royal Sonesta Hotel Toronto.jpeg"]
}

# A list of 
hotels = ["1 Hotel Toronto", "The Omni King Edward Hotel", "The Ritz-Carlton Toronto", "The Yorkville Royal Sonesta Hotel Toronto"]


def get_hotel(w3_wallet):
    """Display the database of hotel list."""
    db_list = list(hotel_database.values())

    for number in range(len(hotels)):
        st.image(db_list[number][4], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("Rating: ", db_list[number][2])
        st.write("Daily Rate per Ether: ", db_list[number][3], "eth")
        st.text(" \n")

################################################################################
# Streamlit Code

# Streamlit application headings
st.markdown("# Trade Your Hotel Rooms Here!")

st.markdown("## Hotels on Sale!")
st.text(" \n")

st.image(list(hotel_database.values())[0][4], width=400)

with open('./hotels_on_secondary_market_list.csv', 'r') as f:
    file = csv.reader(f)
    hotels_on_secondary_market_list = list(file)
    df_hotels_on_secondary_market_list = pd.DataFrame(hotels_on_secondary_market_list)
    df_hotels_on_secondary_market_list.columns = ['hotel name','start date','end date','confimation','purchase price (Usd)','price listed (Eth)','token ID','seller address']
    ## to set "token ID" column to be index column so that later it can be used to look up other values
    df_hotels_on_secondary_market_list = df_hotels_on_secondary_market_list.set_index('token ID')
st.write("hotels_on_sedondary_market_list",df_hotels_on_secondary_market_list)

tokens_on_secondary_market_list = list(df_hotels_on_secondary_market_list)


################################################################################
# Streamlit Sidebar Code - Start
st.sidebar.markdown("## USD/Ether Converter")


st.sidebar.markdown("## Current Account Address and Ether Balance in Ether")

##########################################

account = generate_account()

##########################################

# Write the client's Ethereum account address to the sidebar
st.sidebar.write(account.address)

##########################################

st.sidebar.write(get_balance(w3_wallet, account.address))

##########################################

# Create a select box for user to list 
st.sidebar.markdown("## SELL")

## show existing token list

tokens = contract.functions.totalSupply().call()
token_id_listed = st.sidebar.selectbox("List Your Hotel Token ID to sell", list(range(tokens)))

booking_info_listed = contract.functions.roomconfirmation(token_id_listed).call()

## st.sidebar.text(booking_info_listed)
st.sidebar.write("Hotel Name: ", booking_info_listed[0])
st.sidebar.write("Start Date: ",booking_info_listed[1])
st.sidebar.write("End Date: ",booking_info_listed[2])
## st.sidebar.write("Confirmation Note: ",booking_info_listed[3])
st.sidebar.write("Price purchased: ",booking_info_listed[4])

price_list_for_sale = st.sidebar.number_input("price listed for sale")
st.sidebar.write("price_list_for_sale: ",price_list_for_sale)

# Identify the seller Ethereum Address
#seller_address = "0x05d38543486F918D1d0fFB73E074e90445dD9E5D"
seller_address = st.sidebar.text_input("Input seller Address")
st.sidebar.write("seller_address", seller_address)

## below part enable seller to add their token to secondary market database
if st.sidebar.button("List token on Sale"):
    st.sidebar.write("token_id_listed",token_id_listed)
    st.sidebar.write("booking_info_listed",booking_info_listed)
    ## add other info to booking info like: listed price, token id, seller's address to receive proceeds from the sale
    booking_info_listed.append(price_list_for_sale)
    booking_info_listed.append(token_id_listed)
    booking_info_listed.append(seller_address)
    ## hotel_listed_info = hotel_listed_info.append(account.address)

    tokens_on_secondary_market_list.append(token_id_listed) 

    hotels_on_secondary_market_list.append(booking_info_listed)

    df = pd.DataFrame(hotels_on_secondary_market_list)

    df.to_csv('hotels_on_secondary_market_list.csv', index = False, header= None)

    st.balloons()

##########################################
# BUY
# Create a select box to chose hotel
st.sidebar.markdown("## *********************************")
st.sidebar.markdown("## BUY")


tokens = contract.functions.totalSupply().call()

token_id_listed = st.sidebar.selectbox("Choose a token to buy", list(range(tokens)))


## st.sidebar.markdown("## Hotel Name, Daily Rate, and Ethereum Address")
st.sidebar.write("Token selected to buy ", token_id_listed)

seller_address = df_hotels_on_secondary_market_list.loc[str(token_id_listed),'seller address']
st.sidebar.write("seller_address", seller_address)


buyer_address = account.address
st.sidebar.write("buyer_address", buyer_address)

st.sidebar.markdown("buyer's Ethereum Balance")

# Write the inTech Finder candidate's Ethereum balance to the sidebar
st.sidebar.write(get_balance(w3_wallet,account.address)) 


# Write the inTech Finder candidate's Daily rate to the sidebar
price_to_pay_seller = st.sidebar.number_input("price_to_pay_seller")
st.sidebar.write("price_to_pay_seller: ",price_to_pay_seller)


st.sidebar.markdown("## Total Proceeds (ether) to be paid")

st.sidebar.write(price_to_pay_seller)


##########################################

if st.sidebar.button("Pay seller & Transfer NFT Ownership"):
    # Transfer NYT
    contract.functions.transferFrom(seller_address,buyer_address,token_id_listed).transact({"from": seller_address, "gas": 3000000})
    st.sidebar.write("#### Just transfered ownership of token ID: ",token_id_listed)

    # make payament to seller
    ##transaction_hash = send_transaction(w3_wallet,buyer_address,seller_address,price_to_pay_seller)
    transaction_hash = send_transaction(w3_wallet,account,seller_address,price_to_pay_seller)

    # Markdown for the transaction hash

    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()

## Transfer NFT ownership

if st.sidebar.button("Transfer NFT Ownership"):

    contract.functions.transferFrom(seller_address,buyer_address,token_id_listed).transact({"from": seller_address, "gas": 3000000})

    st.sidebar.write("#### Just transfered ownership of token ID: ",token_id_listed)


    # Celebrate your successful payment
    st.balloons()

if st.sidebar.button("Send Payment"):

    transaction_hash = send_transaction(w3_wallet,account,seller_address,price_to_pay_seller)
    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()
