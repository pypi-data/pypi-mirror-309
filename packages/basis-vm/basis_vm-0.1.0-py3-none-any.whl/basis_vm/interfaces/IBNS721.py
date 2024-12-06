"""
Title: Basis Network Standard (BNS-721)
Description: A smart contract implementing the BNS-721 standard for Non-Fungible Tokens (NFTs), similar to ERC-721.

This contract allows for the creation and management of unique tokens on the Basis network. It includes
functionality for minting, transferring, and querying ownership of NFTs.

Note: Event declarations are included in comments due to VM limitations.

v1.0.0. Licensed under the Apache License, Version 2.0 (the "License");

Basis network.
"""

class IBNS721():
    def __init__(self, name: str, symbol: str):
        """
        Initializes the NFT contract with the given parameters.

        Args:
            name (str): The name of the NFT collection.
            symbol (str): The symbol of the NFT collection.

        State Variables:
            _name (str): The name of the NFT collection.
            _symbol (str): The symbol of the NFT collection.
            _owners (dict): A mapping from token IDs (as strings) to owner addresses.
            _balances (dict): A mapping from owner addresses to token counts.
            _token_approvals (dict): A mapping from token IDs (as strings) to approved addresses.
            _operator_approvals (dict): A nested mapping from owner to operator approvals.
            _token_uris (dict): A mapping from token IDs (as strings) to token URIs.
            _next_token_id (int): The next token ID to be minted.
        """
        self._name = name
        self._symbol = symbol
        self._owners = {}  # token_id (str) -> owner (str)
        self._balances = {}  # owner (str) -> balance (int)
        self._token_approvals = {}  # token_id (str) -> approved (str)
        self._operator_approvals = {}  # owner (str) -> {operator: bool}
        self._token_uris = {}  # token_id (str) -> token_uri (str)
        self._next_token_id = 1  # Start token IDs from 1

    @read_only
    def name(self) -> str:
        """
        Returns the name of the NFT collection.

        Returns:
            str: The name of the collection.
        """
        return self._name

    @read_only
    def symbol(self) -> str:
        """
        Returns the symbol of the NFT collection.

        Returns:
            str: The symbol of the collection.
        """
        return self._symbol

    @read_only
    def balance_of(self, owner: str) -> int:
        """
        Returns the number of NFTs owned by `owner`.

        Args:
            owner (str): The address of the owner.

        Returns:
            int: The number of NFTs owned by the owner.

        Raises:
            ValueError: If the owner address is invalid.
        """
        if not owner:
            raise ValueError("Owner address is invalid.")
        return self._balances.get(owner, 0)

    @read_only
    def owner_of(self, token_id: int) -> str:
        """
        Returns the owner of the NFT specified by `token_id`.

        Args:
            token_id (int): The ID of the NFT.

        Returns:
            str: The address of the owner.

        Raises:
            ValueError: If the token does not exist.
        """
        token_id_str = str(token_id)
        owner = self._owners.get(token_id_str)
        if owner is None:
            raise ValueError("Token does not exist.")
        return owner

    @read_only
    def token_uri(self, token_id: int) -> str:
        """
        Returns the metadata URI of the NFT specified by `token_id`.

        Args:
            token_id (int): The ID of the NFT.

        Returns:
            str: The metadata URI of the NFT.

        Raises:
            ValueError: If the token does not exist.
        """
        token_id_str = str(token_id)
        if token_id_str not in self._owners:
            raise ValueError("Token does not exist.")
        return self._token_uris.get(token_id_str, "")

    def approve(self, to: str, token_id: int) -> None:
        """
        Approves `to` to transfer the specified NFT on behalf of the caller.

        Args:
            to (str): The address to be approved.
            token_id (int): The ID of the NFT.

        Raises:
            ValueError: If the caller is not the owner or an approved operator.
            ValueError: If the token does not exist.
        """
        token_id_str = str(token_id)
        owner = self.owner_of(token_id)
        caller = auth_user
        if caller != owner and not self.is_approved_for_all(owner, caller):
            raise ValueError("Caller is not owner nor approved for all.")
        self._token_approvals[token_id_str] = to
        # Event: Approval(owner, to, token_id)

    @read_only
    def get_approved(self, token_id: int) -> str:
        """
        Returns the approved address for the NFT `token_id`.

        Args:
            token_id (int): The ID of the NFT.

        Returns:
            str: The approved address.

        Raises:
            ValueError: If the token does not exist.
        """
        token_id_str = str(token_id)
        if token_id_str not in self._owners:
            raise ValueError("Token does not exist.")
        return self._token_approvals.get(token_id_str, "")

    def set_approval_for_all(self, operator: str, approved: bool) -> None:
        """
        Approves or revokes approval for an operator to manage all of the caller's assets.

        Args:
            operator (str): The operator address.
            approved (bool): True to approve, False to revoke.

        Raises:
            ValueError: If the operator is the caller.
        """
        caller = auth_user
        if operator == caller:
            raise ValueError("Cannot set approval for self.")
        if caller not in self._operator_approvals:
            self._operator_approvals[caller] = {}
        self._operator_approvals[caller][operator] = approved
        # Event: ApprovalForAll(caller, operator, approved)

    @read_only
    def is_approved_for_all(self, owner: str, operator: str) -> bool:
        """
        Checks if `operator` is approved to manage all of `owner`'s assets.

        Args:
            owner (str): The owner address.
            operator (str): The operator address.

        Returns:
            bool: True if approved, False otherwise.
        """
        return self._operator_approvals.get(owner, {}).get(operator, False)

    def transfer_from(self, from_addr: str, to: str, token_id: int) -> None:
        """
        Transfers the NFT `token_id` from `from_addr` to `to`.

        Args:
            from_addr (str): The current owner of the NFT.
            to (str): The address to transfer the NFT to.
            token_id (int): The ID of the NFT.

        Raises:
            ValueError: If the caller is not authorized.
            ValueError: If `from_addr` is not the current owner.
            ValueError: If `to` address is invalid.
        """
        token_id_str = str(token_id)
        caller = auth_user
        if not self._is_approved_or_owner(caller, token_id_str):
            raise ValueError("Caller is not owner nor approved.")
        if self._owners.get(token_id_str) != from_addr:
            raise ValueError("From address is not the owner.")
        if not to:
            raise ValueError("Transfer to the zero address is prohibited.")

        # Clear approvals
        if token_id_str in self._token_approvals:
            del self._token_approvals[token_id_str]

        # Update ownership and balances
        self._owners[token_id_str] = to
        self._balances[from_addr] -= 1
        self._balances[to] = self._balances.get(to, 0) + 1

        # Event: Transfer(from_addr, to, token_id)

    def safe_transfer_from(self, from_addr: str, to: str, token_id: int) -> None:
        """
        Safely transfers the NFT `token_id` from `from_addr` to `to`.

        Args:
            from_addr (str): The current owner of the NFT.
            to (str): The address to transfer the NFT to.
            token_id (int): The ID of the NFT.

        Raises:
            ValueError: If the transfer is not safe.
        """
        # For simplicity, assuming transfer is always safe in this implementation
        self.transfer_from(from_addr, to, token_id)
        # Note: In a complete implementation, we'd check if 'to' is a contract and handle accordingly.

    @owner_only
    def mint(self, to: str, token_uri: str = "") -> int:
        """
        Mints a new NFT and assigns it to `to`.

        Args:
            to (str): The address to mint the NFT to.
            token_uri (str, optional): The metadata URI associated with the NFT.

        Returns:
            int: The ID of the minted NFT.

        Raises:
            ValueError: If `to` address is invalid.
        """
        if not to:
            raise ValueError("Mint to the zero address is prohibited.")
        token_id = self._next_token_id
        token_id_str = str(token_id)

        self._owners[token_id_str] = to
        self._balances[to] = self._balances.get(to, 0) + 1
        self._token_uris[token_id_str] = token_uri
        self._next_token_id += 1

        # Event: Transfer('0x0', to, token_id)
        return token_id

    @owner_only
    def burn(self, token_id: int) -> None:
        """
        Burns the NFT `token_id`.

        Args:
            token_id (int): The ID of the NFT.

        Raises:
            ValueError: If the token does not exist.
        """
        token_id_str = str(token_id)
        owner = self._owners.get(token_id_str)
        if owner is None:
            raise ValueError("Token does not exist.")

        # Clear approvals
        if token_id_str in self._token_approvals:
            del self._token_approvals[token_id_str]

        # Clear token URI
        if token_id_str in self._token_uris:
            del self._token_uris[token_id_str]

        # Update ownership and balances
        del self._owners[token_id_str]
        self._balances[owner] -= 1
        if self._balances[owner] == 0:
            del self._balances[owner]

        # Event: Transfer(owner, '0x0', token_id)

    def _is_approved_or_owner(self, spender: str, token_id_str: str) -> bool:
        """
        Internal function to check if `spender` is allowed to manage `token_id`.

        Args:
            spender (str): The address to check.
            token_id_str (str): The ID of the NFT as a string.

        Returns:
            bool: True if `spender` is owner or approved, False otherwise.

        Raises:
            ValueError: If the token does not exist.
        """
        owner = self.owner_of(int(token_id_str))
        return (
            spender == owner or
            self.get_approved(int(token_id_str)) == spender or
            self.is_approved_for_all(owner, spender)
        )

    @read_only
    def supports_interface(self, interface_id: str) -> bool:
        """
        Checks if the contract supports a given interface.

        Args:
            interface_id (str): The interface identifier.

        Returns:
            bool: True if supported, False otherwise.
        """
        # Simplified: Returning True for known interfaces
        supported_interfaces = {
            "IERC165": True,
            "IERC721": True,
            "IERC721Metadata": True
        }
        return supported_interfaces.get(interface_id, False)
