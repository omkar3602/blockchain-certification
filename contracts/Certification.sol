// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.9.0;
pragma experimental ABIEncoderV2;



contract Certification {
    address constant SENDER = 0x68FFD6C6695E64fDe44cF491cb4619E05D592C2c;
    
    
    address public owner;

    struct Certificate {
        address to;
        string name;
        string competitionName;
        uint256 timestamp;
    }
    Certificate[] certificates;

    constructor () public {
        owner = msg.sender;
    }

    function issueCertificate(address to, string memory name, string memory competitionName) public {
        require(msg.sender == SENDER, "You cannot issue certificates");

        certificates.push(Certificate(to, name, competitionName, block.timestamp));
    }

    function viewCertificates() public view returns (Certificate[] memory)
    {
        return certificates;
    }

}