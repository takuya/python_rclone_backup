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
