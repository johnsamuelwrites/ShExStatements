#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

class Node:
  def __init__(self, name):
    self.name = name
  
  def __str__(self):
    return (self.name)

class Value:
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return (self.name)

class ValueSet:
  def __init__(self, values = []):
     self.values = values

  def add_value (self, value):
     self.values.add(values)

  def __str__(self):
    return (','.join(self.values))


class Constraint:
  def __init__(self, constraint):
    self.constraint = constraint

class ShExStatement:
  def __init__(self, node, prop, value, constraints=None):
    self.node = node
    self.prop = node
    self.value = node
    self.constraints = constraints
    pass

class ShExStatements:
  def __init__(self, statements = []):
    self.statements = statements

  def add(statement):
    self.statements.add(statement)
