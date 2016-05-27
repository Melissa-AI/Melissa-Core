## Melissa
[![Join the chat at https://gitter.im/Melissa-AI/Melissa-Core](https://badges.gitter.im/Melissa-AI/Melissa-Core.svg)](https://gitter.im/Melissa-AI/Melissa-Core?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Melissa is a <del>virtual</del> assistant for OS X, Windows and Linux systems. She currently uses either Google's speech-to-text engine or CMU's Sphinx, OS X's `say` command or Linux's `espeak` command along with some magical scripting which makes her alive, developed by [Tanay Pant](http://tanaypant.com) and a group of sorcerers.

### Installation
#### For OS X Systems
Clone the project using `git`. You can install git and other CLI developer tools by running the following commands:

```
xcode-select --install
```

You will need to install [PortAudio](http://www.portaudio.com/download.html), [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/) and [Python Weather API](https://code.google.com/archive/p/python-weather-api/). Now run the following commands:

```
git clone https://github.com/Melissa-AI/Melissa-Core.git
cd Melissa-Core
pip install -r requirements.txt
cp profile.yaml.default profile.yaml
cp memory.db.default memory.db
```

Melissa is currently configured to use Google STT by default in the `profile.yml` file. To use the offline CMU Sphinx STT, open the `profile.yml` file to insert `sphinx` instead of `google`. You will also have to install the Sphinx Base and Pocket Sphinx as well as add the appropriate language models by following the instructions given [here](https://wolfpaulus.com/journal/embedded/raspberrypi2-sr/).

If you have blink(1), you will have to install its commandline tool by following the instructions on [this](http://blink1.thingm.com/blink1-tool/) page.

#### For Linux Systems
Install `git` and `espeak` using your distribution's package manager or build them from their binary files. Follow the same steps as OS X's installation system, starting from installing PortAudio and PyAudio. To play music, you will have to install [mpg123](http://www.mpg123.de) and/or [sox](http://sox.sourceforge.net/).

#### For Windows
Follow the same installation steps as Linux, but take care to add the appropriate environment variables to the path. Melissa may prove to be more troublesome to install for Windows users.

### Configuration
Once you have successfully set up your development environment, open `profile.yaml` to customise the file and add details about yourself.

### Usage Guide
Follow [this](https://github.com/Melissa-AI/Melissa-Core/blob/master/USAGE.md) link for reading the Usage aka Dating Guide.

### Contributing

After forking `Melissa-AI/Melissa-Core` and making the appropriate changes, open an issue and a pull request. After testing the issue/pull request, your request will be merged.

### Licence

[The MIT License (MIT)](https://github.com/Melissa-AI/Melissa-Core/blob/master/LICENSE.md)
