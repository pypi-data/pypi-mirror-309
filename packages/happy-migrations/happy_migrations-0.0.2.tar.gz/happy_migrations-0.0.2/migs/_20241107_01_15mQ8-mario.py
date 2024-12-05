"""
mario
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "create table mario(a);",
        "drop table mario;"
    )
]
