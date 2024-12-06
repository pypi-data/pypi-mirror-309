"""
Open Quantum Safe (OQS) Python wrapper for liboqs.

The liboqs project provides post-quantum public key cryptography algorithms:
https://github.com/open-quantum-safe/liboqs

This module provides a Python 3 interface to liboqs.
"""

from __future__ import annotations

import ctypes as ct  # to call native
import ctypes.util as ctu
import importlib.metadata  # to determine module version at runtime
import logging
import platform  # to learn the OS we're on
import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Final, TypeVar, cast

if TYPE_CHECKING:
    from types import TracebackType

TKeyEncapsulation = TypeVar("TKeyEncapsulation", bound="KeyEncapsulation")
TSignature = TypeVar("TSignature", bound="Signature")

logger = logging.getLogger(__name__)


def oqs_python_version() -> str | None:
    """pqcow-liboqs version string."""
    try:
        result = importlib.metadata.version("pqcow-liboqs")
    except importlib.metadata.PackageNotFoundError:
        warnings.warn("Please install pqcow-liboqs using pip install", stacklevel=2)
        return None
    return result


# pqcow-liboqs tries to automatically install and load this liboqs version in
# case no other version is found
OQS_VERSION = oqs_python_version()


def _load_shared_obj(name: str, oqs_path_dir: Path | None = None) -> ct.CDLL:
    """Attempt to load shared library."""
    paths: list[Path] = []
    dll = ct.windll if platform.system() == "Windows" else ct.cdll

    if oqs_path_dir and oqs_path_dir.exists():
        if not oqs_path_dir.is_dir():
            msg = f"{oqs_path_dir} is not a directory"
            raise RuntimeError(msg)

        if platform.system() == "Darwin":
            paths.append(oqs_path_dir.absolute() / Path(f"lib{name}").with_suffix(".dylib"))
        elif platform.system() == "Windows":
            paths.append(oqs_path_dir.absolute() / Path(name).with_suffix(".dll"))
        elif platform.system() == "Linux":
            paths.append(oqs_path_dir.absolute() / Path(f"lib{name}").with_suffix(".so"))
        else:
            msg = f"Unsupported platform: {platform.system()}"
            raise RuntimeError(msg)

    # Search typical locations
    if found_lib := ctu.find_library(name):
        paths.insert(0, Path(found_lib))

    if found_lib := ctu.find_library(f"lib{name}"):
        paths.insert(0, Path(found_lib))

    for path in paths:
        if path:
            try:
                lib: ct.CDLL = dll.LoadLibrary(str(path))
            except OSError:
                pass

            else:
                return lib

    msg = f"No {name} shared libraries found"
    raise RuntimeError(msg)


def _load_liboqs(name: str = "oqs", oqs_path: Path | None = None) -> ct.CDLL:
    try:
        liboqs = _load_shared_obj(
            name=name,
            oqs_path_dir=oqs_path or Path(__file__).parent,
        )
        assert liboqs  # noqa: S101
    except RuntimeError:
        sys.exit("Could not load liboqs shared library")

    return liboqs


_liboqs = _load_liboqs()

# Expected return value from native OQS functions
OQS_SUCCESS: Final[int] = 0
OQS_ERROR: Final[int] = -1


def native() -> ct.CDLL:
    """Handle to native liboqs handler."""
    return _liboqs


# liboqs initialization
native().OQS_init()


def oqs_version() -> str:
    """`liboqs` version string."""
    native().OQS_version.restype = ct.c_char_p
    return ct.c_char_p(native().OQS_version()).value.decode("UTF-8")  # type: ignore[union-attr]


# Warn the user if the liboqs version differs from pqcow-liboqs version
if oqs_version() != oqs_python_version():
    warnings.warn(
        f"liboqs version {oqs_version()} differs from pqcow-liboqs version "
        f"{oqs_python_version()}",
        stacklevel=2,
    )


class MechanismNotSupportedError(Exception):
    """Exception raised when an algorithm is not supported by OQS."""

    def __init__(self, alg_name: str) -> None:
        """:param alg_name: requested algorithm name."""
        self.alg_name = alg_name
        self.message = f"{alg_name} is not supported by OQS"


class MechanismNotEnabledError(MechanismNotSupportedError):
    """Exception raised when an algorithm is supported but not enabled by OQS."""

    def __init__(self, alg_name: str) -> None:
        """:param alg_name: requested algorithm name."""
        self.alg_name = alg_name
        self.message = f"{alg_name} is supported but not enabled by OQS"


class KeyEncapsulation(ct.Structure):
    """
    An OQS KeyEncapsulation wraps native/C liboqs OQS_KEM structs.

    The wrapper maps methods to the C equivalent as follows:

    Python            |  C liboqs
    -------------------------------
    generate_keypair  |  keypair
    encap_secret      |  encaps
    decap_secret      |  decaps
    free              |  OQS_KEM_free
    """

    _fields_: ClassVar[list[tuple[str, Any]]] = [
        ("method_name", ct.c_char_p),
        ("alg_version", ct.c_char_p),
        ("claimed_nist_level", ct.c_ubyte),
        ("ind_cca", ct.c_ubyte),
        ("length_public_key", ct.c_size_t),
        ("length_secret_key", ct.c_size_t),
        ("length_ciphertext", ct.c_size_t),
        ("length_shared_secret", ct.c_size_t),
        ("keypair_cb", ct.c_void_p),
        ("encaps_cb", ct.c_void_p),
        ("decaps_cb", ct.c_void_p),
    ]

    def __init__(self, alg_name: str, secret_key: int | bytes | None = None) -> None:
        """
        Create new KeyEncapsulation with the given algorithm.

        :param alg_name: KEM mechanism algorithm name. Enabled KEM mechanisms can be obtained with
        get_enabled_KEM_mechanisms().
        :param secret_key: optional if generating by generate_keypair() later.
        """
        super().__init__()
        self.alg_name = alg_name
        if alg_name not in _enabled_KEMs:
            # perhaps it's a supported but not enabled alg
            if alg_name in _supported_KEMs:
                raise MechanismNotEnabledError(alg_name)
            raise MechanismNotSupportedError(alg_name)

        self._kem = native().OQS_KEM_new(ct.create_string_buffer(alg_name.encode()))

        self.details = {
            "name": self._kem.contents.method_name.decode(),
            "version": self._kem.contents.alg_version.decode(),
            "claimed_nist_level": int(self._kem.contents.claimed_nist_level),
            "is_ind_cca": bool(self._kem.contents.ind_cca),
            "length_public_key": int(self._kem.contents.length_public_key),
            "length_secret_key": int(self._kem.contents.length_secret_key),
            "length_ciphertext": int(self._kem.contents.length_ciphertext),
            "length_shared_secret": int(self._kem.contents.length_shared_secret),
        }

        if secret_key:
            self.secret_key = ct.create_string_buffer(
                secret_key,
                self._kem.contents.length_secret_key,
            )

    def __enter__(self: TKeyEncapsulation) -> TKeyEncapsulation:
        return self

    def __exit__(
        self,
        ctx_type: type[BaseException] | None,
        ctx_value: BaseException | None,
        ctx_traceback: TracebackType | None,
    ) -> None:
        self.free()

    def generate_keypair(self) -> bytes | int:
        """
        Generate a new keypair and returns the public key.

        If needed, the secret key can be obtained with export_secret_key().
        """
        public_key = ct.create_string_buffer(self._kem.contents.length_public_key)
        self.secret_key = ct.create_string_buffer(self._kem.contents.length_secret_key)
        rv = native().OQS_KEM_keypair(
            self._kem,
            ct.byref(public_key),
            ct.byref(self.secret_key),
        )
        return bytes(public_key) if rv == OQS_SUCCESS else 0

    def export_secret_key(self) -> bytes:
        """Export the secret key."""
        return bytes(self.secret_key)

    def encap_secret(self, public_key: int | bytes) -> tuple[bytes, bytes | int]:
        """
        Generate and encapsulates a secret using the provided public key.

        :param public_key: the peer's public key.
        """
        my_public_key = ct.create_string_buffer(
            public_key,
            self._kem.contents.length_public_key,
        )
        ciphertext: ct.Array[ct.c_char] = ct.create_string_buffer(
            self._kem.contents.length_ciphertext,
        )
        shared_secret: ct.Array[ct.c_char] = ct.create_string_buffer(
            self._kem.contents.length_shared_secret,
        )
        rv = native().OQS_KEM_encaps(
            self._kem,
            ct.byref(ciphertext),
            ct.byref(shared_secret),
            my_public_key,
        )

        # TODO: What should it return?
        #  1. tuple[bytes | int, bytes | int]
        #  2. tuple[bytes, bytes | int]
        #  3. tuple[bytes, bytes] | int
        return (
            bytes(cast(bytes, ciphertext)),
            bytes(cast(bytes, shared_secret)) if rv == OQS_SUCCESS else 0,
        )

    def decap_secret(self, ciphertext: int | bytes) -> bytes | int:
        """
        Decapsulate the ciphertext and returns the secret.

        :param ciphertext: the ciphertext received from the peer.
        """
        my_ciphertext = ct.create_string_buffer(
            ciphertext,
            self._kem.contents.length_ciphertext,
        )
        shared_secret: ct.Array[ct.c_char] = ct.create_string_buffer(
            self._kem.contents.length_shared_secret,
        )
        rv = native().OQS_KEM_decaps(
            self._kem,
            ct.byref(shared_secret),
            my_ciphertext,
            self.secret_key,
        )
        return bytes(cast(bytes, shared_secret)) if rv == OQS_SUCCESS else 0

    def free(self) -> None:
        """Releases the native resources."""
        if hasattr(self, "secret_key"):
            native().OQS_MEM_cleanse(
                ct.byref(self.secret_key),
                self._kem.contents.length_secret_key,
            )
        native().OQS_KEM_free(self._kem)

    def __repr__(self) -> str:
        return f"Key encapsulation mechanism: {self._kem.contents.method_name.decode()}"


native().OQS_KEM_new.restype = ct.POINTER(KeyEncapsulation)
native().OQS_KEM_alg_identifier.restype = ct.c_char_p


def is_kem_enabled(alg_name: str) -> bool:
    """
    Return True if the KEM algorithm is enabled.

    :param alg_name: a KEM mechanism algorithm name.
    """
    return native().OQS_KEM_alg_is_enabled(ct.create_string_buffer(alg_name.encode()))


_KEM_alg_ids = [native().OQS_KEM_alg_identifier(i) for i in range(native().OQS_KEM_alg_count())]
_supported_KEMs: list[str] = [i.decode() for i in _KEM_alg_ids]  # noqa: N816
_enabled_KEMs: list[str] = [i for i in _supported_KEMs if is_kem_enabled(i)]  # noqa: N816


def get_enabled_kem_mechanisms() -> list[str]:
    """Return the list of enabled KEM mechanisms."""
    return _enabled_KEMs


def get_supported_kem_mechanisms() -> list[str]:
    """Return the list of supported KEM mechanisms."""
    return _supported_KEMs


class Signature(ct.Structure):
    """
    An OQS Signature wraps native/C liboqs OQS_SIG structs.

    The wrapper maps methods to the C equivalent as follows:

    Python            |  C liboqs
    -------------------------------
    generate_keypair  |  keypair
    sign              |  sign
    verify            |  verify
    free              |  OQS_SIG_free
    """

    _fields_: ClassVar[list[tuple[str, Any]]] = [
        ("method_name", ct.c_char_p),
        ("alg_version", ct.c_char_p),
        ("claimed_nist_level", ct.c_ubyte),
        ("euf_cma", ct.c_ubyte),
        ("length_public_key", ct.c_size_t),
        ("length_secret_key", ct.c_size_t),
        ("length_signature", ct.c_size_t),
        ("keypair_cb", ct.c_void_p),
        ("sign_cb", ct.c_void_p),
        ("verify_cb", ct.c_void_p),
    ]

    def __init__(self, alg_name: str, secret_key: int | bytes | None = None) -> None:
        """
        Create new Signature with the given algorithm.

        :param alg_name: a signature mechanism algorithm name. Enabled signature mechanisms can be
        obtained with get_enabled_sig_mechanisms().
        :param secret_key: optional, if generated by generate_keypair().
        """
        super().__init__()
        if alg_name not in _enabled_sigs:
            # perhaps it's a supported but not enabled alg
            if alg_name in _supported_sigs:
                raise MechanismNotEnabledError(alg_name)
            raise MechanismNotSupportedError(alg_name)

        self._sig = native().OQS_SIG_new(ct.create_string_buffer(alg_name.encode()))
        self.details = {
            "name": self._sig.contents.method_name.decode(),
            "version": self._sig.contents.alg_version.decode(),
            "claimed_nist_level": int(self._sig.contents.claimed_nist_level),
            "is_euf_cma": bool(self._sig.contents.euf_cma),
            "length_public_key": int(self._sig.contents.length_public_key),
            "length_secret_key": int(self._sig.contents.length_secret_key),
            "length_signature": int(self._sig.contents.length_signature),
        }

        if secret_key:
            self.secret_key = ct.create_string_buffer(
                secret_key,
                self._sig.contents.length_secret_key,
            )

    def __enter__(self: TSignature) -> TSignature:
        return self

    def __exit__(
        self,
        ctx_type: type[BaseException] | None,
        ctx_value: BaseException | None,
        ctx_traceback: TracebackType | None,
    ) -> None:
        self.free()

    def generate_keypair(self) -> bytes | int:
        """
        Generate a new keypair and returns the public key.

        If needed, the secret key can be obtained with export_secret_key().
        """
        public_key: ct.Array[ct.c_char] = ct.create_string_buffer(
            self._sig.contents.length_public_key,
        )
        self.secret_key = ct.create_string_buffer(self._sig.contents.length_secret_key)
        rv = native().OQS_SIG_keypair(
            self._sig,
            ct.byref(public_key),
            ct.byref(self.secret_key),
        )
        return bytes(cast(bytes, public_key)) if rv == OQS_SUCCESS else 0

    def export_secret_key(self) -> bytes:
        """Export the secret key."""
        return bytes(self.secret_key)

    def sign(self, message: bytes) -> bytes | int:
        """
        Signs the provided message and returns the signature.

        :param message: the message to sign.
        """
        # Provide length to avoid extra null char
        my_message = ct.create_string_buffer(message, len(message))
        message_len = ct.c_int(len(my_message))
        signature: ct.Array[ct.c_char] = ct.create_string_buffer(
            self._sig.contents.length_signature,
        )
        sig_len = ct.c_int(
            self._sig.contents.length_signature,
        )  # initialize to maximum signature size
        rv = native().OQS_SIG_sign(
            self._sig,
            ct.byref(signature),
            ct.byref(sig_len),
            my_message,
            message_len,
            self.secret_key,
        )

        return bytes(cast(bytes, signature[: sig_len.value])) if rv == OQS_SUCCESS else 0

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        """
        Verify the provided signature on the message; returns True if valid.

        :param message: the signed message.
        :param signature: the signature on the message.
        :param public_key: the signer's public key.
        """
        # Provide length to avoid extra null char
        my_message = ct.create_string_buffer(message, len(message))
        message_len = ct.c_int(len(my_message))

        # Provide length to avoid extra null char in sig
        my_signature = ct.create_string_buffer(signature, len(signature))
        sig_len = ct.c_int(len(my_signature))
        my_public_key = ct.create_string_buffer(
            public_key,
            self._sig.contents.length_public_key,
        )
        rv = native().OQS_SIG_verify(
            self._sig,
            my_message,
            message_len,
            my_signature,
            sig_len,
            my_public_key,
        )
        return rv == OQS_SUCCESS

    def free(self) -> None:
        """Releases the native resources."""
        if hasattr(self, "secret_key"):
            native().OQS_MEM_cleanse(
                ct.byref(self.secret_key),
                self._sig.contents.length_secret_key,
            )
        native().OQS_SIG_free(self._sig)

    def __repr__(self) -> str:
        return f"Signature mechanism: {self._sig.contents.method_name.decode()}"


native().OQS_SIG_new.restype = ct.POINTER(Signature)
native().OQS_SIG_alg_identifier.restype = ct.c_char_p


def is_sig_enabled(alg_name: str) -> bool:
    """
    Return True if the signature algorithm is enabled.

    :param alg_name: a signature mechanism algorithm name.
    """
    return native().OQS_SIG_alg_is_enabled(ct.create_string_buffer(alg_name.encode()))


_sig_alg_ids = [native().OQS_SIG_alg_identifier(i) for i in range(native().OQS_SIG_alg_count())]
_supported_sigs = [i.decode() for i in _sig_alg_ids]
_enabled_sigs = [i for i in _supported_sigs if is_sig_enabled(i)]


def get_enabled_sig_mechanisms() -> list[str]:
    """Return the list of enabled signature mechanisms."""
    return _enabled_sigs


def get_supported_sig_mechanisms() -> list[str]:
    """Return the list of supported signature mechanisms."""
    return _supported_sigs
