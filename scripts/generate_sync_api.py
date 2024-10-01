#!/usr/bin/env python
# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import re
import sys
from types import FunctionType
from typing import Any

from documentation_provider import DocumentationProvider
from generate_api import (
    api_globals,
    arguments,
    generated_types,
    get_type_hints,
    header,
    process_type,
    return_type,
    return_value,
    short_name,
    signature,
)

documentation_provider = DocumentationProvider(False)


def generate(t: Any) -> None:
    print("")
    class_name = short_name(t)
    base_class = t.__bases__[0].__name__
    if class_name in ["Page", "BrowserContext", "Browser"]:
        base_sync_class = "SyncContextManager"
    elif base_class in ["ChannelOwner", "object", "AssertionsBase"]:
        base_sync_class = "SyncBase"
    else:
        base_sync_class = base_class
    print(f"class {class_name}({base_sync_class}):")
    print("")
    documentation_provider.print_events(class_name)
    for [name, type] in get_type_hints(t, api_globals).items():
        print("")
        print("    @property")
        print(f"    def {name}(self) -> {process_type(type)}:")
        documentation_provider.print_entry(class_name, name, {"return": type}, True)
        [prefix, suffix] = return_value(type)
        prefix = "        return " + prefix + f"self._impl_obj.{name}"
        print(f"{prefix}{suffix}")
    for [name, value] in t.__dict__.items():
        if name.startswith("_"):
            continue
        if str(value).startswith("<property"):
            value = value.fget
            print("")
            print("    @property")
            print(
                f"    def {name}({signature(value, len(name) + 9)}) -> {return_type(value)}:"
            )
            documentation_provider.print_entry(
                class_name, name, get_type_hints(value, api_globals), True
            )
            [prefix, suffix] = return_value(
                get_type_hints(value, api_globals)["return"]
            )
            prefix = "        return " + prefix + f"self._impl_obj.{name}"
            print(f"{prefix}{arguments(value, len(prefix))}{suffix}")
    for [name, value] in t.__dict__.items():
        if isinstance(value, FunctionType) and "remove_listener" != name:
            # List of dunder methods to allow without docs
            allow_without_docs_methods = [
                "__getitem__",
            ]
            if name.startswith("_") and name not in allow_without_docs_methods:
                continue
            is_async = inspect.iscoroutinefunction(value)
            return_type_value = return_type(value)
            return_type_value = re.sub(r"\"([^\"]+)Impl\"", r"\1", return_type_value)
            print("")
            print(
                f"    def {name}({signature(value, len(name) + 9)}) -> {return_type_value}:"
            )
            # Allow dunder methods without docs
            if name not in allow_without_docs_methods:
                documentation_provider.print_entry(
                    class_name, name, get_type_hints(value, api_globals)
                )
            if class_name in [
                "LocatorAssertions",
                "PageAssertions",
                "APIResponseAssertions",
            ]:
                print("        __tracebackhide__ = True")
            if "expect_" in name:
                print(
                    f"        return EventContextManager(self, self._impl_obj.{name}({arguments(value, 12)}).future)"
                )
            else:
                [prefix, suffix] = return_value(
                    get_type_hints(value, api_globals)["return"]
                )
                if is_async:
                    prefix += f"self._sync(self._impl_obj.{name}("
                    suffix = "))" + suffix
                else:
                    prefix += f"self._impl_obj.{name}("
                    suffix = ")" + suffix

                print(
                    f"""
        return {prefix}{arguments(value, len(prefix))}{suffix}"""
                )
    print("")
    print(f"mapping.register({class_name}Impl, {class_name})")


def main() -> None:
    assert sys.version_info >= (3, 9)

    print(header)
    print(
        "from playwright._impl._sync_base import EventContextManager, SyncBase, SyncContextManager, mapping"
    )

    for t in generated_types:
        generate(t)
    documentation_provider.print_remainder()


if __name__ == "__main__":  # pragma: no cover
    main()
