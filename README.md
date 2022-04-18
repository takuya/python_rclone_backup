# python_rclone_backup

python_rclone_backup

## install 

sample, install by pip from github.
```shell
pip install git+https://github.com/takuya/python_rclone_backup.git#egg=rclone_backup
```

using pyenv and pipenv 
```shell
pyenv local 3.9.8
pyenv exec pipenv install --python=3.9.8
pyenv exec pipenv install git+https://github.com/takuya/python_rclone_backup.git#egg=rclone_backup
pyenv exec pipenv install 
```

## for rclone backup

- pre/post scripts
- Archiving 
- pipe 
- config

We know `rclone` is great. but backup come with messy procedure.

This will make archiving more simple. add pipe, with `post backup` / `pre backup` commands to maintain.
### pre/post scripts

for achive , pre/post scripts.

### Archiving and Pipe

tar for archive , adding `archive` option alternatively to use `rclone sync`.
```python
['./backup', 'my-remote:/archive-test.tgz', 'archive'],
```

pipe for archive , adding `pipe` option alternatively to use `rclone sync`.

```python
['mysqldump | gzip -c - ', 'my-remote:/mysqldump.sql.gz', 'pipe'],
```

### backup config

config using dict / list, for reducing shell script.

### config example

```python
import os
import sys
import rclone_backup

project_root = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")
sys.path.insert(0, project_root)
from rclone_backup.Backup import Backup


def main():
    config = {
        'pre_backup':  {
            "stop service": "sudo systemctl stop xxx.service"
        },
        'backup_pair': [
            ['./backup/Backup.py', 'my-remote:/', 'copy'],
            ['./backup', 'my-remote:/archive-test.tgz', 'archive'],
            ['apt list --installed | gzip -c - ', 'my-remote:/apt-list.gz', 'pipe'],
        ],
        'post_backup': {
            "start service": "sudo systemctl start xxx.service"
        },
    }
    rclone_config = "~/.rclone.conf"
    rclone_opts = [
        '--links',
        '-q',
    ]
    bk = Backup(rclone_config, rclone_opts, dry_run=(os.environ.get('dry_run') or False))
    bk.add_backup_list(config['backup_pair'])
    bk.add_pre_backup_cmd(config["pre_backup"])
    bk.add_post_backup_cmd(config["post_backup"])
    bk.start(verbose=(os.environ.get('verbose') or False))


if __name__ == '__main__':
    main()

main()

```

This will execute these shell commands.

```shell
sudo systemctl stop xxx.service
sudo tar cvzf /var/www www.tgz
rclone --config ~/.rclone.conf --links copy ./backup/Backup.py my-remote:/Backup.py
tar czf - ./backup | rclone --config ~/.rclone.conf --links rcat  my-remote:/archive-test.tgz
apt list --installed | gzip -c -  | rclone --config ~/.rclone.conf --links rcat  my-remote:/apt-list.gz
sudo systemctl start xxx.service
```

## mysqldump sample : pipe

mysqldump pipe to rclone

```python
import os
from rclone_backup.Backup import Backup

db_host, db_user, db_pass, db_name = ['localhost', 'mysql', 'password', 'db_name']

config = {
  'backup_pair':[
    [f'mysqldump --single-transaction -h {db_host} -u {db_user} --password={db_pass} {db_name}'
     '| gzip -',
     'my-remote:/mysqldump.gz', 'pipe'],
   ]
}



def main():
    bk = Backup(dry_run=(os.environ.get('dry_run') or False))
    bk.add_backup_list(config['backup_pair'])
    bk.start(verbose=(os.environ.get('verbose') or False))


if __name__ == '__main__':
    main()

main()

```



