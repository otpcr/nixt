N I X T
=======


**NAME**

::

   NIXT - You have been nixt.


**SYNOPSIS**

::

    nixt  <cmd> [key=val] [key==val]
    nixtc [-i] [-v]
    nixtd
    nixts


**DESCRIPTION**

::

    N I X T


**INSTALL**


installation is done with pipx

::

    $ pipx install nixt
    $ pipx ensurepath


**USAGE**


without any argument the bot does nothing

::

    $ nixt
    $

see list of commands

::

    $ nixt cmd
    cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,
    pwd,rem,req,res,rss,srv,syn,tdo,thr,upt


start a console

::

    $ nixtc
    >


use -v to enable verbose

::

    $ nixtc -v
    NIXT since Tue Sep 17 04:10:08 2024
    > 


use -i to init modules

::

    $ nixtc -i
    >



start daemon

::

    $ nixtd
    $


start service

::

   $ nixts
   <runs until ctrl-c>


**CONFIGURATION**


*irc*

::

    $ nixt cfg server=<server>
    $ nixt cfg channel=<channel>
    $ nixt cfg nick=<nick>

*sasl*

::

    $ nixt pwd <nsvnick> <nspass>
    $ nixt cfg password=<frompwd>4

*rss*

::
 
    $ nixt rss <url>
    $ nixt dpl <url> <item1,item2>
    $ nixt rem <url>
    $ nixt nme <url> <name>

*opml*

::

    $ nixt exp
    $ nixt imp <filename>


**SYSTEMD**

::

    $ nixt srv > nixt.service
    $ sudo mv nixt.service /etc/systemd/system/
    $ sudo systemctl enable nixt --now

    joins #nixt on localhost


**COMMANDS**

::

    here is a list of available commands

    cfg - irc configuration
    cmd - commands
    dpl - sets display items
    err - show errors
    exp - export opml (stdout)
    imp - import opml
    log - log text
    mre - display cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    res - restore deleted feeds
    rss - add a feed
    srv - create service file
    syn - sync rss feeds
    tdo - add todo item
    thr - show running threads


**SOURCE**

::

    source is at ``https://github.com/otpcr/nixt``


**FILES**

::

    ~/.nixt
    ~/.local/bin/nixt   (cli)
    ~/.local/bin/nixtc  (console)
    ~/.local/bin/nixtd  (daemon)
    ~/.local/bin/nixts  (service)
    ~/.local/pipx/venvs/nixt/*


**AUTHOR**

::

    Bart Thate <record11719@gmail.com>


**COPYRIGHT**

::

    NIXT is Public Domain.
