# Copyright 2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""###Module fp.functional - compose and partially apply functions.

Not a replacement for the std library's `functools` which is more about
modifying function behavior through decorators than functional composition
and application.

#### FP utilities to manipulate function arguments return values:

* function **swap:** swap the arguments of a 2 argument function
* function **sequenced:** convert function to take a sequence of its arguments
* function **partial:** returns a partially applied function

"""
from __future__ import annotations
from collections.abc import Callable, Sequence
from typing import Any

__all__ = [ 'swap', 'sequenced', 'partial' ]

## Functional Utilities

def swap[U,V,R](f: Callable[[U,V],R]) -> Callable[[V,U],R]:
    """Swap arguments of a two argument function."""
    return (lambda v,u: f(u,v))

def sequenced[R](f: Callable[..., R]) -> Callable[..., R]:
    """Convert a function with arbitrary positional arguments to one taking
    a sequence of the original arguments.
    """
    def F(arguments: Sequence[Any]) -> R:
        return f(*arguments)
    return F

def partial[R](f: Callable[..., R], *args: Any) -> Callable[..., R]:
    """Partially apply arguments to a function, left to right.

    * type-wise the only thing guaranteed is the return value
    * best practice is to either
      * use `partial` and `sequenced` results immediately and locally
      * otherwise cast the results when they are created

    """
    def apply(fn_seq: Callable[..., R], vals: Sequence[Any]) -> Callable[..., R]:
        return (lambda restT: fn_seq(vals + restT))

    def wrap(*bs: Any) -> R:
        return apply(sequenced(f), args)(bs)

    return wrap

