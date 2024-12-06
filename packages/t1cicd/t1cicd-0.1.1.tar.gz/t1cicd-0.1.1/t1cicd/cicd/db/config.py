import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    port: int
    dbname: str
    user: str
    password: str
    min_size: int
    max_size: int

    @classmethod
    def from_env(cls) -> "DBConfig":
        """Create configuration from environment variables"""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "cs6510"),
            user=os.getenv("DB_USER", "postgresql"),
            password=os.getenv("DB_PASSWORD", ""),
            min_size=int(os.getenv("DB_POOL_MIN_SIZE", "1")),
            max_size=int(os.getenv("DB_POOL_MAX_SIZE", "5")),
        )

    @property
    def conninfo(self) -> str:
        return (
            f"host={self.host} port={self.port} dbname={self.dbname} user={self.user}"
        )
