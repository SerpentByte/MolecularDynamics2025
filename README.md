# MolecularDynamics2025
This repo contains information and materials related to the introductory course to molecular dynamics. The course was conducted between January-April of 2025.

## Getting started
### Requirements
- a laptop or a desktop
- linux OS (please see the **obtaining a _Linux Terminal_** section)

### Obtaining a *Linux Terminal*
#### Context
The terminal in linux is the most powerful feature of the linux (UNIX/GNU) based operating system. Although there is a learning curve, the whole computer can be controlled from a single black (or your colour of choice) screen. </br>
This includes file/folder creation and modifications, navigation into different folders (directories), creating or editing documents, compiling and running programs or even launching apps. </br>
Linux is free, open source and mostly lightweight. This means even very old laptops (lets say even from 2002) can smoothly run a Linux based OS. </br>
This is why Linux the OS of choice in the computational/theoretical science community. Subsequently all the programs developed were primarily focused on running or launching them from the terminal.</br>
We still follow the tradition since using the terminal is very efficient. Therefore everyone needs to obtain a terminal for this course. </br>
</br>
#### getting a terminal
If you already are on the Linux or Mac, you will by default have access to a terminal. If you do not know how to launch one, we will come to it during the lectures.</br>
Windows users need to perform either of the two things below to get an access to a terminal:
- **Linux installtion in a Virtual Machine**: one can create a pseudo-computer inside windows by the use of a software called a Virtual Machine (VM). There are many VMs present. But I will recommend to use [Virtual Box](https://www.virtualbox.org/) by Oracle. Running a VM inside Windows is quite heavy on the laptop. Therefore, unless your laptop is quite powerful, I would advise against this. Using linux inside a VM does not require internet, unless something needs to be downloaded. You would also need an ISO of a linux distribution to install in a newly created virutal machine. Please use [Lubuntu](https://lubuntu.org/) or [Xubuntu](https://xubuntu.org/) for the VM since they are very light. Please download the latest 64 bit (x64) LTS ISO for either of them.
- **SSH via MobaXterm**: Another way is to obtain access to a linux server and connect to it via SSH. [MobaXterm](https://mobaxterm.mobatek.net/) is a ssh client for windows. I recommend to download the installer version and not the portable version. But I leave this choice to you. Access to a Linux server will be provided and the IP address and the login credentials will be announded in the Google Classroom. But connection to the server can only be eshtablished if you are within the institute network. In case you are outside the institute netwrok, you would need to connect to the VPN before you can access the server. Therefor using MobaXterm will require a good internet connectivity.</br>

### Getting used to the Terminal
We shall decdicate a whole class for learning how to work with the terminal. The directory [linux_commands](https://github.com/SerpentByte/MolecularDynamics2025/tree/main/linux_commands) contains details on a few basic and most useful commands. We will require this everytime we use linux.

### Getting started with Python
We shall discuss basic molecular dynamics algorithms in detail during the lectures. However, if we do not implement them, a complete understanding of the algorithms cannot be achieved. Hence we shall also implement them using a programming language of choice. </br>
Most MD codes are written in Fortran of C/C++ due their very fast execution speeds and extreme optimization capabilities. But both of them are hard and simulations we shall perform will not be very complicated. Hence Python is the language of choice. Python is intuitive and easy to learn. It is also very easy to write codes in Python. However using Python is not mandatory. Please limit the programming languages to Python, Fortran, C/C++ or Julia. . Kindly do not use Java, Rust or TCL for this since they are not meant for scientific computing. 
</br></br>
We shall not use the system python for this and will rely on a python distribution called Ananconda3. Please download a stripped down version of Anaconda3 called [Miniconda3](https://repo.anaconda.com/miniconda/). Download the Mac or Linux version as needed. If you are using an ssh server, copy the download link and then into the terminal type ```wget <paste the link here>``` and press enter.
