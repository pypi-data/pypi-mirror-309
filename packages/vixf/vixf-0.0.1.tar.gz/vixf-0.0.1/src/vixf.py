#!python3
"""
Allow editing X11 fields with terminal editor in $VISUAL.  Use keyboard
automation to select-all and copy text from the field, save it into a file,
edit that file with the terminal editor, and when the editor is done, read the
(presumably modified) text back from the file and paste it over the original
text.
"""

# stdlib imports
import argparse
import configparser
import locale
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

# Install these with pip or your system package manager; note that on
# GNU/Linux, pyperclip needs either xclip(1) or xsel(1) to be installed,
# preferably the former.  I wanted to do this in pure Python (and drop
# a dependency) without these forks, but haven't figured that out (yet).
import pynput
import pyperclip

# Name self for paths and error reporting
SELF = 'vixf'

# List of editors to try if not configured or set with environment variables;
# the first one that exists will be used, failing that, the last one will be
# used regardless
EDITOR_FALLBACKS = [
    'editor',
    'sensible-editor',
    'vi',
]

# Default grace period for refocus events
FOCUS_DELAY_DEFAULT = 0.1

# List of terminal emulators to try if not configured; the first one that
# exists will be used, failing that, the last one will be used regardless
TERMINAL_FALLBACKS = [
    'x-terminal-emulator',
    'sensible-terminal',
    'xterm',
]


def main(environ = None):
    """
    Just bundle everything into a main function.
    """
    # If we weren't passed a test environment, use the real one
    environ = os.environ

    # Handle specifying a different user configuration file with -c or
    # --config; /etc/vixf/config is always read
    parser = argparse.ArgumentParser(
        prog=SELF,
        description='Edit contents of text fields in a text editor',
    )
    parser.add_argument(
        '-c', '--config',
        help='path to user config file',
        default=os.path.expanduser(f'~/.config/{SELF}/config'),
    )
    args = parser.parse_args()

    # Read config; read /etc/vixf/config first, then ~/.vixf/config, if they
    # exist.  It's not an error if they don't.
    config = configparser.ConfigParser()
    config.read(
        [
            f'/etc/{SELF}/config',
            args.config,
        ],
        encoding=locale.getpreferredencoding(),
    )

    # Wait for refocus events to finish
    focus_delay(config)

    # Get a keyboard controller object so we can start simulating keypresses
    keyboard = pynput.keyboard.Controller()

    # CTRL-A: select all
    with keyboard.pressed(pynput.keyboard.Key.ctrl):
        keyboard.type('a')

    # CTRL-C: copy selected
    with keyboard.pressed(pynput.keyboard.Key.ctrl):
        keyboard.type('c')

    # Read clipboard
    content_before = pyperclip.paste()

    # Stop here (error condition) if there's nothing in the clipboard
    if len(content_before) == 0:
        print(
            f'{SELF}: Nothing to edit.  Did the selection work?',
            file=sys.stderr,
        )
        sys.exit(1)

    # Open a named temporary file for editing; it will stay open as long as
    # this block does, just closing it after the initial write won't delete it
    with tempfile.NamedTemporaryFile(
            mode='w',
            delete_on_close=False
    ) as tf:

        # Write the copied content into the file
        tf.write(content_before)
        tf.close()

        # Pick an editor and a terminal
        editor = select_editor(config, environ)
        terminal = select_terminal(config)

        # Build the command to run for the user to edit the content
        command = shlex.split(editor) + [tf.name]
        if terminal:
            command = shlex.split(terminal) + ['-e'] + command

        # Run the command; if it exits non-zero, raise an exception and stop
        subprocess.run(command, check=True)

        # Open the temporary file again, but just for reading this time; get
        # all the content out of it, presumably modified
        with open(
            tf.name,
            mode='r',
            encoding=locale.getpreferredencoding(),
        ) as tfr:
            content_after = tfr.read()

    # If any data in the file after edit, copy it to the clipboard
    if len(content_after):
        pyperclip.copy(content_after)
    else:
        print(
            f'{SELF}: Nothing to paste.  Did the edit work?',
            file=sys.stderr,
        )
        sys.exit(1)

    # Wait for refocus events to finish
    focus_delay(config)

    # CTRL-V: paste over selection
    with keyboard.pressed(pynput.keyboard.Key.ctrl):
        keyboard.type('v')


def focus_delay(config):
    """
    Wait for just a bit to let focus events in the window manager complete
    """
    seconds = config.getfloat('focus', 'delay', fallback=FOCUS_DELAY_DEFAULT)
    time.sleep(seconds)


def select_editor(config, environ):
    """
    Try very hard to pick a prefered and existent editor.  Try VISUAL first,
    then EDITOR, then rattle through some common paths, and just return "vi"
    and hope for the best otherwise.
    """
    editor = config.get('editor', 'command', fallback=None)
    if not editor:
        if 'VISUAL' in environ:
            editor = environ['VISUAL']
        elif 'EDITOR' in environ:
            editor = environ['EDITOR']
        else:
            for fallback in EDITOR_FALLBACKS:
                editor = fallback
                if shutil.which(editor):
                    break
    return editor


def select_terminal(config):
    """
    Try very hard to pick a prefered and existent terminal emulator, or return
    "None" if we're configured not to need one.  Last resort is "xterm".
    """
    if config.getboolean('terminal', 'required', fallback=True):
        terminal = None
        terminal = config.get('terminal', 'command', fallback=None)
        if not terminal:
            for fallback in TERMINAL_FALLBACKS:
                terminal = fallback
                if shutil.which(terminal):
                    break
    else:
        terminal = None
    return terminal


if __name__ == '__main__':
    main()
