# Project_3: Hotel.io

## Overview & Features

Did you know that almost 20% of hotels rooms booked online are cancelled before the guest arrives? This not only directly impacts the revenue of the hotel, but also leads to poor marketing, since Online Travel Agencies keep track of cancellations drawn by a hotel. The prospective guest is hit with cancellation fees and left dissastified. All in all, in the event of a cancellation there is an apparent lose-lose relationship between prospective guests and hotel operators. We strive to solve this crucial pain point.

**Introducing (drum roll please)...**

![image](https://user-images.githubusercontent.com/24529411/186531759-69331a01-be22-4fdd-a894-f4ec3bdd600f.png)

<ins>**Hotel.io: a platform that addresses last minute cancellations and creates a win-win solution for prospecitve guests and hotel operators.**</ins>

Hotel.io solves this problem by creating and implementing the following features:

1) A UI from which users can buy, sell, or swap hotel room bookings
An integration with Booking.com using the rapidAPI in order to obtain real-time hotel pricing from hotels such as The Marriot, Sheridan, 4 Seasons, Courtyard among others
2) Smart contracts that mint NFTs the moment a hotel room is purchased
3) Smart contracts that create rules around and facilitate the trading, buying and selling of rooms on a secondary market

### NOTE

* A subscription to utilize rapidAPI is needed in order to succesfully run the application

## Technologies

The Hotel.io marketplace utilizes Python (v 3.9.7) and the following libraries:
1. os 2. csv 3. pandas as pd 4. json 5. from pathlib import Path 6. streamlit as st 7. from dataclasses import dataclass 8. from typing import Any, List 9. from web3 import Web3 10. from dotence import load_dotenv 11. from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json 12. from PIL import Image 13. time 14. requests 15. from bip44 import Wallet 16. from web3 import Account 17. from web3 import middleware 18. from web3.gas_strategies.time_based import medium_gas_price_strategy 19. from functions import get_location, get_hotels 20. RapidAPI

## Installation Guide

Majority of the above libraries should be part of the base applications that were installed with the Python version above; if not, you will have to install them through the pip package manager of Python.

[PIP Install Support Web Site](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-python-from-the-command-line)

## Application Sections

### 1. Booking the Hotel: RapidAPI Pull

When it comes to the booking interface, we have not re-invented the wheel, and frankly there is still room for a number of improvements. Leveraging Streamlit, a user can simply log in to our App, search the city they would like to visit, enter their check in and check out dates, indicate the number of guests and number of rooms, and let the Booking.com API perform the heavy lifting. Users are then presented with a list of hotels, sorted by popularity, from which they can select. The dropdown not only lists the name of the hotel, but also the total cost of their stay and average cost per night for easy comparison. Once the user is satisfied with their selection, the following step is to enter your personal wallet address and purchase!

**link to the hotel booking file**

#### INPUT

##### Image 1: Calling the data
![image](https://user-images.githubusercontent.com/24529411/186524189-eab9dde0-c018-45b6-aded-d74b0f233564.png)

#### OUTPUT


### 2. Creating a Smart Contract: Minting an the Hotel Room Purchase into an NFT

Upon choosing your adventure destination, our application then begins the exciting process of minting an NFT reflecting the details of your booking. The process begins with a customer inputting their wallet account address to start the call to the deployed Hotelbooking_NFT smart contract which utilizes ERC721Full library for its industry standards for Non Fungible Token functions. The needed variables/information for our smart contract call are the hotel name, check in date, departure date and confirmation number which should be automatically pulled from the purchased reservation made by the customer. With this information the deployed contract will insert them into a dictionary called room-confirmation  and start the process of minting a unique Hotel Reservation Token. Once the token has been minted we connect the TokenID to a unique URI (Uniform Resource Identifer) which identifies the location of the token on the BlockChain/IPFS and permanently link the tokenID to the created room-confirmation dictionary. Finally after the call to the smart contract has been executed and included on the Blockchain the minted TokenID, the transaction receipt mined and a hotel reservation IPFS link to your tokenized reservation NFT is provided to the customer for their future reference. With a created NFT for their reservation they will have the capability of listing it on our secondary market.

**link to the smart contract file**

#### INPUT

##### Image 1: Inputing room criteria
![image](https://user-images.githubusercontent.com/24529411/186529554-6c59cc91-79b7-4ccc-b5a2-117d7aafd8bb.png)

##### Image 2: Tokenizing the reservation
![image](https://user-images.githubusercontent.com/24529411/186529756-ab7a8f41-ef2c-4a06-8d87-ab0268e964ce.png)

#### OUTPUT


### 3. Secondary Market: Relisting a Purchased Hotel Room

While we attempted to design a way to disrupt the hotel market, as a byproduct we ended up creating an entirely new market to supplement it with our booking NFT market. A key component of this platform is the ability to empower consumers and give them the flexibility modern life demands. Within our secondary market you will find a suite of tools, ranging from being able to check the current price of any bookings you currently hold to browsing all other listings tailored to your unique filters and parameters. Clients can list or delist their bookings based off their desires, while simultaneously being able to gauge the current market for their asset and determine the best path forward. The pieces that make up this venture have been tried and tested in other fields, giving us confidence that we can succeed and scale this concept as growth accelerates.

#### INPUT

##### Image 1: Calling the data
![image](https://user-images.githubusercontent.com/24529411/186524189-eab9dde0-c018-45b6-aded-d74b0f233564.png)

#### OUTPUT


**link to creating the secondary market file**

## Development Pipeline

Upon succesful deployment of the Hotel.io platform, we aim to create a NFT / Smart Contract system to not only allow trading of hotel rooms within a secondary market, but also to create secondary marketplaces for airfaires, car rentals and airbnbs.

## Concluding Thoughts

We have seamlessly integrated and connected our disparate sections into one streamlined application for our user base’s ease of use. Client inputs in initial sections are pulled forward to limit hassle on the client side. From initial booking to tokenization to potential listing and purchasing on the secondary market, everything within this tool is designed to make the process as easy as possible, while at the same time placing countless options at the user’s fingertips to accomplish whatever they desire. Want to book a room? Purchase directly from the hotel and tokenize one or shop our secondary market and find one you feel is a better deal. Want to know how your prior booking price reflects what that room is worth today? We have you covered, all within a few clicks of our streamlit application.

## Contributors

Contributors for the development and deployment of the Hotel.io platform and marketplace include:

1. Ryan Anderson: a) Streamlit Engineer (RapidAPI pull) b)
2. Tao Chen: a) Streamlit Engineer (secondary market)
3. James Handral: a) Streamlit Engineer (smart Contract / NFT)
4. Colton Mayes: a) Streamlit Engineer (merging the three applications) b) Final Presentation c) README
5. Bennett Kramer: a) Final Presentation b) README
