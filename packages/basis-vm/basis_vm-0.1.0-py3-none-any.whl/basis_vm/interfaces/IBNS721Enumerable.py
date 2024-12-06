"""
Title: Basis Network Standard (BNS-721 Enumerable)
Description: An extension of BNS-721 implementing the enumerable functionality, similar to ERC-721 Enumerable.

This contract extends IBNS721 to allow enumeration of NFTs owned by an address and all NFTs in the contract.

Note: Event declarations are included in comments due to VM limitations.

v1.0.0. Licensed under the Apache License, Version 2.0 (the "License");

Basis network.
"""

import IBNS721

class IBNS721Enumerable(IBNS721.IBNS721):
    def __init__(self, name: str, symbol: str):
        """
        Initializes the enumerable NFT contract with the given parameters.

        State Variables:
            _all_tokens (list): List of all token IDs as strings.
            _owned_tokens (dict): Mapping from owner to list of token IDs as strings.
            _owned_tokens_index (dict): Mapping from token ID to index in the owner's token list.
            _all_tokens_index (dict): Mapping from token ID to index in the _all_tokens list.
        """
        super().__init__(name, symbol)
        self._all_tokens = []  # List of all token IDs (as strings)
        self._owned_tokens = {}  # owner (str) -> list of token IDs (as strings)
        self._owned_tokens_index = {}  # token ID (str) -> index in owner's token list
        self._all_tokens_index = {}  # token ID (str) -> index in _all_tokens list

    @read_only
    def total_supply(self) -> int:
        """
        Returns the total number of NFTs stored by the contract.

        Returns:
            int: Total supply of NFTs.
        """
        return len(self._all_tokens)

    @read_only
    def token_by_index(self, index: int) -> int:
        """
        Returns a token ID at a given index of all the NFTs stored by the contract.

        Args:
            index (int): The index to query.

        Returns:
            int: The token ID at the given index.

        Raises:
            ValueError: If the index is out of bounds.
        """
        if index < 0 or index >= len(self._all_tokens):
            raise ValueError("Index out of bounds.")
        return int(self._all_tokens[index])

    @read_only
    def token_of_owner_by_index(self, owner: str, index: int) -> int:
        """
        Returns a token ID owned by `owner` at a given index.

        Args:
            owner (str): The address of the owner.
            index (int): The index to query.

        Returns:
            int: The token ID at the given index.

        Raises:
            ValueError: If the index is out of bounds or owner has no tokens.
        """
        tokens = self._owned_tokens.get(owner)
        if tokens is None or index < 0 or index >= len(tokens):
            raise ValueError("Index out of bounds.")
        return int(tokens[index])

    @owner_only
    def mint(self, to: str, token_uri: str = "") -> int:
        """
        Mints a new NFT and assigns it to `to`, updating enumerable mappings.

        Returns:
            int: The ID of the minted NFT.
        """
        token_id = super().mint(to, token_uri)
        token_id_str = str(token_id)

        # Add to all tokens list
        self._all_tokens_index[token_id_str] = len(self._all_tokens)
        self._all_tokens.append(token_id_str)

        # Add to owner's tokens list
        if to not in self._owned_tokens:
            self._owned_tokens[to] = []
        self._owned_tokens_index[token_id_str] = len(self._owned_tokens[to])
        self._owned_tokens[to].append(token_id_str)

        return token_id

    def transfer_from(self, from_addr: str, to: str, token_id: int) -> None:
        """
        Transfers the NFT `token_id` from `from_addr` to `to`, updating enumerable mappings.
        """
        token_id_str = str(token_id)
        super().transfer_from(from_addr, to, token_id)

        # Remove from previous owner's tokens list
        self._remove_token_from_owner_enumeration(from_addr, token_id_str)

        # Add to new owner's tokens list
        if to not in self._owned_tokens:
            self._owned_tokens[to] = []
        self._owned_tokens_index[token_id_str] = len(self._owned_tokens[to])
        self._owned_tokens[to].append(token_id_str)

    @owner_only
    def burn(self, token_id: int) -> None:
        """
        Burns the NFT `token_id`, updating enumerable mappings.
        """
        token_id_str = str(token_id)
        owner = self.owner_of(token_id)
        super().burn(token_id)

        # Remove from owner's tokens list
        self._remove_token_from_owner_enumeration(owner, token_id_str)

        # Remove from all tokens list
        self._remove_token_from_all_tokens_enumeration(token_id_str)

    def _remove_token_from_owner_enumeration(self, owner: str, token_id_str: str):
        """
        Internal function to remove a token from the owner's enumeration mappings.
        """
        last_token_index = len(self._owned_tokens[owner]) - 1
        token_index = self._owned_tokens_index[token_id_str]

        if token_index != last_token_index:
            last_token_id_str = self._owned_tokens[owner][last_token_index]
            self._owned_tokens[owner][token_index] = last_token_id_str
            self._owned_tokens_index[last_token_id_str] = token_index

        self._owned_tokens[owner].pop()
        del self._owned_tokens_index[token_id_str]

        if not self._owned_tokens[owner]:
            del self._owned_tokens[owner]

    def _remove_token_from_all_tokens_enumeration(self, token_id_str: str):
        """
        Internal function to remove a token from the all tokens enumeration mappings.
        """
        last_token_index = len(self._all_tokens) - 1
        token_index = self._all_tokens_index[token_id_str]

        if token_index != last_token_index:
            last_token_id_str = self._all_tokens[last_token_index]
            self._all_tokens[token_index] = last_token_id_str
            self._all_tokens_index[last_token_id_str] = token_index

        self._all_tokens.pop()
        del self._all_tokens_index[token_id_str]
