pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract HotelReservationRegistry is ERC721Full {
    constructor() public ERC721Full("HotelReservationToken", "RES") {}

    struct HotelConfirmation {
        // Data class for Hotel reservation

        string hotelName;
        string startDate;
        string endDate;
        string confirmation;
        uint256 hotelRoomValue;
    }

    mapping(uint256 => HotelConfirmation) public roomconfirmation; // data structure (dictionary) creation

    event Price(uint256 token_id, uint256 hotelRoomValue, string reportURI); // event function to record data as a log entry on the blockchain

    event TerminationOfToken(uint256 token_id, string current_date); // event function to delete Token that has expired per the endDate

    function registerHotelReservation(
        // register hotel reservation and returns the newly minted token as a uint256

        address owner,
        string memory hotelName,
        string memory startDate,
        string memory endDate,
        string memory confirmation,
        uint256 hotelRoomValue,
        string memory tokenURI // The URI to where the hotelreservation resides on the internet
    ) public returns (uint256) {
        uint256 tokenId = totalSupply(); // the count of the number of tokens minted

        _mint(owner, tokenId); // minting hotelreservation NFT

        _setTokenURI(tokenId, tokenURI); //permanently link the tokenID to the URI

        roomconfirmation[tokenId] = HotelConfirmation(
            hotelName,
            startDate,
            endDate,
            confirmation,
            hotelRoomValue
        ); //  - linking token ID to HotelConfirmation struct

        return tokenId; // NFT creation for hotel reservation
    }

    function updatedPriceOfReservation(
        uint256 tokenId,
        uint256 updatedRoomPrice,
        string memory reportURI
    ) public returns (uint256) {
        // function to update price of reservatoin

        roomconfirmation[tokenId].hotelRoomValue = updatedRoomPrice; // updating the price of the NFT room reservation

        emit Price(tokenId, updatedRoomPrice, reportURI); // event triggered by emit keyword

        return roomconfirmation[tokenId].hotelRoomValue;
    }

    function TerminatingToken(uint256 tokenId, string memory current_date)
        internal
    {
        roomconfirmation[tokenId].endDate = current_date;

        emit TerminationOfToken(tokenId, current_date);

        return _burn(ownerOf(tokenId), tokenId);
    }
}
