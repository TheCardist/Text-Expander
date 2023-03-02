# Python Text-Expander

This is inspired by using Espanso which is a great Text Expander application but I wanted to create it using Python. 

I configure my 'triggers' and what that trigger is replaced by using the config.yaml file where I outline each time. I decided to use semi-colon for the basis of each trigger word and that's what the Python script is looking for before it begins recording keystrokes.

It's required that you use semi-colon to start the process of logging each keystroke and end with a space so it then reviews what you've typed to determine if it matches any of the triggers you've outlined in the config.yaml file.

When you type a trigger within that configuration file then it backspaces the trigger you typed and then addings the replacement text over top.
