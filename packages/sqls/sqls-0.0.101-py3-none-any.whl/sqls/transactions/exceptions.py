# Copyright 2020 - 2024 Marko Durkovic
# SPDX-License-Identifier: Apache-2.0
"""Transaction exceptions."""


class IntegrityError(Exception):
    """IntegrityError from database."""


class OperationalError(Exception):
    """OperationalError from database."""
