# Base16 Textual Style Builder

## About

This is a script which generates styles for the [Textual IRC client](http://www.codeux.com/textual/) based on the color schemes of [Base16](https://github.com/chriskempson/base16) by [chriskempson](https://github.com/chriskempson) and the default *Simplified* style bundled with Textual.

This repository is for someone who wants to customize the styles. If you just want to use the styles in their default configuration, you can use the ready-to-use styles at [base16-textual](https://github.com/FroZnShiva/base16-textual).
You can also see previews of the styles there.

The Git tags denote the last supported Textual version.

## Requirements

* Python 3
* [python-scss](https://github.com/pistolero/python-scss)
```sh
pip install sass
```

## Usage

Clone the repository and switch into it:
```sh
git clone https://github.com/FroZnShiva/base16-builder-textual
cd base16-builder-textual
```

Generate the styles by running:
```sh
./base16-textual
```
The styles are stored in the `output` directory by default.

If you want to install the files directly for Textual, you can ran **one** of the following commands depending if you have installed the application via the Mac App Store (MAS) or any other way:

```sh
./base16-textual --install     # For the non-MAS version
./base16-textual --install-mas # For the MAS version
```

See available configuration options by viewing the integrated help:
```sh
./base16-textual --help
```

### Grouping

By default joins, quits, parts, and nick changes will be grouped. Each group can be expanded or collapsed by clicking on the arrow.

![Feature: Grouping](https://github.com/FroZnShiva/base16-builder-textual/raw/master/feature-previews/grouping.png)

You can disable this feature by passing:

```sh
./base16-textual --disable-grouping
```

You can pass a comma-separated list of channels that are either included or excluded by the grouping feature, be passing one of the following options:

```sh
./base16-textual --grouping-exclude "#channel1,channel2"
# or
./base16-textual --grouping-include "#channel1,channel2"
```

