#!/usr/local/autopkg/python
#
# Copyright 2020 Anver Housseini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## Added in Arch Type - Ryan Muske
##
"""See docstring for HomebrewCaskURL class"""

import json

from autopkglib import URLGetter

__all__ = ["HomebrewCaskURL"]


class HomebrewCaskURL(URLGetter):
    """An AutoPkg processor which reads the download url from the Homebrew Cask API."""

    input_variables = {
        "cask_name": {
            "required": True,
            "description": (
                "Name of cask to fetch, as would be given to the 'brew' command. Example: 'firefox'"
            ),
        },
        "arch_type": {
            "required": False,
            "default": "amd64",
            "description": (
                "Targeted Build Archiecture. Example: 'arm64'"
            ),
        }
    }
    output_variables = {
        "url": {"description": ("URL for the Cask's download.")},
        "version": {"description": ("Version infrom from formula")}
        }

    description = __doc__

    def main(self):
        """Grab url from cask"""

        homebrew_api_baseurl = "https://formulae.brew.sh/api/cask"
        archiecture_type: str = self.env['arch_type']
        cask_url = f"{homebrew_api_baseurl}/{self.env['cask_name']}.json"

        manifest = self.download(cask_url)

        data = json.loads(manifest.decode("utf-8"))
        parsedversion = data["version"]

        if archiecture_type.lower() in ['arm64', 'arm']:
            parsed = data['variations']["arm64_ventura"]["url"]
        else:
            parsed = data["url"]

        self.env["version"] = parsedversion
        self.env["url"] = parsed
        self.output(f"Got URL {self.env['url']} for cask '{self.env['cask_name']}':")


if __name__ == "__main__":
    PROCESSOR = HomebrewCaskURL()
    PROCESSOR.execute_shell()
