# python_rclone_backup

python_rclone_backup

## for rclone backup

We know `rclone` is great. but backup come with messy procedure.

This will make archiving more simple. add pipe, with `post backup` / `pre backup` commands to maintain.
### pre/post scripts

for achive , pre/post scripts.

### Archiving and Pipe

for archive , adding `archive` option alternatively to use `rclone sync`.

for archive , adding `pipe` option alternatively to use `rclone sync`.

### backup config

config using dict / list, for reducing shell script.

### config example

```python
import os
from rclone_backup.Backup import Backup

config = {
    'pre_backup':  {
        "stop service": [
            "sudo systemctl stop xxx.service",
            "sudo tar cvzf /var/www www.tgz"
        ]
    },
    'backup_pair': [
        ['www.tgz', 'my-remote:/www.tgz', 'copy'],
        ['./var/log', 'my-remote:/archive-test.tgz', 'archive'],
        ['apt list --installed | gzip -c - ', 'my-remote:/apt-list.gz', 'pipe'],
    ],
    'post_backup': {
        "start service": "sudo systemctl start xxx.service"
    },
}
rclone_config = "~/.rclone.conf"
rclone_opts = [
    '--links',
]


def main():
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
    [f'mysqldump --single-transaction -h {db_host} -u {db_user} --password={db_pass} {db_name}| gzip -c - ',
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



