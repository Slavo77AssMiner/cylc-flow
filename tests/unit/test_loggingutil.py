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

import logging
import tempfile
import pytest

from pytest import param
from unittest import mock

from cylc.flow import LOG
from cylc.flow.loggingutil import (
    TimestampRotatingFileHandler, CylcLogFormatter)


@mock.patch("cylc.flow.loggingutil.glbl_cfg")
def test_value_error_raises_system_exit(
    mocked_glbl_cfg,
):
    """Test that a ValueError when writing to a log stream won't result
    in multiple exceptions (what could lead to infinite loop in some
    occasions. Instead, it **must** raise a SystemExit"""
    with tempfile.NamedTemporaryFile() as tf:
        # mock objects used when creating the file handler
        mocked = mock.MagicMock()
        mocked_glbl_cfg.return_value = mocked
        mocked.get.return_value = 100
        file_handler = TimestampRotatingFileHandler(tf.name, False)
        # next line is important as pytest can have a "Bad file descriptor"
        # due to a FileHandler with default "a" (pytest tries to r/w).
        file_handler.mode = "a+"

        # enable the logger
        LOG.setLevel(logging.INFO)
        LOG.addHandler(file_handler)

        # Disable raising uncaught exceptions in logging, due to file
        # handler using stdin.fileno. See the following links for more.
        # https://github.com/pytest-dev/pytest/issues/2276 &
        # https://github.com/pytest-dev/pytest/issues/1585
        logging.raiseExceptions = False

        # first message will initialize the stream and the handler
        LOG.info("What could go")

        # here we change the stream of the handler
        old_stream = file_handler.stream
        file_handler.stream = mock.MagicMock()
        file_handler.stream.seek = mock.MagicMock()
        # in case where
        file_handler.stream.seek.side_effect = ValueError

        try:
            # next call will call the emit method and use the mocked stream
            LOG.info("wrong?!")
            raise Exception("Exception SystemError was not raised")
        except SystemExit:
            pass
        finally:
            # clean up
            file_handler.stream = old_stream
            # for log_handler in LOG.handlers:
            #     log_handler.close()
            file_handler.close()
            LOG.removeHandler(file_handler)
            logging.raiseExceptions = True


@pytest.mark.parametrize(
    'dev_info, expect',
    [
        param(
            True,
            (
                '%(asctime)s %(levelname)-2s - [%(module)s:%(lineno)d] - '
                '%(message)s'
            ),
            id='dev_info=True'
        ),
        param(
            False,
            '%(asctime)s %(levelname)-2s - %(message)s',
            id='dev_info=False'
        )
    ]
)
def test_CylcLogFormatter__init__dev_info(dev_info, expect):
    """dev_info switch changes the logging format string."""
    formatter = CylcLogFormatter(dev_info=dev_info)
    assert formatter._fmt == expect
