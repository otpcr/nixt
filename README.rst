N I X T
=======


NAME


``nixt`` - NIXT


SYNOPSIS


``nixtctl <cmd> [key=val] [key==val]``


DESCRIPTION


NIXT has all the python3 code to program a unix cli program, such as
disk perisistence for configuration files, event handler to
handle the client/server connection, code to introspect modules
for commands, deferred exception handling to not crash on an
error, a parser to parse commandline options and values, etc.

NIXT uses object programming (OP) that allows for easy json save//load
to/from disk of objects. It provides an "clean namespace" Object class
that only has dunder methods, so the namespace is not cluttered with
method names. This makes storing and reading to/from json possible.

NIXT is Public Domain.


INSTALL


$ ``pipx install nixt``
$ ``pipx ensurepath``

<new terminal>

$ ``nixtctl srv > nixt.service``
$ ``sudo mv *.service /etc/systemd/system/``
$ ``sudo systemctl enable nixt --now``

joins #nixt on localhost


USAGE


without any argument the bot does nothing::

$ ``nixtctl``
$

see list of commands

$ ``nixtctl cmd``
cfg,cmd,dne,dpl,err,exp,fnd,imp,log,mod,mre,nme,pwd
rem,res,rss,srv,syn,tdo,thr,upt

start daemon

$ ``nixtd``
$

start service

$ ``nixts``
<runs until ctrl-c>


CONFIGURATION

::

    irc

    $ nixtctl cfg server=<server>
    $ nixtctl cfg channel=<channel>
    $ nixtctl cfg nick=<nick>

    sasl

    $ nixtctl pwd <nsvnick> <nspass>
    $ nixtctl cfg password=<frompwd>

    rss

    $ nixtctl rss <url>
    $ nixtctl dpl <url> <item1,item2>
    $ nixtctl rem <url>
    $ nixtctl nme <url> <name>


COMMANDS

::

    cmd - commands
    err - show errors
    log - log text
    mod - modules
    thr - show running threads
    upt - show uptime


**CODE**

::

    >>> from nixt.object import Object, dumps, loads
    >>> o = Object()
    >>> o.a = "b"
    >>> print(loads(dumps(o)))
    {'a': 'b'}


FILES

::

    ~/.nixt
    ~/.local/bin/nixt
    ~/.local/bin/nixtctl
    ~/.local/bin/nixtd
    ~/.local/bin/nixts
    ~/.local/pipx/venvs/nixt/*


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    NIXT is Public Domain.
