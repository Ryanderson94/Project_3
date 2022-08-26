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

* A subscription to utilize rapidAPI and Pinata is needed in order to succesfully run the application

## Technologies

The Hotel.io marketplace utilizes Python (v 3.9.7) and the following libraries:
1. os 2. csv 3. pandas as pd 4. json 5. from pathlib import Path 6. streamlit as st 7. from dataclasses import dataclass 8. from typing import Any, List 9. from web3 import Web3 10. from dotence import load_dotenv 11. from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json 12. from PIL import Image 13. time 14. requests 15. from bip44 import Wallet 16. from web3 import Account 17. from web3 import middleware 18. from web3.gas_strategies.time_based import medium_gas_price_strategy 19. from functions import get_location, get_hotels 20. Login to the RapidAPI and a free basic subscription to the Booking.com

## Installation Guide

Majority of the above libraries should be part of the base applications that were installed with the Python version above; if not, you will have to install them through the pip package manager of Python.

[PIP Install Support Web Site](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-python-from-the-command-line)

Additionally, in order to run the application, users will need the following:

1) WEB3 Provider URI
2) Smart Contract Address
3) Trading Contract Address
4) Pinata API Key
5) Pinata Secret API Key
6) API Key
7) MNEMONIC Code

## Application Sections

### 1. Booking the Hotel: RapidAPI Pull

When it comes to the booking interface, we have not re-invented the wheel. Leveraging Streamlit, a user can simply log in to our App, search the city they would like to visit, enter their check in and check out dates, indicate the number of guests and number of rooms, and let the Booking.com API perform the heavy lifting. Users are then presented with a list of hotels, sorted by popularity, from which they can select. The dropdown not only lists the name of the hotel, but also the total cost of their stay and average cost per night for easy comparison. Once the user is satisfied with their selection, the following step is to enter your personal wallet address and purchase!

On the back-end, a RapidAPI call is made to pull real-time hotel information within the parameters of a screening, which include: locations, prices, dates, popularity, hotel operators, and more. the platform loads the saved contract data (ABI file) and smart contract address that deployed the contract. This allows for the back-end to interact with the front-end application, which leverages an instance of web3.py for communication to the Blockchain smart contract.

**Please refer to the link and images for furhter detail:**
[Hotel Reservation App](https://github.com/Ryanderson94/Project_3/blob/main/hotel_reservation_app.py)

##### *Back-end: Calling the data through RapidAPI (Booking.com API)*
![image](https://user-images.githubusercontent.com/24529411/186980161-e3338eef-6f19-4892-9626-1c839f1a9522.png)

##### *Front-End: Option criteria when booking a reservation*
![image](https://user-images.githubusercontent.com/24529411/186999401-9cdaf739-dde3-400c-b0cd-6b68ba97adcb.png)


### 2. Creating a Smart Contract: Minting an the Hotel Room Purchase into an NFT

Upon choosing an adventure destination, the Hotel.io application begins the process of minting an NFT reflecting the details of your booking on the back-end. The process is launched by a customer inputting their wallet account address to start the call to the deployed Hotelbooking_NFT smart contract which utilizes ERC721Full library for its industry standards for Non Fungible Token functions. 

Key variable include:

* Hotel name
* Check-in date
* Departure date
* Confirmation number 

Note that these variables should automatically be pulled from the purchased reservation made by the customer. 

With this information the deployed contract will insert them into a dictionary called <ins>**room-confirmation**</ins> and start the process of minting a unique Hotel Reservation Token. Once the token has been minted we connect the TokenID to a unique URI (Uniform Resource Identifer) which identifies the location of the token on the BlockChain/IPFS and permanently link the tokenID to the created room-confirmation dictionary. 

Finally after the call to the smart contract has been executed and included on the Blockchain the minted TokenID, the transaction receipt mined and a hotel reservation IPFS link to your tokenized reservation NFT is provided to the customer for their future reference. With a created NFT for their reservation they will have the capability of listing it on our secondary market. 

**Please refer to the link and images for furhter detail:**
[Hotel Reservation App](https://github.com/Ryanderson94/Project_3/blob/main/hotel_reservation_app.py)

##### *Back-End: Tokenizing the reservation*
![image](https://user-images.githubusercontent.com/24529411/186999298-acc48300-193f-4b7f-b09b-66aa777aeea7.png)

##### *Front-End: Confirmation Recipt of Hotel Reservation (NFT / Tokenization)*
![image](https://user-images.githubusercontent.com/24529411/186999472-b7543c34-3e7a-4fba-8705-76562d5f183c.png)

### 3. Secondary Market: Relisting a Purchased Hotel Room

While we attempted to design a way to disrupt the hotel market, as a byproduct we ended up creating an entirely new market to supplement it with our booking NFT market. A key component of this platform is the ability to empower consumers and give them the flexibility modern life demands. Within our secondary market you will find a suite of tools, ranging from being able to check the current price of any bookings you currently hold to browsing all other listings tailored to your unique filters and parameters. 

Clients can list or delist their bookings based off their desires, while simultaneously being able to gauge the current market for their asset and determine the best path forward. Once a client has listed its NFT on the secondary market, the token is then pulled into a CSV for potential purchases to view in a readable format.

Once the platform goes live, we have code built in to burn any tokens that have expired, meaning they will no longer exist because the current date is past the existing reservation date. This parameter is embedded in each of the smart contracts.

**Please refer to the link and images for furhter detail:**
[Secondary Market App](https://github.com/Ryanderson94/Project_3/blob/main/secondary_market.py)

##### Back-End: Inputting Room Criteria on the Secondary Market
![image](https://user-images.githubusercontent.com/24529411/186979198-966a0f99-d91d-4174-9681-b64ed32bd21c.png)

##### Front-End: Buy / Sell Inputs on Secondary Market
![image](https://user-images.githubusercontent.com/24529411/186999088-bd9ca37f-c5ce-43f7-8dd5-d3de65742955.png) ![image](https://user-images.githubusercontent.com/24529411/186999118-a06a5058-aa9e-464c-8edd-453f27032cd7.png)



##### Front-End: CSV File of Available Rooms on Secondary Market
![image](https://user-images.githubusercontent.com/24529411/186998973-a71a3c8e-a61e-405a-b1b8-df4a7303c4bf.png)

## Development Pipeline

Upon succesful deployment of the Hotel.io platform, we aim to create a NFT / Smart Contract system to not only allow trading of hotel rooms within a secondary market, but also exapnding into adjacent markets, which include secondary marketplaces for the following:

1) Airfaires 
2) Car rentals
3) Airbnbs

There is a tremendous market opportunity and we believe that demand will continue to rise in an increasingly virtual and unpredictable environment.

## Concluding Thoughts

We have seamlessly integrated and connected our disparate sections into one streamlined application for our user base’s ease of use. Client inputs in initial sections are pulled forward to limit hassle on the client side. From initial booking to tokenization to potential listing and purchasing on the secondary market, everything within this tool is designed to make the process as easy as possible, while at the same time placing countless options at the user’s fingertips to accomplish whatever they desire. Want to book a room? Purchase directly from the hotel and tokenize one or shop our secondary market and find one you feel is a better deal. Want to know how your prior booking price reflects what that room is worth today? We have you covered, all within a few clicks of our streamlit application.

## Contributors

Contributors for the development and deployment of the Hotel.io platform and marketplace include:

1. **Ryan Anderson**: a) Streamlit Engineer (RapidAPI pull) b) Repository Administrator
2. **Tao Chen**: a) Streamlit Engineer (secondary market)
3. **James Handral**: a) Streamlit Engineer (NFT / Tokenization)
4. **Colton Mayes**: a) Streamlit Engineer (Merging of RapidAPI and NFT / Tokenization) b) Final Presentation c) README
5. **Bennett Kramer**: a) Final Presentation b) README
