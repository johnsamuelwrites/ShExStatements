#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import re

class Type:
  def __init__(self, name):
    self.name = name[2:]
  
  def __str__(self):
    return self.name

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

class TypeList:
  value_list = []
  def __init__(self, value_list):
    self.value_list = value_list

  def add(self, value):
    if(type(value) == Type):
      self.value_list.append(value)
    else:
      raise Exception("Mixing of non-type values not allowed")

  def get_value_list(self):
    return self.value_list

  def __str__(self):
    string = ""
    for s in self.value_list:
      string = string + str(s) + " "
    return string

class ValueList:
  value_list = []
  def __init__(self, value_list):
    self.value_list = value_list

  def add(self, value):
    if(type(value) == Value):
      self.value_list.append(value)

  def get_value_list(self):
    return self.value_list

  def __str__(self):
    string = ""
    for s in self.value_list:
      string = string + str(s) + " "
    return string

class Cardinality:
  def __init__(self, cardinality):
    self.cardinality = cardinality

class ShExStatement:
  def __init__(self, node, prop, value, cardinality=None, comment=None):
    self.node = node
    self.prop = prop
    self.value = value
    self.cardinality = cardinality
    self.comment = comment

  def get_node(self):
    return self.node

  def get_prop(self):
    return self.prop

  def get_value(self):
    return self.value

  def get_cardinality(self):
    return self.cardinality

  def get_comment(self):
    return self.comment

  def __str__(self):
    return(str(self.node) + "|" +
           str(self.prop) + "|" +
           str(self.value) + "|" +
           str(self.cardinality) +
           str(self.comment) + "\n"
          )

class ShExStatements:
  def __init__(self, statements):
    self.statements = statements 
    self.prefixes = set()
    self.imports = set()

  def add(self, statement):
    self.statements.append(statement)

  def add_prefixes(self, prefixes):
    self.prefixes.update(prefixes)

  def add_imports(self, imports):
    self.imports.update(imports)

  def __str__(self):
    string = ""
    for s in self.statements:
      string = string + str(s)
    return string

  def get_statements(self):
    return self.statements

  def generate_shex(self):
    start = None
    shape = {}
    shapeconstraints = {}
    for statement in self.statements:
      node = str(statement.get_node())
      constraint = None
      combination = []
      if node not in shape:
        shape[node] = []
        shapeconstraints[node] = []
        if not start:
          start = node
      prop = statement.get_prop()
      value = statement.get_value()
      if (prop == "EXTRA"):
        constraint = prop + " " + str(value)
      elif (prop == "CLOSED"):
        constraint = prop
      else:
        combination.append(prop)
        combination.append(" ")
        if (type(value) == Node and str(value).startswith("@")):
          value = "@<" + str(value)[1:] + ">"
        elif type(value) == NodeKind:
          value = str(value)
        elif type(value) == Value or type(value) == ValueList:
          value = "[ " + str(value) + " ]"
        elif type(value) == Type or type(value) == TypeList:
          value = str(value)
        combination.append(value)

        if statement.get_cardinality():
          if (statement.get_cardinality() in {"*", "+", "?"}):
            combination.append(statement.get_cardinality())
          else: # numerical values
            combination.append("{" + statement.get_cardinality() + "}")
        combination.append(" ;")
        if statement.get_comment():
          combination.append(statement.get_comment())
        shape[node].append(combination)
      if(constraint):
        shapeconstraints[node].append(constraint)
    
    shex_statement_str = ""
    if self.imports:
       for imp in self.imports:
         shex_statement_str = shex_statement_str + "IMPORT <" + imp + ">\n"
    if self.prefixes:
       for prefix in self.prefixes:
         shex_statement_str = shex_statement_str + "PREFIX " + prefix[0] + ": " + prefix[1] + "\n"
    if start is not None:
        shex_statement_str = shex_statement_str + "start = @" + "<" + str(start)[1:] + ">" + "\n"

    for key in shape.keys():
        shex_statement_str = shex_statement_str + "<" + str(key)[1:] + ">" 
        if shapeconstraints[key]:
            shex_statement_str = shex_statement_str + "  " + " ".join(shapeconstraints[key]) 

        shex_statement_str = shex_statement_str + " {" + "\n"
        for combination in shape[key]:
            shex_statement_str = shex_statement_str + "  " + "".join(combination) + "\n"
        shex_statement_str = shex_statement_str + "}" + "\n"

    return shex_statement_str
