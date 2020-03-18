#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import re

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

class Constraint:
  def __init__(self, constraint):
    self.constraint = constraint

class ShExStatement:
  def __init__(self, node, prop, value, constraints=None):
    self.node = node
    self.prop = prop
    self.value = value
    self.constraints = constraints

  def get_node(self):
    return self.node

  def get_prop(self):
    return self.prop

  def get_value(self):
    return self.value

  def get_constraints(self):
    return self.constraints

  def __str__(self):
    return(str(self.node) + "|" +
           str(self.prop) + "|" +
           str(self.value) + "|" +
           str(self.constraints)
          )

class ShExStatements:
  def __init__(self, statements = []):
    self.statements = statements

  def add(statement):
    self.statements.add(statement)

  def __str__(self):
    string = ""
    for s in self.statements:
      string = string + str(s)
    return (string)

  def generate_shex(shexstatement):
    pass
