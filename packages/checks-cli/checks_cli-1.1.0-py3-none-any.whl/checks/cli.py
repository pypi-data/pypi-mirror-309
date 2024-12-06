""" Core CLI loop, parsing commands and routing """

import sys
from argparse import ArgumentParser
from checks.parser import Parser
from checks.exceptions import ParseError
from checks.utils import pins, err
from checks.commands import (
    add,
    check,
    check_all,
    uncheck,
    uncheck_all,
    remove,
    list_tasks,
    search,
    remove_all,
    save,
    clear
)


PROGRAM = "checks"
VERSION = "1.1.0"


def main():
    """ The Interactive CLI Session """
    # Parse command-line args/flags
    args = get_args()

    if args.version:
        # Print checks version and exit
        print("%s %s" % (PROGRAM.title(), VERSION))
        sys.exit(0)

    if args.nocolor:
        pins.disable_colors()

    print_startup_info()

    PROMPT = pins.colorize("@checks/> ", "sea_green", attrs=['italic'])

    try:
        while True:
            command = input(PROMPT).strip()
            # Empty?
            if not command:
                continue

            # Parse and process the command
            process_command(command)

    except (KeyboardInterrupt, EOFError):
        print("Force quit.")
        sys.exit(0)


def get_args():
    """ Parse and return command-line args """
    arg_parser = ArgumentParser(prog=PROGRAM,
                                usage="%s [OPTIONS]" % PROGRAM,
                                description="Command-line tool to manage tasks list.")

    arg_parser.add_argument("-v", "--version", action="store_true",
                            help="print the checks version number and exit")
    arg_parser.add_argument("-nc", "--nocolor", action="store_true",
                            help="run checks without color support")

    return arg_parser.parse_args()


def process_command(command: str):
    """ Process command using `Parser` class """
    # Parse the command
    try:
        tokens = Parser.parse(command)
    except ParseError as e:
        print("Parse error: %s" % e)
        return

    match tokens['action']:
        case "help" | "h":
            print_help()

        case "add" | "a":
            add(tokens['args'])

        case "check" | "c":
            flags = tokens['flags']
            if "-a" in flags or "--all" in flags:
                check_all()
                return

            check(tokens['args'])

        case "uncheck" | "uc":
            flags = tokens['flags']
            if "-a" in flags or "--all" in flags:
                uncheck_all()
                return

            uncheck(tokens['args'])

        case "remove" | "rm":
            flags = tokens['flags']
            if "-a" in flags or "--all" in flags:
                agree = pins.input_question("Remove all tasks? (y/N): ",
                                            prompt_color="light_red")
                if agree:
                    remove_all()
                return

            remove(tokens['args'])

        case "list" | "ls":
            flags = tokens['flags']
            minimal = "-m" in flags or "--minimal" in flags
            completed = "-c" in flags or "--completed" in flags
            pending = "-p" in flags or "--pending" in flags

            list_tasks(completed=completed, pending=pending, minimal=minimal)

        case "search" | "s":
            search(tokens['args'][0])

        case "clear" | "cls":
            clear()

        case "save" | "sv":
            save()

        case "quit" | "q":
            sys.exit(0)

        case _:
            err("CLI Error", "command '%s' is recognized by the parser but not by CLI." %
                tokens["action"])


def print_startup_info():
    """ Print the startup help text. """
    print("%s %s" % (PROGRAM.title(), VERSION))
    print("Type '%s' for usage hint. (%s to force quit)\n" % (pins.colorize("help", fgcolor="plum"),
                                                              pins.colorize("CTRL+C", fgcolor="light_red")))


def print_help():
    """ Print help text """
    help_table = {
        "add,     a": "add tasks",
        "check,   c": "mark tasks as complete",
        "uncheck, uc": "mark tasks as incomplete",
        "remove,  rm": "remove tasks",
        "list,    ls": "list all tasks",
        "search,  s": "search tasks",
        "clear,   cls": "clear terminal",
        "save,    sv": "save all tasks",
        "quit,    q": "exit the application",
        "help,    h": "print this help text",
    }

    print(pins.create_table(help_table, indent_values=4,
                            keys_fg="plum", values_attrs=['italic']))
    print()
