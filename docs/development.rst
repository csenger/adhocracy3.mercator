Development
===========

General Remarks
---------------

Use test driven development and check code style bevore pushing commits
(see `Coding Style Guideline` ).

Manually check pyflake, pep257::

    bin/check_code src/adhocracy src/adhocracy_sample

Example Vim config according to coding guideline::

    https://github.com/liqd/vim_config

When changing the api, the frontend needs to re-generate the
TypeScript modules providing the resource classes.  This may trigger
compiler errors that have to be resolved manually.  For more details,
see comment in the beginning of mkResources.ts.

Running the Testsuite
---------------------

frontend unit tests:

    A.  Integrated with py.test::

            bin/py.test ./src/adhocracy_frontend/adhocracy_frontend/tests/unit/

    B.  In browser::

            make -C ./parts/static/js/ compile_tests_browser
            xdg-open http://localhost:6551/static/test.html

        Make sure backend is running (or some means of delivering html
        and js to the browser).

        This is the best way to develop, as it lets you run tests
        indiviually and repeatedly and enter the debugger.

        .. note::

           In the debugger, it helps to disable the script tag about
           blanket in test.html.  You can do this thusly::

               make -C ./parts/static/js/ compile_tests_browser test-no-blanket
               xdg-open http://localhost:6551/static/test-no-blanket.html

    C.  With node.js::

            make -C ./parts/static/js/ compile_tests_node
            bin/jasmine-node ./parts/static/js/

        .. note::

           Node only works with the commonjs module system;
           whereas the frontend currently uses requirejs and the amd
           module system (rationale: requirejs is more powerful with
           importing module-system-oblivious libraries like angular,
           underscore, ...).  You know that you have run into this
           problem if this appears in your browser console::

               Uncaught Error: Module name "Adhocracy/UtilSpec" has not been loaded yet for context: _. Use require([])
               http://requirejs.org/docs/errors.html#notloaded

           In order for the javascript code to work in the browser, you
           need to revert to adm::

               make -C ./parts/static/js/ compile_tests_browser

frontend integration tests:

    Frontend integration tests behave like unit tests in the sense
    that they are driven by jasmine and can access all exports of all
    typescript modules; they behave like end-to-end tests in that they
    can talk to a running backend, angular runtime, etc..

    This makes it possible to write integration tests that reproduce
    any possible bug once it is reported (even though it may sometimes
    be better to write a unit or an acceptance test).

    For instance, one can write
    a test that registers and injects the AdhHttp service, renders
    some directive into the DOM, sends some keys to some input fields
    and clicks "save", and, once the object has been saved to the
    database, gets it from the backend and compares it to the one
    rendered in the directive.

    Integration tests do not support nodejs.  They can only be run in
    browser manually or via py.test.

    A.  Integrated with py.test::

            bin/py.test ./tests/integration/

    B.  In browser::

            make -C ./parts/static/js/ compile_tests_browser
            xdg-open http://localhost:6551/static/igtest.html

        .. note::

           As with the unit tests (see above), when running
           integration tests in the browser manually, you are
           responsible for making sure the backend is running.  In
           contrast to unit tests, debugging works smoothly without
           any tricks, because we don't run blanket for test coverage
           reporting.

frontend functional tests::

    bin/py.test ./src/adhocracy_frontend/adhocracy_frontend/tests/functional

protractor acceptance tests::

    bin/protractor etc/protractorConf.js

run backend functional tests::

    bin/py.test -m"functional" src/adhocracy_core/adhocracy_core/websocket src/adhocracy_core/docs

run backend unit tests and show python test code coverage::

    bin/py.test_run_unittests_with_coverage

run all tests (without protractor acceptance tests)::

    bin/py.test_run_all

delete database (works best on development systems without valuable data!)::

    rm -f ./var/Data.*
    bin/supervisorctl restart adhocracy:*

If you are using the `supervisor group adhocracy_test:*`, you don't have
to delete anything.  The database is in-memory and will die with the
test_zodb service.

Generate html documentation
---------------------------

Recreate api documentation source files::

    bin/sphinx_api_adhocracy

Generate html documentation::

    bin/sphinx_build_adhocracy

Open html documentation::

   xdg-open docs/build/html/index.html

Create scaffold for extension packages
---------------------------------------
::

    bin/pcreate -s adocracy_extension adhocracy_XX

Update packages
---------------

python
``````

Check whether new Python versions exist::

    bin/checkversions -v -l 0 versions.cfg | grep was

You may then update the pinned Python versions in `versions.cfg` if
appropriate.

ruby
````
::

    bin/gem outdated  # binary may also be called bin/gem1.9.1 or bin/gem2.1

node.js
```````
::

    bin/npm --prefix node_modules --depth 0 outdated

bower
`````

::

    cd .../lib  # where bower installs the libraries
    bower list

Adhocracy Releases
------------------

Adhocracy uses `semantic versions <http://semver.org/>`_ with one
extra rule:

    Versions 0.0.* are considered alpha and do not have to follow the
    major-minor-patch rules of semantic versioning.

Git tag and `setup.py`-version must be the same string.

In order to create a new version, first make sure that:

    1. you are on master.  (this rule is motivated by the fact that
       rebasing tags is really nothing we want to have to deal with.)

    2. the last commit contains everything you want to release and
       nothing else.

    3. you have git-pushed everything to origin.

Then, to upgrade to version 0.0.3, carry out the following steps:

    4. update `setup.py` to the new version (search for `name=...` and
       `version=...`).  Commit this change.

    5. `git tag -a 0.0.3 -m '...'`.  The commit comment can be
       literally `'...'` if there is nothing special to say about this
       release, or something like e.g. `Presentation <customer>
       <date>`.

    6. `git push --tags` (I think `git push` and `git fetch` treat
       tags and commits separately these days; for the convoluted
       details, consult the man pages).

Browse existing tags and check out a specific release::

    git tag
    git checkout 1.8.19

Apply a hotfix to an old release::

    git checkout -b 1.8.19-hotfix-remote-root-exploit 1.8.19
    ...  # (edit)
    git commit ...
    git tag -a 1.8.20 -m 'Fix: remote-root exploit'

There is more to tags, such as deleting and signing.  See `git tag
--help`.
