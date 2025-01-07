<h2>Here is a list and descriptions of the most basic and highly used linux commands</h2>

One can check the documentation for advanced usage for each command by typing
```<command> -h``` in Linux terminal.

|**command** | **description**                                        |
|------------|--------------------------------------------------------|
| cd         | stands for **c**hange **d**irectory. It is used to navigate through the different files and folders/directories|
| mkdir      | stands for **m**a**k**e **dir**ectory. It is used to create a new directory |
| rm         | stands for **r**e**m**ove. It is used to remove a file. However directories would not be deleted by this |
| rm -r      | this is *recursively* (```-r```) delete all contents of a directory and then delete the directory too |
| cp         | stands for **c**o**p**y. Used to copy files from one location to another. However this will not copy directories. ```-r``` has to be used to copy directories|
| mv         | stands for **m**o**v**e. Used to move a file from one location to another. ```-r``` has to be used if a directory is being moved |


&nbsp;<br>
&nbsp;<br>

<h3> Syntax of the commands </h3>

*```-v``` flag stands for verbose. Using this flag will display messages that confirm that the command has properly executed.*<br>
*My personal opinion is to use this flag if the command supports.*

<h4> cd </h4>

```cd <direcotory name>```

<h4> mkdir </h4>

```mkdir <directory name>```<br>
```mkdir -pv <directory name>```<br>
(```-p``` will create parent directory and its sub-directories also)<br>
(```-v``` will show whether the directories have been created or not)<br>

<h4> rm </h4>

```rm <file name>```<br>
```rm -rv <directory name>```<br>

<h4>cp</h4>

```cp -v <source path> <target path>```<br>
```cp -rv <source directory> <target path>```<br>

<h4>mv</h4>

```mv -v <source path> <target path>```<br>
```mv -rv <source directory> <target path>```<br>

<h2>Wildcard characters</h2>
Wildcard characters are special characters that mean something specific in the linux command line.<br>
Two of the most important ones are * and ?.<br>
Here are a few links to learn what they are and how to use them.<br>
https://www.educba.com/linux-wildcards/<br>
https://www.iexpertify.com/linux/using-wildcards-in-linux/<br>
https://medium.com/techtofreedom/wildcards-on-linux-a-practical-guide-ed59795a4cc1<br>

