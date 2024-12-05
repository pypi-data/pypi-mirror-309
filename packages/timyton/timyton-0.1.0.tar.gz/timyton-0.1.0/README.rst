=======
Timyton
=======

Timyton is a time tracker application for the console.

* Timyton uses `Tryton <https://www.tryton.org/>`_ as its backend.
  All your invoicing needs are then covered by your Tryton instance.

* Timyton is usable offline and will synchronize its data with your tryton
  server when it becomes available again.

* Timyton uses `Textual <https://textual.textualize.io/>`_ to create its user
  interface providing a nice and slick experience.


Installation & Usage
====================

We recommend you use `pipx <https://pypa.github.io/pipx/>`_ to install
``timyton``.

.. code-block:: bash

   $ pipx install timyton

Once this is one you can start timyton

.. code-block:: bash

   $ timyton

You will be greeted by the preference window in which you can input the server
address of your Tryton instance, the database on this instance and your user
name on this instance.

The next step is to register the application key by clicking on the *Register*
button. **On your Tryton instance**, you will have to log in ; then in your
preferences a new application key should have appeared in the *Applications*
tab, check that the key match the one from timyton and validate it.

You can now select the employee you will input the timesheet for and you should
be good to go.

Inspiration & Goals
===================

timyton is heavily inspired by `chronos <https://foss.heptapod.net/tryton/chronos>`_.

The goal of this project is to have yet another timesheet client for Tryton but
also to get a grasp of modern python features while working on small but real
project.
