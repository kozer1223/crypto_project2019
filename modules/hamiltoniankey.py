from .sparsegraph import SparseGraph
import struct

class HamiltonianKey:

    def __init__(self, n):
        """
        Creates empty Hamiltonian graph-based key with size of n vertices.
        """
        # SparseGraph describing public key
        self.public_key = SparseGraph(n)
        # tuple describing subsequent vertices in the Hamiltonian cycle
        # may be empty if only public key is known
        self.private_key = ()

    # Serialized key specification:
    # byte              value
    # 0                 n (2 bytes)
    # 2                 |E| (4 bytes)
    # 6                 edges (4 * |E| bytes)
    #     6 + 4i        vertex u of ith edge (2 bytes)
    #     8 + 4i        vertex v of ith edge (2 bytes)
    # (if private key)
    # 6 + 4|E|          Hamiltonian cycle (2 * n bytes)
    #     6 + 4|E| + 2i vertex u in ith position i cycle (2 bytes)

    def write_private(self):
        """
        Returns serialized public key and private key as parseable bytestring.
        """
        data = self.write_public()
        for v in self.private_key:
            data += struct.pack('H', v)
        return data

    def write_public(self):
        """"
        Returns serialized public key as parseable bytestring.
        """
        data = b''
        data += struct.pack('H', self.public_key.n)
        data += struct.pack('I', self.public_key.edges_count())
        for (u, v) in self.public_key.edges():
            data += struct.pack('HH', u, v)
        return data

    @staticmethod
    def from_bytestring(string):
        """
        Returns a HamiltonianKey based on a bytestring of a serialized
        key (public or (public, private)).
        """
        n = struct.unpack('H', string[0:2])[0]
        E = struct.unpack('I', string[2:6])[0]
        key = HamiltonianKey(n)
        for i in range(E):
            offset = 6 + 4 * i
            (u, v) = struct.unpack('HH', string[offset:(offset + 4)])
            key.public_key.add_edge(u, v)
        try:
            offset = 6 + E * 4
            key.private_key = tuple(
                struct.unpack('H', string[(offset + 2*i):(offset + 2*i + 2)])[0]
                for i in range(n)
                )
        except:
            pass
        return key

    def __str__(self):
        return 'HamiltonianKey(public_key=' + str(self.public_key) + ', private_key=' + str(self.private_key) + ')'

    def __repr__(self):
        return str(self)
