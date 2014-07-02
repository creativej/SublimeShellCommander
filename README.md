# Sublime Shell Commander

A simple plugin for hooking up shell commands in Sublime.

__Features__:
- Auto call command on sublime event. E.g. on_post_save.
- Filename pattern matching rule for command line calls


### Dependency
- [SublimeREPL](https://github.com/wuub/SublimeREPL) sublime plugin

Shell Commander uses SublimeREPL in the background to running shell commands.


### Manual Install

1. Click the `Preferences > Browse Packages…` menu
2. Browse up a folder and then into the `Installed Packages/` folder
3. Download [zip package](https://github.com/creativej/SublimeShellCommander/archive/master.zip) rename it to `SublimeShellCommander.sublime-package` and copy it into the `Installed Packages/` directory
4. Restart Sublime Text

### How to use
In order to use Shell Commander you need to edit either the package user preference file or your project file e.g. project.sublime-project

You can access the Shell Commander's user preference file by:
Click the `Preferences > Package Settings > Shell Commander > Settings - User` menu


#### Setup basic custom command
```
{
    "commands": {
        "echo test": "echo Hello world!"
    }
}
```


#### Setup basic custom command to run in your project path
```
{
    "commands": {
        "project path": "cd {{project_path}}; pwd"
    }
}
```


__Available parameters:__
- project_path
- filename
- relative_filename
- file_path
- active_symbol (the word your cursor was on)


#### How to access the commands
Once the command is setup in the setting file, you can access it using the shortcut __"ctrl+shift+p"__:

![Sublime command menu](http://i.imgur.com/VERXK3V.png =200x)



You can also hook the command up with your key bindings:
```
// Default (OSX).sublime-keymap
[
    ...
    {
        "keys": ["ctrl+j"], "command": "shell_commander_run_predefined", "args": { "name": "echo test" }
    },
    ...
]
```




#### Run command on sublime events
The following examples runs "echo test" command on saving of any file

```
{
    "commands": {
        "echo test": "echo Hello world!"
    },
    "on_post_save": {
        "pattern": ".*", // e.g. "index\\.html"
        "command": "echo test"
    }
}
```

__Events:__
- on_post_save
- on_pre_save
- on_pre_close
- on_close
- on_activated
- on_new
