#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""ZenML Pro login constants."""

import os

ENV_ZENML_PRO_API_URL = "ZENML_PRO_API_URL"
DEFAULT_ZENML_PRO_API_URL = "https://cloudapi.zenml.io"

ZENML_PRO_API_URL = os.getenv(
    ENV_ZENML_PRO_API_URL, default=DEFAULT_ZENML_PRO_API_URL
)

ENV_ZENML_PRO_URL = "ZENML_PRO_URL"
DEFAULT_ZENML_PRO_URL = "https://cloud.zenml.io"

ZENML_PRO_URL = os.getenv(ENV_ZENML_PRO_URL, default=DEFAULT_ZENML_PRO_URL)

ENV_ZENML_PRO_SERVER_SUBDOMAIN = "ZENML_PRO_SERVER_SUBDOMAIN"
DEFAULT_ZENML_PRO_SERVER_SUBDOMAIN = "cloudinfra.zenml.io"
ZENML_PRO_SERVER_SUBDOMAIN = os.getenv(
    ENV_ZENML_PRO_SERVER_SUBDOMAIN, default=DEFAULT_ZENML_PRO_SERVER_SUBDOMAIN
)
