// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.9.0;
pragma experimental ABIEncoderV2;



contract Certification {
    address constant SENDER = 0x1583fF370ac71Db02E085cc98Da1613fcFD21Ace;
    
    
    address public owner;

    struct Certificate {
        address to;
        string name;
        string competitionName;
        uint256 timestamp;
        string email;
    }
    Certificate[] certificates;

    constructor () public {
        owner = msg.sender;
    }

    function issueCertificate(address to, string memory name, string memory competitionName, string memory email) public {
        require(msg.sender == SENDER, "You cannot issue certificates");

        certificates.push(Certificate(to, name, competitionName, block.timestamp, email));
    }

    function viewCertificates() public view returns (Certificate[] memory)
    {
        return certificates;
    }

}