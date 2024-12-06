import uuid
import random
import string
from typing import Any, Optional, Callable
import jinja2

class OperationError(Exception):

    """Baseclass for all Operation errors."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message)

    @property
    def message(self) -> Optional[str]:
        return self.args[0] if self.args else None


class OperationNotFound(OperationError):
   """Raised if an operation does not exist."""


class OperationVarUndefinedValue(OperationError):
    """Raised if the value in the template is undefined"""


def op_keep(**kwargs) -> Any:
  """
    Keep the value as is.
  """
  if 'value' in kwargs:
    return kwargs['value']
  raise OperationError("No value provided for keep() operation")


def op_remove(**kwargs) -> Any:
  """
    Remove the key entirely
  """
  return None


def op_random_uuid(**kwargs) -> Any:
  """
    Return a random UUID
  """
  return str(uuid.uuid1())


def op_random_pasword(**kwargs) -> Any:
    """
    Return a random password

    Args:
      params (list): The length of the password and the characters to use (optional)
    """

    if 'params' not in kwargs:
        raise OperationError(
            "Invalid number of parameters for random_password() operation, expected 1 got 0")

    params = kwargs['params']

    length = int(params[0]) if params[0].isdigit() else 32
    characters = string.ascii_letters + string.digits
    if len(params) > 1:
       characters = params[1]

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def op_env(**kwargs) -> Any:
  """
    Return an environment variable or a default value

    Args:
      params (list): The name of the environment variable
      value (str): The default value to return if the environment variable is not set
  """
  if 'params' not in kwargs:
    raise OperationError(
        "Invalid number of parameters for env() operation, expected 1 got 0")

  if 'value' not in kwargs:
    raise OperationError(
        "Invalid number of parameters for env() operation, expected 1 got 0")

  params = kwargs['params']
  value = kwargs['value']

  import os
  return os.getenv(params[0], value)


def op_value(**kwargs) -> Any:
  """
    Change the value with the one given in the parameters

    Args:
      params (list): The new value to set
  """
  if 'params' in kwargs:
    params = kwargs['params']
    if len(params) == 0:
      raise OperationError("No parameters provided for value() operation")
    elif len(params) == 1:
      return params[0]
    else:
      return ", ".join(params)
  raise OperationError

def generate_op_var(cfg: dict, root_key:str ='vars') -> Callable:
  """
    Configure the var() operation with passed configuration dictionary and an optional root key
  """

  def op_var(**kwargs) -> Any:
    """
      Return the value of a variable defined in the configuration

      Args:
        params (list): The name of the variable to return
    """
    if 'params' not in kwargs:
      raise OperationError(
          "Invalid number of parameters for var() operation, expected 1 got 0")

    params = kwargs['params']

    if len(params) != 1:
      raise OperationError(
          f"Invalid number of parameters for var() operation, expected 1 got {len(params)}")

    p = params[0]
    try:
      tpl = jinja2.Template(f"{{{{ {p} }}}}")
      if root_key not in cfg:
        raise OperationVarUndefinedValue(f"Variable {root_key} is not defined in the configuration dict")
      return tpl.render(cfg[root_key])
    except jinja2.exceptions.UndefinedError as e:
      raise OperationVarUndefinedValue(str(e))
    except KeyError as e:
      raise OperationVarUndefinedValue(str(e))
    except Exception as e:
      raise OperationError(str(e))

  return op_var


DEFAULT_OPERATIONS = {
    'keep': op_keep,
    'remove': op_remove,
    'random_uuid': op_random_uuid,
    'random_password': op_random_pasword,
    'env': op_env,
}