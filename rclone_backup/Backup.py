import subprocess
import sys
##  for pp
from pprint import PrettyPrinter
from subprocess import Popen

pp_printer = PrettyPrinter()
pp = pp_printer.pprint


class Backup:
    rclone = '/usr/bin/rclone'

    def __init__(self, rclone_config=None, rclone_options=None, dry_run=False, verbose=False) -> None:
        if rclone_options is None:
            rclone_options = [
                '--no-update-modtime',
                '--size-only',
                '--links',
                '-q',
            ]
        if rclone_config is None:
            rclone_config = '~/.rclone.conf'
        ##
        self.rclone_config = rclone_config
        self.rclone_options = rclone_options
        self.pre_backup_cmds = []
        self.post_backup_cmds = []
        self.backup_pair = []
        self.backup_cmds = []
        self.verbose = verbose
        self.tasks = []
        self.dry_run = dry_run

    def build_backup_cmds(self):
        cmds = []
        for e in self.backup_pair:
            name = e['name']
            opr, src, dst = e['args']
            cmd = {
                "name": name,
                "cmd":  self.__rclone_cmd(opr, src, dst)
            }
            cmds.append(cmd)
        return cmds

    def __rclone_options(self):
        opts = self.rclone_options.copy()
        opts.append(f'--config {self.rclone_config}')
        if self.verbose:
            opts.append('--verbose')
        if self.dry_run:
            opts.append('--dry-run')
        opts = list(map(str.strip, opts))
        opts.sort()
        return opts

    def __rclone_cmd(self, opr, src='', dst=''):
        opts = self.__rclone_options()

        if opr == 'archive':
            rcd = self.__rclone_cmd('rcat', src='', dst=dst)
            sh_cmd = f'tar czf - {src} | {rcd}'
            if self.dry_run:
                sh_cmd = f"echo '{sh_cmd}'"
            return sh_cmd
        elif opr == 'pipe':
            rcd = self.__rclone_cmd('rcat', src='', dst=dst)
            sh_cmd = f'{src} | {rcd}'
            if self.dry_run:
                sh_cmd = f"echo '{sh_cmd}'"
            return sh_cmd
        else:
            cmd = "rclone %s %s %s %s " % (" ".join(opts), opr, src, dst)
            return cmd

    def __add_cmds(self, target: list, name, cmd):
        if isinstance(cmd, dict):
            for k, v in cmd.items():
                self.__add_cmds(target, k, v)
        elif isinstance(cmd, list):
            for i, e in enumerate(cmd):
                self.__add_cmds(target, f"{name}:{i}", e)
        else:
            target.append({
                "name": name,
                "cmd":  cmd
            })
        return target

    def add_backup_list(self, arr):
        if isinstance(arr[0], list):
            for e in arr:
                self.add_backup_pair(*e)
        else:
            self.add_backup_pair(*arr)

    def add_backup_pair(self, src, dst, sub_cmd='sync', name=None):
        self.backup_pair.append({
            'name': name,
            'args': [sub_cmd, src, dst]
        })

    def add_pre_backup_cmd(self, cmd, name=None):
        self.__add_cmds(self.pre_backup_cmds, name, cmd)

    def add_post_backup_cmd(self, cmd, name=None):
        self.__add_cmds(self.post_backup_cmds, name, cmd)

    def __pre_backup(self):
        for e in self.pre_backup_cmds:
            self.__append_task(e['cmd'], e['name'])

    def __post_backup(self):
        for e in self.post_backup_cmds:
            self.__append_task(e['cmd'], e['name'])

    def __backup_main(self):
        for e in self.build_backup_cmds():
            self.__append_task(e['cmd'], e['name'])

    def __append_task(self, cmd: str, name: str = None):
        self.tasks.append([cmd, name])

    def __start_task(self):
        for task in self.tasks:
            self.__exec_command(*task)

    def __exec_command(self, cmd: str, name: str = None):
        if name is not None:
            print(name)
            sys.stdout.flush()
        print("  " + cmd)

        out = sys.stdout
        if not self.verbose:
            out = subprocess.DEVNULL
        popen = Popen(cmd, shell=True, stdout=out)
        popen.wait()

    def start(self, verbose=False):
        self.verbose = verbose
        self.__pre_backup()
        self.__backup_main()
        self.__post_backup()
        ##
        self.__start_task()
