"""Define the HashStrategy interface for hashing tokens."""
from abc import ABC, abstractmethod
import hashlib
from typing import Dict, Type

ALGORITHM_REGISTRY: Dict[str, Type['HashStrategy']] = {}

def register_algorithm(algorithm: str):
    """Decorator to register a hashing algorithm."""
    def decorator(cls: Type['HashStrategy']):
        ALGORITHM_REGISTRY[algorithm] = cls
        return cls

    return decorator

class HashStrategy(ABC):
    """HashStrategy interface for hashing tokens."""
    @abstractmethod
    def hash_token(self, token: str) -> str:
        """Hash the token using the specified algorithm."""
        pass


class HashStrategyFactory:
    """HashStrategyFactory for creating instances of HashStrategy based on the algorithm."""
    @staticmethod
    def get_strategy(algorithm: str) -> HashStrategy:
        """Get the hashing strategy based on the algorithm."""
        strategy_class = ALGORITHM_REGISTRY.get(algorithm)
        if not strategy_class:
            raise ValueError(f"Unsupported hashing algorithm: {algorithm}")

        return strategy_class()
    
@register_algorithm("HS256")
class Sha256Strategy(HashStrategy):
    """Sha256Strategy for hashing tokens using the SHA-256 algorithm."""
    def hash_token(self, token: str) -> str:
        """Hash the token using the SHA-256 algorithm."""
        return hashlib.sha256(token.encode()).hexdigest()
