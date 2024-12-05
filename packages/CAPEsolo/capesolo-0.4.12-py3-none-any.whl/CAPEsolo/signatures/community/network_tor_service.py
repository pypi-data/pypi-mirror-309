# Copyright (C) 2012 Claudio "nex" Guarnieri (@botherder)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from CAPEsolo.capelib.signatures import Signature


class TorHiddenService(Signature):
    name = "network_tor_service"
    description = "Creates a Tor Hidden Service on the machine"
    severity = 3
    categories = ["network", "stealth"]
    authors = ["nex"]
    minimum = "0.5"
    ttps = ["T1188"]  # MITRE v6
    ttps += ["T1090"]  # MITRE v6,7,8
    ttps += ["T1090.003"]  # MITRE v7,8
    ttps += ["U0903"]  # Unprotect

    def run(self):
        indicators = [".*\\\\tor\\\\hidden_service\\\\private_key$", ".*\\\\tor\\\\hidden_service\\\\hostname$"]

        for indicator in indicators:
            if self.check_file(pattern=indicator, regex=True):
                return True

        return False
