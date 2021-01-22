# REAPER ReaMenus

ReaMenus is a community menuset for Cockos' digital audio workstation REAPER.

## Introduction

The [original ReaMenus](https://github.com/mikestopcontinues/reamenus) was created and updated by [mikestopcontinues](https://github.com/mikestopcontinues) until v5.31, then maintained by [Pet](http://forum.cockos.com/member.php?u=103730) as mentioned in the related [REAPER forum thread](http://forum.cockos.com/showthread.php?t=58672).
However the development has been stalled, with the last version being 5.40 updated in 2017.

This repository aims to provide a more maintainable version of ReaMenus, to lower the technical barrier in writing menu items as an invitation for community contribution, and to remove some excuses for procrastination when attempting to update ReaMenu.

Compare the syntax for reaper-menu.ini in REAPER:

``` ini
item_7=-2 &Templates
item_8=46000 &Open template...
item_9=40392 &Save tracks as track template...
item_10=_S&M_SHOW_RESVIEW_TR_TEMPLATES &Track templates...
item_11=-1
item_12=46001 &(track template list)
item_13=-3
item_14=-1
item_15=-4 EDITING
```

with how it's written in this repository:

``` ini
> &Templates
    46000 &Open template...
    40392 &Save tracks as track template...
    _S&M_SHOW_RESVIEW_TR_TEMPLATES &Track templates...
    ---
    46001 &(track template list)
---
## EDITING
```

This markdown-like syntax has a more friendly appearance to maintainers, with headers, submenus, and separators clearly demonstrated.
The syntax also allows importation from mixin files, incrementation, and localization.

## How to build

A python module is used for parsing the source files, in the `/src` folder and combining them into a release file, in the `/release` folder.

To build, use the following command:

`python -m reamenus`

## Syntax

All syntaxes need to be written at the beginning of a line, with only spaced indentation allowed before them.
A space must be included to separate the syntax from the content that follows.

### Section Name

Section names are taken from the file name, thus `[Main file]` section should correspond to the file `Main file.txt`.

However, because some characters cannot be included in the file name, the following syntax is used to rename the section.

`! Section name`

Which renames a section to `[Section name]`.

This syntax is currently only used for `[Ruler/arrange context]`, since the character `/` is not allowed in the filename.

### Title

Menu sections in the `.ini` file can be renamed with the `title=` prefix, which changes the displayed name of the menu in REAPER.

This prefix is shorted to a single sharp, `#`, so `# File` will be converted to `title=File`.

### Header

Headers, a grayed out menu item that links to no action, is indicated with two sharps `##`, e.g. `## Edit` will be converted to `-4 Edit`.

### Separator

Just like markdown, separator is written as `---`, which translates to `-1`.

### Submenu

Submenus are a bit more complicated.

As shown in the example from [introduction](#introduction), use `>` to indicate the header of the submenu, and apply indentation of 4 spaces to the following lines to place them in the submenu.
The first line with at least one level less indentation marks the end of the submenu.
All other syntaxes can be use within a submenu with indentation placed before the syntax.
Also, multiple layers of submenus are possible.

As an example:

``` markdown
## Header
> Submenu
    submenu item 1
    submenu item 2
    ---
    ## Header
    > Subsubmenu
        subsubmenu item
    ---
    submenu item 3
---
normal item
```

### Importation

To avoid writing the same contents in multiple files, and to simply maintenance workload, repeated lines may be extracted into an unique file, leaving only a link to the file. Upon building, the content of the target file will be copied to the location of the syntax.

Inspired by sass, the syntax for importation is `@import filename`.
The search location for the filename is `/src/.../mixins`.

### Incrementation

Sometimes items may repeat many times with only difference in numerals - incremental channel numbers for example, a syntax is available to generate the list from a single line.

`++ REPS Content {{1|STEPSIZE}}`

Explained below.

The line starts with two plus signs, after necessary indentations, then a number indicating how many repetitions to be generated, everything after is the actual content of the line.

Within the content of the line, wrap the incrementing number, or multiple numbers, with double curled brackets.
The result will start from the written number, and start incrementing from the first repetition.

The repeating number can be padded with 0, thus `{{01}}` will become `01`, `02`, `03` and etc.

An optional step size argument can be added by adding a `|` after the initial number.
This will increase the initial number by the indicated step size, or decrease if the step size is a negative number.

### Localization

We can support multiple languages by categorizing contents in language folders.
The original English ReaMenus should reside in `src/en/`, which builds into `ReaMenus.en.ReaperMenuset`.
By the same logic, French localization should be placed into `src/fr/`, or whatever other language code string that is used.
