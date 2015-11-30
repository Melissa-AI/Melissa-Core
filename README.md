## Melissa
Melissa is a <del>virtual</del> assistant for OS X and Linux systems. She currently uses Google speech-to-text engine, OS X's `say` command or Linux's `espeak` command along with some magical scripting which makes her alive, developed by a group of sorcerers.

### Installation
#### For OS X Systems
Clone the project using `git`. You can install git and other CLI developer tools by running the following commands:

```
xcode-select --install
git clone https://github.com/tanay1337/Melissa.git
cd Melissa
pip install -r requirements.txt
cp profile.yaml.default profile.yaml
```

Manually install `pywapi` with the help of instructions provided [here](https://code.google.com/p/python-weather-api/).

#### For Linux Systems
Install `git` and `espeak` using your distribution's package manager or build them from their binary files. Follow the same steps as OS X's installation system, starting from the second command.

### Configuration
Once you have successfully set up your development environment, open `profile.yaml` to customise the file and add details about yourself.

### Contributing

After forking `tanay1337/Melissa` and making the appropriate changes, open an issue and a pull request. After testing the issue/pull request, your request will be merged.

### Licence

[The MIT License (MIT)](https://github.com/tanay1337/Melissa/blob/master/LICENSE.md)
