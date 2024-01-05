# yapl
An easy to configure program launcher that runs on your terminal.

# Installation
Put the `yapl.py` file somewhere and execute this script through keyboard shortcuts (ex: sxhkd). Or just run this script directly, it also works.

# Configuration
The configuration file looks something like this:

```json
{
  "PROGRAM_NAME": {
    "cmd": "/path/to/executable",
    "cwd": "/path/to/working/dir",
    "env_var": ["SOME=kuru", "VAR=kuru"],
  }

  ...
}
```

That should give you a rough idea on how to configure `yapl`. Configuration file is saved to `$HOME/.config/yapl/yapl.json`
