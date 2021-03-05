#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

class UnrecognizedCharacterError(Exception):
    """
      UnrecognizedCharacterError
    """

    def __init__(self, message):
        """
        Unrecognized character error

        Parameters
        ----------
            self :   
              The name to use.
            message:  str
               error message
        """
        super(UnrecognizedCharacterError, self).__init__(message)
        self.message = message


class ParserError(Exception):
    """
      ParserError
    """

    def __init__(self, message):
        """
        Parser error

        Parameters
        ----------
            self :   
              The name to use.
            message:  str
               error message
        """
        super(ParserError, self).__init__(message)
        self.message = message
