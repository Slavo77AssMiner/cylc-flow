#!/usr/bin/env bash
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
#-------------------------------------------------------------------------------
# Test validation for a bad Jinja2 TemplateSyntaxError workflow.
. "$(dirname "$0")/test_header"
#-------------------------------------------------------------------------------
set_test_number 2
install_workflow "${TEST_NAME_BASE}" "${TEST_NAME_BASE}"
#-------------------------------------------------------------------------------
TEST_NAME="${TEST_NAME_BASE}-val"
run_fail "${TEST_NAME}" cylc validate .
cmp_ok "${TEST_NAME}.stderr" <<'__ERROR__'
Jinja2Error: Encountered unknown tag 'end'.
Jinja was looking for the following tags: 'elif' or 'else' or 'endif'.
The innermost block that needs to be closed is 'if'.
Context lines:
        {% if true %}
        R1 = foo
        {% end if %	<-- TemplateSyntaxError
__ERROR__
#-------------------------------------------------------------------------------
purge
exit
