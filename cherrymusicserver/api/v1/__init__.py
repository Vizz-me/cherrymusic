#!/usr/bin/env python3
#
# CherryMusic - a standalone music server
# Copyright (c) 2012 Tom Wallroth & Tilman Boerner
#
# Project page:
#   http://fomori.org/cherrymusic/
# Sources on github:
#   http://github.com/devsnd/cherrymusic/
#
# CherryMusic is based on
#   jPlayer (GPL/MIT license) http://www.jplayer.org/
#   CherryPy (BSD license) http://www.cherrypy.org/
#
# licensed under GNU GPL version 3 (or later)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

#python 2.6+ backward compability
from __future__ import unicode_literals

import cherrypy

from cherrymusicserver.api.v1 import jsontools
from cherrymusicserver.api.v1 import users
from cherrymusicserver.api.v1.resources import Resource


debug = True


def get_resource():
    root = ResourceRoot()
    root.users = users.get_resource()
    return root


def get_config():
    return {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'error_page.default': jsontools.json_error_handler,
            'tools.json_out.on': True,
            'tools.json_out.handler': jsontools.json_handler,
            'tools.json_in.on': True,
            'tools.sessions.on': False,
        }
    }


def mount(mountpath):
    cherrypy.tree.mount(get_resource(), mountpath, config=get_config())


class ResourceRoot(Resource):

    def GET(self):
        resources = []
        for name, member in self.__dict__.items():
            if getattr(member, 'exposed', False):
                resources.append(name)
        return resources
