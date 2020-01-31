# Calculator With Integer Radix Converter

Advanced calculator plugin for [Wox](http://www.getwox.com/).
Uses fuctions from ```math``` module and ```scipy.special``` (if installed).

# Attention
This plugin is advanced version based on Python Calculator, used personally without uploading temporarily.

# Supported features:
- Multi radix result with integer result(*)
- Function docstring and autocomplete
- Auto-closing parentheses
- Thousands separator
- List formatting
- Input filtering
- Copy to clipboard after pressing Enter

***Protip***: use ```=``` sign to filter any unneccesary results:

```=2+2``` or ```2+2=```

## Installation
[Get Wox](http://www.getwox.com/)

To install the plugin, type in Wox:
```
wpm install Python Calculator
```

**You must replace relatives file with these project files, beacuse this project has not been uploaded into offical repository.**

Install ```scipy``` to enable advanced calculations:
```
pip install scipy
```

## Security
Plugin uses ```eval``` function which opens up a potential vector for injection attacks.

Be careful when entering untrusted input.
