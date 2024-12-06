"""
Title: Basis Network Standard (BNS-20)
Description: A fully documented smart contract implementing a standard token, similar to ERC-20.

This contract allows for the creation of a fungible token on the Basis network. It includes
functionality for transferring tokens, approving allowances, and querying balances and allowances.

v1.0.0. Licensed under the Apache License, Version 2.0 (the "License");

Basis network.
"""

class IBNS20():
    def __init__(self, name: str, symbol: str, decimals: int, total_supply: int):
        """
        Initializes the token contract with the given parameters and assigns the total supply
        to the contract owner.

        Args:
            name (str): The name of the token.
            symbol (str): The symbol of the token.
            decimals (int): The number of decimal places the token uses.
            total_supply (int): The total supply of tokens.

        State Variables:
            _name (str): The name of the token.
            _symbol (str): The symbol of the token.
            _decimals (int): The number of decimal places the token uses.
            _total_supply (int): The total supply of tokens.
            _balances (dict): A mapping from addresses to their token balances.
            _allowances (dict): A nested mapping from owner addresses to spender addresses to allowances.
        """
        self._name = name
        self._symbol = symbol
        self._decimals = decimals
        self._total_supply = total_supply
        self._balances = {contract_owner: total_supply}
        self._allowances = {}

    @read_only
    def name(self) -> str:
        """
        Returns the name of the token.

        Returns:
            str: The name of the token.
        """
        return self._name

    @read_only
    def symbol(self) -> str:
        """
        Returns the symbol of the token.

        Returns:
            str: The symbol of the token.
        """
        return self._symbol

    @read_only
    def decimals(self) -> int:
        """
        Returns the number of decimals the token uses.

        Returns:
            int: The number of decimals.
        """
        return self._decimals

    @read_only
    def total_supply(self) -> int:
        """
        Returns the total token supply.

        Returns:
            int: The total supply of tokens.
        """
        return self._total_supply

    @read_only
    def balance_of(self, account: str) -> int:
        """
        Returns the account balance of another account with address `account`.

        Args:
            account (str): The address of the account.

        Returns:
            int: The balance of the account.
        """
        return self._balances.get(account, 0)

    def transfer(self, to: str, amount: int) -> bool:
        """
        Transfers `amount` tokens to address `to`.

        Args:
            to (str): The address to transfer to.
            amount (int): The amount of tokens to be transferred.

        Returns:
            bool: True if the transfer was successful.

        Raises:
            ValueError: If the sender has insufficient balance.
            ValueError: If the amount is invalid.
        """
        sender = auth_user
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if self._balances.get(sender, 0) < amount:
            raise ValueError("Insufficient balance.")
        self._balances[sender] -= amount
        self._balances[to] = self._balances.get(to, 0) + amount
        return True

    def approve(self, spender: str, amount: int) -> bool:
        """
        Allows `spender` to withdraw from your account multiple times, up to the `amount` amount.

        Args:
            spender (str): The address authorized to spend.
            amount (int): The maximum amount they can spend.

        Returns:
            bool: True if the approval was successful.
        """
        owner = auth_user
        if owner not in self._allowances:
            self._allowances[owner] = {}
        self._allowances[owner][spender] = amount
        return True

    @read_only
    def allowance(self, owner: str, spender: str) -> int:
        """
        Returns the amount which `spender` is still allowed to withdraw from `owner`.

        Args:
            owner (str): The address which owns the funds.
            spender (str): The address which will spend the funds.

        Returns:
            int: The remaining allowance for the spender.
        """
        return self._allowances.get(owner, {}).get(spender, 0)

    def transfer_from(self, from_account: str, to: str, amount: int) -> bool:
        """
        Transfers `amount` tokens from address `from_account` to address `to`.

        Args:
            from_account (str): The address to send tokens from.
            to (str): The address to transfer to.
            amount (int): The amount of tokens to be transferred.

        Returns:
            bool: True if the transfer was successful.

        Raises:
            ValueError: If the `from_account` has insufficient balance.
            ValueError: If the allowance is insufficient.
            ValueError: If the amount is invalid.
            ValueError: If the caller is not authorized.
        """
        spender = auth_user
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if self._balances.get(from_account, 0) < amount:
            raise ValueError("Insufficient balance in from_account.")
        allowed = self._allowances.get(from_account, {}).get(spender, 0)
        if allowed < amount:
            raise ValueError("Transfer amount exceeds allowance.")
        self._balances[from_account] -= amount
        self._balances[to] = self._balances.get(to, 0) + amount
        self._allowances[from_account][spender] -= amount
        return True

    @owner_only
    def mint(self, to: str, amount: int) -> bool:
        """
        Mints `amount` tokens and assigns them to `to`, increasing the total supply.

        Args:
            to (str): The address that will receive the minted tokens.
            amount (int): The amount of tokens to mint.

        Returns:
            bool: True if the minting was successful.

        Raises:
            ValueError: If the amount is invalid.
        """
        if amount <= 0:
            raise ValueError("Mint amount must be positive.")
        self._total_supply += amount
        self._balances[to] = self._balances.get(to, 0) + amount
        return True

    @owner_only
    def burn(self, from_account: str, amount: int) -> bool:
        """
        Burns `amount` tokens from `from_account`, reducing the total supply.

        Args:
            from_account (str): The address from which tokens will be burned.
            amount (int): The amount of tokens to burn.

        Returns:
            bool: True if the burning was successful.

        Raises:
            ValueError: If the `from_account` has insufficient balance.
            ValueError: If the amount is invalid.
        """
        if amount <= 0:
            raise ValueError("Burn amount must be positive.")
        if self._balances.get(from_account, 0) < amount:
            raise ValueError("Insufficient balance to burn.")
        self._balances[from_account] -= amount
        self._total_supply -= amount
        return True
