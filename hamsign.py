#!/usr/bin/env python3
import argparse

from modules.genkey import generate_key
from modules.hamiltoniankey import HamiltonianKey
from modules.signature import (
    sign, verify_sign, write_signature, read_signature
)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # genhamkey subcommand
    genhamkey = subparsers.add_parser(
        'genhamkey', help='generates new hamiltonian key.'
    )
    genhamkey.set_defaults(func=genkey_command)
    genhamkey.add_argument(
        '-out', help='output filename for private key', required=True
    )
    genhamkey.add_argument('-pubout', help='output filename for public key')
    genhamkey.add_argument(
        'n', metavar='N', type=int, help='key security parameter'
    )

    # hamkey subcommand
    hamkey = subparsers.add_parser(
        'hamkey',
        help=(
            'prints key information and allows to extract public key out of pr'
            'ivate key'
            )
    )
    hamkey.set_defaults(func=key_command)
    hamkey.add_argument(
        '-in', help='filename of the key', dest='input', required=True
    )
    hamkey.add_argument(
        '-inform', action='store_true', help='show information about the key'
    )
    hamkey.add_argument(
        '-pubout', help='extracts public key to a given location'
    )

    # hamsign subcommand
    hamsign = subparsers.add_parser(
        'hamsign', help='Creates a signature of a given file'
    )
    hamsign.set_defaults(func=sign_command)
    hamsign.add_argument(
        '-key', help='name of the private key file to sing with', required=True
    )
    hamsign.add_argument(
        '-out', help='output filename for the signature', required=True
    )
    hamsign.add_argument(
        'file', metavar='filename', help='name of the plain file to sign'
    )

    # hamverify subcommand
    hamverify = subparsers.add_parser(
        'hamverify', help='checks if given signature of a file is correct'
    )
    hamverify.set_defaults(func=verify_command)
    hamverify.add_argument(
        '-key',
        help='name of the key file for signature verification',
        required=True
    )
    hamverify.add_argument(
        '-signature', help='name of the signature file to verify',
        required=True
    )
    hamverify.add_argument(
        'file', metavar='filename', help='name of the plain file to verify'
    )

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()


def genkey_command(args):
    key = generate_key(args.n)

    try:
        with open(args.out, 'wb') as f:
            f.write(key.write_private())
        print('Private key saved to', args.out)
    except Exception as e:
        print("Error when saving private key:", e)
        exit()

    if args.pubout:
        write_public_key(key, args.pubout)


def key_command(args):
    key = read_key(args.input)

    if args.inform:
        print(key)

    if args.pubout:
        write_public_key(key, args.pubout)


def sign_command(args):
    key = read_key(args.key)

    try:
        with open(args.file, 'rb') as f:
            signature = sign(f, key)
    except OSError as e:
        print("Error opening file:", e)
        exit()
    except Exception as e:
        print("Error when signing:", e)
        exit()

    try:
        with open(args.out, 'w') as f:
            f.write(write_signature(signature))
    except Exception as e:
        print("Error when saving signature:", e)
        exit()

    print("Signature written to", args.out)


def verify_command(args):
    key = read_key(args.key)

    try:
        with open(args.signature, 'r') as f:
            signature = read_signature(f.read())
    except Exception as e:
        print("Error opening signature:", e)
        exit()

    try:
        with open(args.file, 'rb') as f:
            if verify_sign(f, key, signature):
                print("Signature valid")
            else:
                print("Signature invalid")
    except OSError as e:
        print("Error opening file:", e)
        exit()
    except Exception as e:
        print("Error when veryfing signature:", e)
        exit()


def write_public_key(key, path):
    try:
        with open(path, 'wb') as f:
            f.write(key.write_public())
        print('Public key saved to', path)
    except Exception as e:
        print("Error when writing public key:", e)
        exit()


def read_key(path):
    try:
        with open(path, 'rb') as f:
            key = HamiltonianKey.from_bytestring(f.read())
        return key
    except Exception as e:
        print("Error when reading key:", e)
        exit()


if __name__ == "__main__":
    main()
