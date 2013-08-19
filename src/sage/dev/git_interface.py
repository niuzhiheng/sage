- David Roe, Julian Rueth, Keshav Kini, Nicolas M. Thiery, Robert Bradshaw:
  initial version
#       Copyright (C) 2013 David Roe <roed.math@gmail.com>
#                          Julian Rueth <julian.rueth@fsfe.org>
#                          Keshav Kini <keshav.kini@gmail.com>
#                          Nicolas M. Thiery <Nicolas.Thiery@u-psud.fr>
#                          Robert Bradshaw <robertwb@gmail.com>
from sage.env import SAGE_DOT_GIT, SAGE_REPO_AUTHENTICATED, SAGE_SRC
from git_error import GitError, DetachedHeadError
        sage: from sage.dev.config import Config
        sage: from sage.dev.user_interface import UserInterface
        sage: config = Config()
        sage: GitInterface(config, UserInterface(config))
        GitInterface()
            sage: from sage.dev.config import Config
            sage: from sage.dev.user_interface import UserInterface
            sage: config = Config()
            sage: type(GitInterface(config, UserInterface(config)))
            <class 'sage.dev.git_interface.GitInterface'>
        self._src = self._config.get('src', SAGE_SRC)
        self.__user_email_set = False

        Return a printable representation of this object.
            sage: from sage.dev.config import Config
            sage: from sage.dev.user_interface import UserInterface
            sage: from sage.dev.git_interface import GitInterface
            sage: config = Config()
            sage: repr(GitInterface(config, UserInterface(config)))

        OUTPUT:
        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

        A ``merge`` state::

            sage: git.checkout(SUPER_SILENT, "branch1")
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1) for `git merge branch2`.
            ...
            sage: git.merge(SUPER_SILENT,abort=True)

        A ``rebase`` state::

            sage: git.execute_supersilent('rebase', 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1) for `git rebase branch2`.
            ...
            sage: git.rebase(SUPER_SILENT, abort=True)

        A merge within an interactive rebase::

            sage: git.rebase(SUPER_SILENT, 'HEAD^', interactive=True, env={'GIT_SEQUENCE_EDITOR':'sed -i s+pick+edit+'})
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1) for `git merge branch2`.
            ...
            sage: git.rebase(SUPER_SILENT, abort=True)
        Get out of a merge/am/rebase/etc state.
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

        A merge within an interactive rebase::

            sage: git.checkout(SUPER_SILENT, "branch1")
            sage: git.rebase(SUPER_SILENT, 'HEAD^', interactive=True, env={'GIT_SEQUENCE_EDITOR':'sed -i s+pick+edit+'})
            ('rebase-i',)
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1) for `git merge branch2`.
            ...

        Get out of this state::

            sage: git.reset_to_clean_state()

            return
        Reset any changes made to the working directory.
        INPUT:

        - ``remove_untracked_files`` -- a boolean (default: ``False``), whether
          to remove files which are not tracked by git

        - ``remove_untracked_directories`` -- a boolean (default: ``False``),
          whether to remove directories which are not tracked by git

        - ``remove_ignored`` -- a boolean (default: ``False``), whether to
          remove files directories which are ignored by git

        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Set up some files/directories::

            sage: os.chdir(config['git']['src'])
            sage: open('tracked','w').close()
            sage: git.add(SUPER_SILENT, 'tracked')
            sage: with open('.gitignore','w') as f: f.write('ignored\nignored_dir')
            sage: git.add(SUPER_SILENT, '.gitignore')
            sage: git.commit(SUPER_SILENT, '-m', 'initial commit')

            sage: os.mkdir('untracked_dir')
            sage: open('untracked_dir/untracked','w').close()
            sage: open('untracked','w').close()
            sage: open('ignored','w').close()
            sage: os.mkdir('ignored_dir')
            sage: open('ignored_dir/untracked','w').close()
            sage: with open('tracked','w') as f: f.write('version 0')
            sage: git.status()
            # On branch master
            # Changes not staged for commit:
            #   (use "git add <file>..." to update what will be committed)
            #   (use "git checkout -- <file>..." to discard changes in working directory)
            #
            #   modified:   tracked
            #
            # Untracked files:
            #   (use "git add <file>..." to include in what will be committed)
            #
            #   untracked
            #   untracked_dir/
            no changes added to commit (use "git add" and/or "git commit -a")

        Some invalid combinations of flags::

            sage: git.reset_to_clean_working_directory(remove_untracked_files = False, remove_untracked_directories = True)
            Traceback (most recent call last):
            ...
            ValueError: remove_untracked_directories only valid if remove_untracked_files is set
            sage: git.reset_to_clean_working_directory(remove_untracked_files = False, remove_ignored = True)
            Traceback (most recent call last):
            ...
            ValueError: remove_ignored only valid if remove_untracked_files is set

        Per default only the tracked modified files are reset to a clean
        state::

            sage: git.reset_to_clean_working_directory()
            sage: git.status()
            # On branch master
            # Untracked files:
            #   (use "git add <file>..." to include in what will be committed)
            #
            #   untracked
            #   untracked_dir/
            nothing added to commit but untracked files present (use "git add" to track)

        Untracked items can be removed by setting the parameters::

            sage: git.reset_to_clean_working_directory(remove_untracked_files=True)
            Removing untracked
            Not removing untracked_dir/
            sage: git.reset_to_clean_working_directory(remove_untracked_files=True, remove_untracked_directories=True)
            Removing untracked_dir/
            sage: git.reset_to_clean_working_directory(remove_untracked_files=True, remove_ignored=True)
            Removing ignored
            Not removing ignored_dir/
            sage: git.reset_to_clean_working_directory(remove_untracked_files=True, remove_untracked_directories=True, remove_ignored=True)
            Removing ignored_dir/

        if remove_untracked_directories and not remove_untracked_files:
            raise ValueError("remove_untracked_directories only valid if remove_untracked_files is set")
        if remove_ignored and not remove_untracked_files:
            raise ValueError("remove_ignored only valid if remove_untracked_files is set")

        self.reset(SILENT, hard=True)
        Common implementation for :meth:`execute`, :meth:`execute_silent`,
        :meth:`execute_supersilent`, and :meth:`read_output`
          - ``stdout`` - if set to ``False`` will supress stdout
          - ``stderr`` - if set to ``False`` will supress stderr
            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git._run_git('status', (), {})
            # On branch master
            # Initial commit
            #
            nothing to commit (create/copy files and use "git add" to track)
            (0, None, None, 'git status')
            (0, None, None, 'git status')

        TESTS:

        Check that we refuse to touch the live source code in doctests::

            sage: dev.git.status()
            Traceback (most recent call last):
            ...
            AssertionError: possible attempt to work with the live repository/directory in a doctest - did you forget to dev._chdir()?

        import sage.doctest
        import os
        assert not sage.doctest.DOCTEST_MODE or (self._dot_git != SAGE_DOT_GIT and self._repository != SAGE_REPO_AUTHENTICATED and os.path.abspath(os.getcwd()).startswith(self._src)), "possible attempt to work with the live repository/directory in a doctest - did you forget to dev._chdir()?"

        # not sure which commands could possibly create a commit object with
        # some crazy flags set - these commands should be safe
        if cmd not in [ "config", "diff", "grep", "log", "ls_remote", "remote", "reset", "show", "show_ref", "status", "symbolic_ref" ]:
            self._check_user_email()

        complete_cmd = " ".join([arg for i,arg in enumerate(s) if i!=1]) # drop --git-dir from debug output
        self._UI.show("[git] %s"%complete_cmd, log_level=INFO)
        import subprocess
        drop_stdout = ckwds.get('stdout') is False
        read_stdout = ckwds.get('stdout') is str
        drop_stderr = ckwds.get('stderr') is False
        read_stderr = ckwds.get('stderr') is str

        if drop_stdout or read_stdout:
        if drop_stderr or read_stderr:


        # recover stdout and stderr for debugging on non-zero exit code
        if retcode:
            if drop_stdout or read_stdout:
                pass
            else:
                stdout = None

            if drop_stderr or read_stderr:
                pass
            else:
                stderr = None
        else:
            if not read_stdout:
                stdout = None
            if not read_stderr:
                stderr = None

        return retcode, stdout, stderr, complete_cmd
        - ``cmd`` - git command run
        - ``args`` - extra arguments for git
        - ``kwds`` - extra keywords for git
            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.execute('status')
            # On branch master
            # Initial commit
            nothing to commit (create/copy files and use "git add" to track)
            sage: git.execute_silent('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129) for `git status --foo`.

        exit_code, stdout, stderr, cmd = self._run_git(cmd, args, kwds)
            raise GitError(exit_code, cmd, stdout, stderr)
            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.execute_silent('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129) for `git status --foo`.

        exit_code, stdout, stderr, cmd = self._run_git(cmd, args, kwds, stdout=False)
            raise GitError(exit_code, cmd, stdout, stderr)
            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.execute_supersilent('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129) for `git status --foo`.
            ...

        exit_code, stdout, stderr, cmd = self._run_git(cmd, args, kwds, stdout=False, stderr=False)
            raise GitError(exit_code, cmd, stdout, stderr)
            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.read_output('status')
            '# On branch master\n#\n# Initial commit\n#\nnothing to commit (create/copy files and use "git add" to track)\n'
            sage: git.read_output('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129) for `git status --foo`.
            ...

        exit_code, stdout, stderr, cmd = self._run_git(cmd, args, kwds, stdout=str, stderr=False)
            raise GitError(exit_code, cmd, stdout, stderr)
        return stdout
        Return whether ``a`` is a child of ``b``.
        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

            sage: git.is_child_of('master', 'branch2')
            sage: git.is_child_of('branch2', 'master')
            sage: git.is_child_of('branch1', 'branch2')
            False
            sage: git.is_child_of('master', 'master')

        Return whether ``a`` is an ancestor of ``b``.
        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

            sage: git.is_ancestor_of('master', 'branch2')
            sage: git.is_ancestor_of('branch2', 'master')
            False
            sage: git.is_ancestor_of('branch1', 'branch2')
            sage: git.is_ancestor_of('master', 'master')

        return self.merge_base(READ_OUTPUT, a, b) == self.rev_parse(READ_OUTPUT, a)
        Return whether there are uncommitted changes, i.e., whether there are
        modified files which are tracked by git.
        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        An untracked file does not count towards uncommited changes::

            sage: os.chdir(config['git']['src'])
            sage: open('untracked','w').close()
        Once added to the index it does::
            sage: git.add('untracked')
            sage: git.commit(SUPER_SILENT, '-m', 'tracking untracked')
            sage: with open('untracked','w') as f: f.write('version 0')
            sage: git.has_uncommitted_changes()
            True

        return bool([line for line in self.status(READ_OUTPUT, porcelain=True).splitlines() if not line.startswith('?')])
    def untracked_files(self):
        Return a list of file names for files that are not tracked by git and
        not ignored.
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
        An untracked file::
            sage: os.chdir(config['git']['src'])
            sage: git.untracked_files()
            []
            sage: open('untracked','w').close()
            sage: git.untracked_files()
            ['untracked']
         Directories are not displayed here::
            sage: os.mkdir('untracked_dir')
            sage: git.untracked_files()
            ['untracked']
            sage: open('untracked_dir/untracked','w').close()
            sage: git.untracked_files()
            ['untracked', 'untracked_dir/untracked']
        import os
        old_cwd = os.getcwd()
        from sage.env import SAGE_ROOT
        os.chdir(SAGE_ROOT)
            fnames = self.ls_files(READ_OUTPUT, other=True, exclude_standard=True).splitlines()
            fnames = [ os.path.abspath(fname) for fname in fnames ]
            return [ os.path.relpath(fname, old_cwd) for fname in fnames ]
        finally:
            os.chdir(old_cwd)
    def local_branches(self):
        Return a list of local branches sorted by last commit time.
        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create some branches::

            sage: os.chdir(config['git']['src'])
            sage: git.commit(SILENT, '-m','initial commit','--allow-empty')
            sage: git.branch('branch1')
            sage: git.branch('branch2')

        Use this repository as a remote repository::

            sage: config2 = DoctestConfig()
            sage: git2 = GitInterface(config2["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config2['git']['src'])
            sage: git2.commit(SILENT, '-m','initial commit','--allow-empty')
            sage: git2.remote('add', 'git', config['git']['src'])
            sage: git2.fetch(SUPER_SILENT, 'git')
            sage: git2.checkout(SUPER_SILENT, "branch1")
            sage: git2.branch("-a")
            * branch1
              master
              remotes/git/branch1
              remotes/git/branch2
              remotes/git/master

            sage: git2.local_branches()
            ['branch1', 'master']
            sage: os.chdir(config['git']['src'])
            sage: git.local_branches()
            ['branch1', 'branch2', 'master']
        result = self.for_each_ref(READ_OUTPUT, 'refs/heads/',
                    sort='-committerdate', format="%(refname)").splitlines()
        return [head[11:] for head in result]
    def current_branch(self):
        Return the current branch
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
        Create some branches::
            sage: os.chdir(config['git']['src'])
            sage: git.commit(SILENT, '-m','initial commit','--allow-empty')
            sage: git.commit(SILENT, '-m','second commit','--allow-empty')
            sage: git.branch('branch1')
            sage: git.branch('branch2')
            sage: git.current_branch()
            'master'
            sage: git.checkout(SUPER_SILENT, 'branch1')
            sage: git.current_branch()
            'branch1'

        If ``HEAD`` is detached::

            sage: git.checkout(SUPER_SILENT, 'master~')
            sage: git.current_branch()
            Traceback (most recent call last):
            ...
            DetachedHeadError: unexpectedly, git is in a detached HEAD state
            return self.symbolic_ref(READ_OUTPUT, 'HEAD', short=True, quiet=True).strip()
        except GitError as e:
            if e.exit_code == 1:
               raise DetachedHeadError()
            raise
    def commit_for_branch(self, branch):
        Return the commit id of the local ``branch``, or ``None`` if the branch
        does not exist
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
        Create some branches::
            sage: os.chdir(config['git']['src'])
            sage: git.commit(SILENT, '-m','initial commit','--allow-empty')
            sage: git.branch('branch1')
            sage: git.branch('branch2')
        Check existence of branches::
            sage: git.commit_for_branch('branch1') # random output
            '087e1fdd0fe6f4c596f5db22bc54567b032f5d2b'
            sage: git.commit_for_branch('branch2') is not None
            sage: git.commit_for_branch('branch3') is not None
            False
        """
        return self.commit_for_ref("refs/heads/%s"%branch)
    def commit_for_ref(self, ref):
        Return the commit id of the ``ref``, or ``None`` if the ``ref`` does
        not exist.
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create some branches::
            sage: os.chdir(config['git']['src'])
            sage: git.commit(SILENT, '-m','initial commit','--allow-empty')
            sage: git.branch('branch1')
            sage: git.branch('branch2')
        Check existence of branches::
            sage: git.commit_for_ref('refs/heads/branch1') # random output
            '087e1fdd0fe6f4c596f5db22bc54567b032f5d2b'
            sage: git.commit_for_ref('refs/heads/branch2') is not None
            True
            sage: git.commit_for_ref('refs/heads/branch3') is not None
            False
        """
            return self.rev_parse(READ_OUTPUT, ref, verify=True).strip()
            return None
    def rename_branch(self, oldname, newname):
        Rename ``oldname`` to ``newname``.
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
        Create some branches::
            sage: os.chdir(config['git']['src'])
            sage: git.commit(SILENT, '-m','initial commit','--allow-empty')
            sage: git.branch('branch1')
            sage: git.branch('branch2')
        Rename some branches::
            sage: git.rename_branch('branch1', 'branch3')
            sage: git.rename_branch('branch2', 'branch3')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (128) for `git branch --move branch2 branch3`.
        self.branch(oldname, newname, move=True)
    def _check_user_email(self):
        Make sure that a real name and an email are set for git. These will
        show up next to any commit that user creates.
        TESTS::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: del config['git']['user.name']
            sage: del config['git']['user.email']
            sage: UI = DoctestUserInterface(config["UI"])
            sage: git = GitInterface(config["git"], UI)
            sage: os.chdir(config['git']['src'])
            sage: UI.append("Doc Test")
            sage: UI.append("doc@test")
            sage: git._check_user_email()
        if self.__user_email_set:
            return
            self.config(SUPER_SILENT, "user.name")
        except GitError as e:
            if e.exit_code == 1:
                self._UI.normal("No real name has been set for git. This name shows up as the author for any commits you contribute to sage.")
                name = self._UI.question("Your real name:")
                self.git.config("user.name",name,local=True,add=True)
                self._UI.info("Your real name has been saved.")
            else:
                raise
        try:
            self.config(SUPER_SILENT, "user.email")
        except GitError as e:
            if e.exit_code == 1:
                self._UI.normal("No email address has been set for git. This email shows up as the author for any commits you contribute to sage.")
                email = self._UI.question("Your email address:")
                self.git.config("user.email",email,local=True,add=True)
                self._UI.info("Your email has been saved.")
            else:
                raise
        self.__user_email_set = True
        "config",
        "cherry_pick",
        "for_each_ref",
        "ls_files",
        "ls_remote",
        "merge_base",
        "remote",
        "rev_list",
        "rev_parse",
        "show_ref",
        "symbolic_ref",
        Create a wrapper for ``git_cmd__``.
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])
            sage: git.status()
            # On branch master
            #
            # Initial commit
            #
            nothing to commit (create/copy files and use "git add" to track)
        meth.__doc__ = r"""
        Call `git {0}`.

        If `args` contains ``SILENT``, then output to stdout is supressed.

        If `args` contains ``SUPER_SILENT``, then output to stdout and stderr
        is supressed.

        OUTPUT:

        Returns ``None`` unless `args` contains ``READ_OUTPUT``; in that case,
        the commands output to stdout is returned.

        See :meth:`execute` for more information.

        EXAMPLES:

            sage: dev.git.{1}() # not tested

        """.format(git_cmd, git_cmd__)