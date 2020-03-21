#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

class UnrecognizedCharacterError(Exception):
  def __init__(self, message):
    super(UnrecognizedCharacterError, self).__init__(message)
    self.message = message

class ParserError(Exception):
  def __init__(self, message):
    super(ParserError, self).__init__(message)
    self.message = message
