"""
Price value object for representing monetary values.

This module defines an immutable value object for handling prices
with proper validation and formatting.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Price:
    """
    Value object for representing prices.
    
    This immutable class ensures price values are always valid and
    provides convenient formatting methods.
    """
    
    amount: float
    currency: str = "JPY"
    
    def __post_init__(self):
        """Validate price after initialization."""
        if self.amount < 0:
            raise ValueError("Price cannot be negative")
        
        # Validate currency
        supported_currencies = ["JPY", "USD", "EUR", "GBP", "CAD", "AUD"]
        if self.currency not in supported_currencies:
            raise ValueError(f"Unsupported currency: {self.currency}")
        
        # JPY should not have decimals
        if self.currency == "JPY" and self.amount != int(self.amount):
            object.__setattr__(self, 'amount', int(self.amount))
    
    @property
    def formatted(self) -> str:
        """
        Get formatted price string.
        
        Returns:
            Formatted price with currency symbol
        """
        currency_symbols = {
            "JPY": "¥",
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "CAD": "C$",
            "AUD": "A$"
        }
        
        symbol = currency_symbols.get(self.currency, self.currency)
        
        # Format based on currency
        if self.currency == "JPY":
            # No decimals for JPY
            return f"{symbol}{int(self.amount):,}"
        else:
            # Two decimal places for other currencies
            return f"{symbol}{self.amount:,.2f}"
    
    @property
    def amount_in_cents(self) -> int:
        """
        Get price amount in cents/minor units.
        
        Returns:
            Price in minor currency units
        """
        if self.currency == "JPY":
            # JPY doesn't have minor units
            return int(self.amount)
        else:
            # Convert to cents for other currencies
            return int(self.amount * 100)
    
    def add(self, other: 'Price') -> 'Price':
        """
        Add two prices together.
        
        Args:
            other: Another Price object
            
        Returns:
            New Price object with sum
            
        Raises:
            ValueError: If currencies don't match
        """
        if self.currency != other.currency:
            raise ValueError(f"Cannot add prices with different currencies: {self.currency} and {other.currency}")
        
        return Price(self.amount + other.amount, self.currency)
    
    def subtract(self, other: 'Price') -> 'Price':
        """
        Subtract one price from another.
        
        Args:
            other: Price to subtract
            
        Returns:
            New Price object with difference
            
        Raises:
            ValueError: If currencies don't match or result would be negative
        """
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract prices with different currencies: {self.currency} and {other.currency}")
        
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Price subtraction would result in negative value")
        
        return Price(result, self.currency)
    
    def multiply(self, factor: float) -> 'Price':
        """
        Multiply price by a factor.
        
        Args:
            factor: Multiplication factor
            
        Returns:
            New Price object with multiplied amount
            
        Raises:
            ValueError: If factor is negative
        """
        if factor < 0:
            raise ValueError("Cannot multiply price by negative factor")
        
        return Price(self.amount * factor, self.currency)
    
    def apply_discount(self, percentage: float) -> 'Price':
        """
        Apply a percentage discount to the price.
        
        Args:
            percentage: Discount percentage (0-100)
            
        Returns:
            New Price object with discount applied
            
        Raises:
            ValueError: If percentage is invalid
        """
        if not 0 <= percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        
        discount_factor = 1 - (percentage / 100)
        return Price(self.amount * discount_factor, self.currency)
    
    def __eq__(self, other) -> bool:
        """Check equality with another Price."""
        if not isinstance(other, Price):
            return False
        return self.amount == other.amount and self.currency == other.currency
    
    def __lt__(self, other) -> bool:
        """Check if this price is less than another."""
        if not isinstance(other, Price):
            raise TypeError("Cannot compare Price with non-Price object")
        if self.currency != other.currency:
            raise ValueError("Cannot compare prices with different currencies")
        return self.amount < other.amount
    
    def __le__(self, other) -> bool:
        """Check if this price is less than or equal to another."""
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        """Check if this price is greater than another."""
        if not isinstance(other, Price):
            raise TypeError("Cannot compare Price with non-Price object")
        if self.currency != other.currency:
            raise ValueError("Cannot compare prices with different currencies")
        return self.amount > other.amount
    
    def __ge__(self, other) -> bool:
        """Check if this price is greater than or equal to another."""
        return self == other or self > other
    
    def __str__(self) -> str:
        """String representation of the price."""
        return self.formatted
    
    def __repr__(self) -> str:
        """Developer representation of the price."""
        return f"Price(amount={self.amount}, currency='{self.currency}')"
    
    def to_dict(self) -> dict:
        """
        Convert price to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "amount": self.amount,
            "currency": self.currency,
            "formatted": self.formatted,
            "amount_in_cents": self.amount_in_cents
        }