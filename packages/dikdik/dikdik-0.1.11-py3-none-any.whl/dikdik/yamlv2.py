#!/usr/bin/env python
#
# This file is part of dik-dik (https://github.com/mbovo/dikdik).
# Copyright (c) 2020-2023 Manuel Bovo.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from ruamel.yaml import CommentedMap, CommentedSeq
from typing import Callable, Any
from re import Pattern
from . import operations
from loguru import logger

ExtractFunction = Callable[[Any, CommentedMap |
                            CommentedSeq, CommentedMap | CommentedSeq], None]
TransformerFunction = Callable[[str, Any, dict[str, Any]], Any]

def operation_to_transformer(all_operations: dict[Any, Any]=operations.DEFAULT_OPERATIONS, op_name_field: str = "op", op_params_field: str = "params") -> TransformerFunction:
  """
    Mapp the operation name to the operation function and return a TransformerFunction that apply the operation function.
  """
  def generic_transformer(key: str, value: Any, groups: dict[str, Any]) -> Any:
    logger.debug("", key=key, value=value, groups=groups)
    if op_name_field not in groups:
      return None
    if op_params_field not in groups:
      groups['params'] = []

    op = groups[op_name_field]
    params = groups[op_params_field].strip().split(' ')  # split the parameters

    if op in all_operations:
      # Call the specific operation function
      logger.debug("Operation", op=op, params=params, value=value, path=key)
      try:
        trans = all_operations[op](params=params, value=value, path=key)
        return trans
      except TypeError as e:
        raise e
      except operations.OperationVarUndefinedValue as e:
        raise e

  return generic_transformer

def extract_comment_regexp(regexp: Pattern[str], transform: TransformerFunction | None = None) -> ExtractFunction:
  """
  Return an ExtractFunction if a comment match a given regular expression pattern.
  Optionally Apply a set of transformations to the extracted items
  Args:
    regexp (Pattern[str]): The regular expression pattern used to match and extract information from comments.
    transform (TransformerFunction): A function that applies a transformation to the extracted items.
      Transform function signature must be `transform(key: str, value: Any, groups: dict[str,Any]) -> Any`

  Returns:
    ExtractFunction: A function that extracts information from a CommentedMap.
  """

  def extract(key: Any, src: CommentedMap | CommentedSeq, dest: CommentedSeq | CommentedMap) -> None:
      for comment_key, comments in src.ca.items.items():

          # Skip if key does not match
          if key != comment_key:
            continue

          # Skip if empty comments
          if comments is None or len(comments) < 3 or comments[2] is None:
            continue

          groups = {}

          # expand the regexp serching for the operation and parameters
          words = regexp.search(comments[2].value)
          if words is not None and len(words.groups()) > 1:
            # we have a match
            logger.debug("Matched", key=key, value=src[key], groups=words.groupdict())

            # extract the regexp groups as dictionary of groupName: match
            groups.update(words.groupdict())

            # apply the trasformation if any
            if transform is not None:
              ret = transform(key, src[key], groups)
              dest[key] = ret
              if ret is None:
                del dest[key]

  return extract


def deep_visit(src: CommentedMap | CommentedSeq, dest: CommentedMap | CommentedSeq, extract_fun: ExtractFunction) -> None:
  """
    Recursively visits a nested dictionary and apply the given extraction function to each element.

    Args:
      src (CommentedMap | CommentedSeq): The source dictionary to be visited.
      dest (CommentedMap | CommentedSeq): The destination dictionary to be populated, it must be a deep copy of the source.
      extract_fun (Callable): The extraction function to be applied to each element.
      The signature of the function must be `extract_fun(key: Any, src: CommentedMap|CommentedSeq, dest: CommentedMap|CommentedSeq) -> None`
  """

  if isinstance(src, list):
    for key in src:
      index = src.index(key)
      if isinstance(key, dict):
        deep_visit(key, dest[index], extract_fun)
      elif isinstance(key, list):
        deep_visit(key, dest[index], extract_fun)
      extract_fun(key, src, dest)

  if isinstance(src, dict):
    for key, value in src.items():
      if isinstance(src[key], dict):
        deep_visit(src[key], dest[key], extract_fun)
      elif isinstance(src[key], list):
        deep_visit(src[key], dest[key], extract_fun)
      extract_fun(key, src, dest)
