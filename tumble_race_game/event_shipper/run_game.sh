#!/bin/bash
## You must have exported credentials with write access to the configured kinesis stream.


color_override=$1

if [ -n "$color_override" ]; then
    echo "Overriding color to $color_override"
    export COLOR_OVERRIDE=$color_override
fi

python main.py
