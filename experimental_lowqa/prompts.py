"""
A module implementing interfaces for prompting the user for input.
"""

# built-in
import asyncio
import functools
from typing import Dict, Iterable, NamedTuple, Optional

DEFAULT_PROMPT = "selection? "


def select_option(
    options: Iterable[str],
    prompt: str = DEFAULT_PROMPT,
    print_options: bool = False,
) -> Optional[int]:
    """
    Given a list of options, prompt user until they select a valid index and
    return it.
    """

    options = list(options)

    assert len(options) > 0
    if len(options) == 1:
        return 0

    if print_options:
        print("options:")
        for idx, option in enumerate(options):
            print(f"  {idx}: '{option}'")

    selection: int = -1
    while selection < 0 or selection >= len(options):
        try:
            value = input(prompt)
            selection = int(value)
        except ValueError:
            if value in options:
                selection = options.index(value)
        except KeyboardInterrupt:
            return None
    return selection


class SelectOpts(NamedTuple):
    """Manual select method options."""

    default: str = ""
    allow_prompt: bool = True
    custom_option: bool = False
    descriptions: Optional[Dict[str, str]] = None
    prompt: str = DEFAULT_PROMPT


def boolean_select(label: str, **kwargs) -> bool:
    """Provide a boolean select prompt."""
    return manual_select(label, ["y", "n"], **kwargs) == "y"


async def async_boolean_select(label: str, **kwargs) -> bool:
    """Provide a boolean select prompt."""
    return await async_manual_select(label, ["y", "n"], **kwargs) == "y"


async def async_manual_select(
    label: str, options: Iterable[str], **kwargs
) -> Optional[str]:
    """
    Prompt the user until an option from the provided set of options is chosen.
    """
    return await asyncio.get_running_loop().run_in_executor(
        None, functools.partial(manual_select, label, options, **kwargs)
    )


def manual_select(
    label: str, options: Iterable[str], **kwargs
) -> Optional[str]:
    """
    Prompt the user until an option from the provided set of options is chosen.
    """

    opts = SelectOpts(**kwargs)

    options = list(options)

    custom_idx = -1
    if opts.custom_option:
        options.append("<enter manually>")
        custom_idx = len(options) - 1

    if not options:
        print(f"no options for '{label}'!")
        return None

    # select the default if it was provided and valid, or if custom options are
    # enabled and a non-empty default was provided
    if opts.default and (
        (opts.default in options or not opts.allow_prompt)
        or opts.custom_option
    ):
        return opts.default

    print(f"options for '{label}':")
    for idx, option in enumerate(options):
        item_str = f"  {idx}: '{option}'"
        if opts.descriptions and option in opts.descriptions:
            item_str += f" ({opts.descriptions[option]})"
        print(item_str)

    selection = None

    if not opts.allow_prompt:
        print(f"not prompting and '{opts.default}' not in options")
    else:
        selection = select_option(options, prompt=opts.prompt)

    if selection is None or selection < 0:
        return None

    if selection == custom_idx:
        if not opts.allow_prompt:
            print("error: selected manual entry option but prompts disabled")
            return None
        return str(input("value: "))

    return options[selection]
