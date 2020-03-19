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
    return self.name

class NodeKind:
  def __init__(self, name):
    self.name = name
  
  def __str__(self):
    return self.name

class Value:
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return self.name

class ValueList:
  value_list = []
  def __init__(self, value_list):
    self.value_list = value_list

  def add(self, value):
    self.value_list.append(value)

  def get_value_list(self):
    return self.value_list

  def __str__(self):
    string = ""
    for s in self.value_list:
      string = string + str(s) + " "
    return string

class Constraint:
  def __init__(self, constraint):
    self.constraint = constraint

class ShExStatement:
  def __init__(self, node, prop, value, constraint=None):
    self.node = node
    self.prop = prop
    self.value = value
    self.constraint = constraint

  def get_node(self):
    return self.node

  def get_prop(self):
    return self.prop

  def get_value(self):
    return self.value

  def get_constraint(self):
    return self.constraint

  def __str__(self):
    return(str(self.node) + "|" +
           str(self.prop) + "|" +
           str(self.value) + "|" +
           str(self.constraint) + "\n"
          )

class ShExStatements:
  def __init__(self, statements):
    self.statements = statements 

  def add(self, statement):
    self.statements.append(statement)

  def __str__(self):
    string = ""
    for s in self.statements:
      string = string + str(s)
    return string

  def get_statements(self):
    return self.statements

  def generate_shex(self):
    start = None
    nodeconstraints = {}
    for statement in self.statements:
      node = str(statement.get_node())
      combination = []
      if node not in nodeconstraints:
        nodeconstraints[node] = []
        if not start:
          start = node
      combination.append(statement.get_prop())
      value = statement.get_value()
      if (type(value) == Node and str(value).startswith("@")):
        value = "@<" + str(value)[1:] + ">"
      elif type(value) == NodeKind:
        value = str(value)
      elif type(value) == Value or type(value) == ValueList:
        value = "[ " + str(value) + " ]"
      combination.append(value)

      if (statement.get_constraint()):
        combination.append(statement.get_constraint())
      nodeconstraints[node].append(combination)
    
    shex_statement_str = ""
    if start is not None:
        shex_statement_str = shex_statement_str + "start = @" + "<" + str(start)[1:] + ">" + "\n"

    for key in nodeconstraints.keys():
        shex_statement_str = shex_statement_str + "<" + str(key)[1:] + ">" + " {" + "\n"
        for combination in nodeconstraints[key]:
            shex_statement_str = shex_statement_str + "  " + " ".join(combination) + " ;"  + "\n"
        shex_statement_str = shex_statement_str + "}" + "\n"

    return shex_statement_str
