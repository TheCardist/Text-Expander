# Python Text-Expander

This is inspired by using **Espanso** which is a great Text Expander application but it does not work appropriately if you use applications like **Mouse without Borders**.

Due to this, I opted to create my own solution using Python. While not the most fleshed out solution in terms of features it does get the job done.

## Setup
I configure my 'triggers' and the replacement of that trigger by using the config.yaml file where I outline each trigger I want to use. I decided to use a semi-colon for the basis of each trigger word and that's what the Python script is looking for before it begins watching keystrokes.
It's required that you use semi-colon to start the process of logging each keystroke and end with a space so it then reviews what you've typed to determine if it matches any of the triggers you've outlined in the config.yaml file.

## Functionality
When you type a trigger within that configuration file it backspaces the trigger you typed and then adds the replacement text over top. 
E.g. if I setup a trigger for ```:hw```, the program will look for the semi-colon and if what I type afterwards matches this trigger then it would backspace the trigger and type ```hello world```.
