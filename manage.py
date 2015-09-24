#!/usr/bin/env python

import os
from MentalUs import create_app, db
from MentalUs.models import MTUser, MTScale, MTAnnouncement, \
    MTExtendFields, MTUserExtendInfo, MTScaleResult, MTUnfinishedScale
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app('dev')
manager = Manager(app)
migrate = Migrate(app, db)


def generate_debug():
    MTUser.generate_debug()
    MTScale.generate_debug()
    MTAnnouncement.generate_debug()
    MTExtendFields.generate_debug()
    MTScaleResult.generate_debug()
    MTUnfinishedScale.generate_debug()


def make_shell_context():
    config_dict = {
        'MTUser': MTUser,
        'MTScale': MTScale,
        'MTAnnouncement': MTAnnouncement,
        'MTExtendFields': MTExtendFields,
        'MTUserExtendInfo': MTUserExtendInfo,
        'MTScaleResult': MTScaleResult,
        'MTUnfinishedScale': MTUnfinishedScale,
        'db': db,
        'generate_debug': generate_debug
    }
    return config_dict

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()