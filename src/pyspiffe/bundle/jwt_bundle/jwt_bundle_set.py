""""
(C) Copyright 2021 Hewlett Packard Enterprise Development LP

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

"""
This module manages JwtBundleSet objects.
"""

import threading
from typing import Dict, Optional
from pyspiffe.bundle.jwt_bundle.jwt_bundle import JwtBundle
from pyspiffe.spiffe_id.spiffe_id import TrustDomain


class JwtBundleSet(object):
    """JwtBundleSet is a dictionary of JWTBundles objects, keyed by trust domain."""

    def __init__(self, bundles: Dict[TrustDomain, JwtBundle]) -> None:
        """Creates a new JwtBundleSet initialized with the given JWT bundles objects keyed by TrustDomain.

        Args:
            bundles: A dictionary of JwtBundle objects keyed by TrustDomain to initialize the JwtBundleSet.
        """
        self.lock = threading.Lock()
        self._bundles = bundles.copy() if bundles else {}

    def put(self, jwt_bundle: JwtBundle):
        """Adds a new bundle into the set.

        If a bundle already exists for the trust domain, the existing bundle is
        replaced.

        Args:
            jwt_bundle: The new JwtBundle to add.
        """
        with self.lock:
            self._bundles[jwt_bundle.trust_domain()] = jwt_bundle

    def get(self, trust_domain: TrustDomain) -> Optional[JwtBundle]:
        """Returns the JWT bundle of the given trust domain.

        Args:
            trust_domain: The TrustDomain to get a JwtBundle.

        Returns:
            A JwtBundle object for the given TrustDomain.
            None if the TrustDomain is not found in the set.
        """
        with self.lock:
            return self._bundles.get(trust_domain)
