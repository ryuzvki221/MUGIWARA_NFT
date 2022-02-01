// contracts/AdvancedCollectible.sol
// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase{

    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;

    event RequestedCollectible(bytes32 indexed requestId);
    enum Mugiwara{Luffy, Zoro, Nami, Usopp, Chopper, Sanji, Franky, Brook, Robin, Jinbei}


    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Mugiwara)public tokenIdToMugiwara;
    mapping(bytes32 => uint256) public requestIdToTokenId;


    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyHash) public
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Mugiwaras","MGW"){

        keyHash = _keyHash;
        fee = 0.1 * 10 ** 18; // 0.1 LINK
        tokenCounter = 0;
    }

    function createCollectible(uint256 userProvidedSeed, string memory tokenURI) public 
    returns(bytes32){
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit RequestedCollectible(requestId);
    }
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override{
        address owner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(owner, newItemId);
        _setTokenURI(newItemId, tokenURI);

        Mugiwara mugiwara = Mugiwara(randomNumber % 10);
        tokenIdToMugiwara[newItemId] = mugiwara;
        requestIdToTokenId[requestId]= newItemId;
        tokenCounter = tokenCounter +1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public{

        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: transfer owner not caller nor approuved!");
        _setTokenURI(tokenId, _tokenURI);
    }
}