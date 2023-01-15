Overview
========

**didjvu** uses the Gamera_ framework to separate foreground/background
layers, which can be then encoded into a DjVu_ file.

.. _Gamera:
   https://gamera.informatik.hsnr.de/
.. _DjVu:
   http://djvu.org/

Prerequisites
=============

The following software is required:

* Python_ 3 (≥ 3.6)
* Gamera-4_ (≥ 4.0) (not available on PyPI)
* Pillow_
* DjVuLibre_ (≥ 3.5.22)
* minidjvu_ (≥ 0.8) for the ``--pages-per-dict``/``-p`` option

Additionally, one of the following libraries is needed for the ``--xmp``
option:

* GExiv2_ (≥ 0.12.2) + PyGI_ or
* python-xmp-toolkit_ or
* py3exiv2_

.. _Python:
   https://www.python.org/
.. _Pillow:
   https://pypi.org/project/Pillow/
.. _DjVuLibre:
   https://djvu.sourceforge.net/
.. _minidjvu:
   https://minidjvu.sourceforge.net/
.. _GExiv2:
   https://wiki.gnome.org/Projects/gexiv2
.. _PyGI:
   https://wiki.gnome.org/Projects/PyGObject
.. _python-xmp-toolkit:
   https://github.com/python-xmp-toolkit/python-xmp-toolkit
.. _py3exiv2:
   https://launchpad.net/py3exiv2
.. _Gamera-4:
   https://github.com/hsnr-gamera/gamera-4

Installation
============

You can use didjvu without installing it, straight out of unpacked source tarball or a VCS checkout.

It's also possible to install it system-wide with::

   pip install .

The man pages can be deployed using::

   make install_manpage

By default, ``make install_manpage`` installs them to ``/usr/local/``. You can specify a different installation prefix by setting the ``PREFIX`` variable, e.g.::

   make install PREFIX="$HOME/.local"
   
About this fork
===============

This repository is a port of the original repository to Python 3.

The process involved the *2to3* tool and manual fixes afterwards to get the existing tests to pass. Some of the error reports and fixes arising from the early porting process have been contributed by `@rmast`_.

At the moment there are no plans to submit a pull request to the upstream repository, which would probably require some changes to my code as well. This is mostly due to the corresponding upstream issue being marked as *wontfix*: `Issue #13`_.

I will try to keep this fork/port in sync with the upstream changes where necessary. Please note that I do not have any plans on implementing completely new features for now. Feature requests and bugs which can be reproduced in the original version as well should be reported at both places in the best case.

Differences from upstream
-------------------------

* Package requires Python ≥ 3.6.
* Drop old Gamera workarounds.
* Migrate from *nose* to plain *unittest* stdlib module.
* Conform to PEP8 coding style.
* Use standardized *setup.py*-based installation.
* Rename *lib* to *didjvu* and migrate *didjvu* binary to *__main__.py* and console script version.


.. _@rmast:
   https://github.com/rmast
.. _Issue #13:
   https://github.com/jwilk/didjvu/issues/13

.. vim:ft=rst ts=3 sts=3 sw=3 et tw=72
