N I X T
=======


**NAME**


``nixt`` - NIXT 


**SYNOPSIS**


|
| ``nixt <cmd> [key=val] [key==val]``
| ``nixt -cviw``
| ``nixt -d`` 
| ``nixt -s``
|

**DESCRIPTION**


``nixt`` has all you need to program a unix cli program, such as disk
perisistence for configuration files, event handler to handle the
client/server connection, deferred exception handling to not crash
on an error, etc.

``nixt`` contains all the python3 code to program objects in a functional
way. It provides a base Object class that has only dunder methods, all
methods are factored out into functions with the objects as the first
argument. It is called Object Programming (OP), OOP without the
oriented.

``nixt`` allows for easy json save//load to/from disk of objects. It
provides an "clean namespace" Object class that only has dunder
methods, so the namespace is not cluttered with method names. This
makes storing and reading to/from json possible.

``nixt`` is a demo bot, it can connect to IRC, fetch and display RSS
feeds, take todo notes, keep a shopping list and log text. You can
also copy/paste the service file and run it under systemd for 24/7
presence in a IRC channel.

``nixt`` is Public Domain.


**INSTALL**


installation is done with pipx

|
| ``$ pipx install nixt``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ nixt srv > nixt.service``
| ``$ sudo mv nixt.service /etc/systemd/system/``
| ``$ sudo systemctl enable nixt --now``
|
| joins ``#nixt`` on localhost
|

if you run nixt locally from source you might need to add your
current directory to sys.path

|
| ``export PYTHONPATH="."``
|

**USAGE**

use ``nixt`` to control the program, default it does nothing

|
| ``$ nixt``
| ``$``
|

see list of commands

|
| ``$ nixt cmd``
| ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
| ``pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``
|

start daemon

|
| ``$ nixt -d``
| ``$``
|

start service

|
| ``$ nixt -s``
| ``<runs until ctrl-c>``
|


**COMMANDS**


here is a list of available commands

|
| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``err`` - show errors
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``log`` - log text
| ``mre`` - display cached output
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``req`` - reconsider
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``tdo`` - add todo item
| ``thr`` - show running threads
| ``upt`` - show uptime
|

**CONFIGURATION**


irc

|
| ``$ nixt cfg server=<server>``
| ``$ nixt cfg channel=<channel>``
| ``$ nixt cfg nick=<nick>``
|

sasl

|
| ``$ nixt pwd <nsvnick> <nspass>``
| ``$ nixt cfg password=<frompwd>``
|

rss

|
| ``$ nixt rss <url>``
| ``$ nixt dpl <url> <item1,item2>``
| ``$ nixt rem <url>``
| ``$ nixt nme <url> <name>``
|

opml

|
| ``$ nixt exp``
| ``$ nixt imp <filename>``
|


**PROGRAMMING**


``nixt`` runs it's modules in the package, to add your own command  edit
a file in nixt/modules/hello.py and add the following for ``hello world``

::

    def hello(event):
        event.reply("hello world !!")


save this and run

|
| ``$ bin/nixt tbl > nixt/lookups.py``
| ``$ pipx install . --force``
|

program can execute the ``hello`` command now.

|
| ``$ nixt hello``
| ``hello world !!``
|

commands run in their own thread, errors are deferred to not have loops
blocking/breaking on exception and can contain your own written python3
code, see the nixt/modules directory for examples.


**FILES**

|
| ``~/.nixt``
| ``~/.local/bin/nixt``
| ``~/.local/pipx/venvs/nixt/*``
|

**AUTHOR**

|
| ``Bart Thate`` <``bthate@dds.nl``>
|

**COPYRIGHT**

|
| ``nixt`` is Public Domain.
|