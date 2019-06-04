from .sparsegraph import SparseGraph

class HamiltonianKey:
    '''
    HamiltonianKey(n)

    Creates empty Hamiltonian graph-based key with size of n vertices.
    '''
    def __init__(self, n):
        # SparseGraph describing public key
        self.public_key = SparseGraph(n)
        # tuple describing subsequent vertices in the Hamiltonian cycle
        # may be empty if only public key is known
        self.private_key = ()

    '''
    key.write_private()

    Returns serialized public key and private key as parseable bytestring.
    '''
    def write_private(self):
        #unimplemented
        pass

    '''
    key.write_public()

    Returns serialized public key as parseable bytestring.
    '''
    def write_public(self):
        #unimplemented
        pass

    '''
    HamiltonianKey.from_bytestring()

    Returns a HamiltonianKey based on a bytestring of a serialized
    key (public or (public, private)).
    '''
    @staticmethod
    def from_bytestring(self, string):
        #unimplemented
        pass

    def __str__(self):
        return 'HamiltonianKey(public_key=' + str(self.public_key) + ', private_key=' + str(self.private_key) + ')'

    def __repr__(self):
        return str(self)
