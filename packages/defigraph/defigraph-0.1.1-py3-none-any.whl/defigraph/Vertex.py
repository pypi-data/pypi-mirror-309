from web3 import Web3


class Vertex:
    def __init__(self, name: str, decimals: int, address: str):
        if not isinstance(decimals, int):
            raise TypeError(
                f"Decimals should be type {int} but receved {type(decimals)}"
            )
        if not Web3.is_checksum_address(address):
            raise ValueError(f"Expected checksum address but received {address}")

        self.name = name
        self.decimals = decimals
        self.address = address

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, vertex):
        return (
            self.name == vertex.name
            and self.decimals == vertex.decimals
            and self.address == vertex.address
        )

    def __ne__(self, vertex):
        return (
            self.name != vertex.name
            or self.decimals != vertex.decimals
            or eval(self.address) != eval(vertex.address)
        )

    def __hash__(self):
        return hash(str(self))
