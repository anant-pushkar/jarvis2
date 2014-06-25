jarvis2
=======

Jarvis is a project management and unit testing framework. It can be customised to work on any kind of project in any language or set of languages. The testing logic can be written in any languages using filters on stdout, however, test suit needs to be written in python. The project management module, written in python allows you to add your own command line triggers and manage the project as you like. Jarvis gives a programmer the freedom he needs.

To install:
```bash
bash install.sh
```

Start by typing jarvis on the terminal (you may have to add sudo here). This will open the admin shell. Following commands can now be used:

```bash
create_project
```
Used to create project. Choose amongst various project types. By default only c, c++ and python projects are available, however, you may define your own custom project types (refer to wiki for more details)

```bash
open_project
```
Used to open a pre-existing project. Start by selecting the project type followed by the name. This will open the main files in the default editor(set in Documents/jarvis/config.json , gedit by default) and the project terminal where you may use the project specific commands.

The commands used in project terminal are as follows:

| Command       | Use                                                       | 
| ------------- |:---------------------------------------------------------:| 
| build         | Used to build project. Runs scripts from scripts/buildfile| 
| run           | Used to run. Runs scripts from scripts/runfile            | 
| test          | Used to run test suits form jarvis/testCases.py           | 

For more instructions, refer to wiki.
Contact the author at anantpushkar009@gmail.com
