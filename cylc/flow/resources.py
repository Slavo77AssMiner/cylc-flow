# THIS FILE IS PART OF THE CYLC WORKFLOW ENGINE.
# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
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

"""Extract named resources from the cylc.flow package.

Uses the pkg_resources API in case the package is a compressed archive.
"""

from pathlib import Path
import pkg_resources as pr
from cylc.flow import LOG


# {resource: brief description}
resource_names = {
    'etc/syntax/cylc-mode.el': 'Emacs syntax hihglighting.',
    'etc/syntax/cylc.lang': 'Gedit (gtksourceview) syntax highlighting.',
    'etc/syntax/cylc.vim': 'Vim syntax highlighting.',
    'etc/syntax/cylc.xml': 'Kate syntax highlighting.',
    'etc/cylc-bash-completion':
        'Sets up bash auto-completion for Cylc commands',
    'etc/job.sh': 'Bash functions for Cylc task jobs.',
    'etc/cylc': 'Cylc wrapper script.',
}


def list_resources():
    """List available cylc.flow package resources.

    The API has a "listdir" function but no automatic recursion capability,
    and we have few resources, so listing them explicitly for the moment.
    """
    width = len(max(resource_names, key=len))
    result = [
        f'{resource + (width - len(resource)) * " "}    {meta}'
        for resource, meta in resource_names.items()
    ]
    return result


def get_resources(target_dir, resources=None):
    """Extract cylc.flow resources and write them to a target directory.

    Arguments:
        target_dir - where to put extracted resources, created if necessary
        resources - list of name resources, e.g. ['etc/foo.bar']
    """
    if resources is None:
        resources = resource_names
    for resource in resources:
        if resource not in resource_names:
            raise ValueError(f"Invalid resource name {resource}")
        path = Path(target_dir) / Path(resource).name
        LOG.info(f"Extracting {resource} to {path}")
        pdir = path.parent
        if not pdir.exists():
            pdir.mkdir(parents=True)
        # In spite of the name, this returns a byte array, not a string:
        res = pr.resource_string('cylc.flow', resource)
        with open(path, 'wb') as h:
            h.write(res)
