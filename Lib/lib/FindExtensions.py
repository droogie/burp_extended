################################################################################
# Copyright (C) 2011-2012 Joseph Tartaro <droogie[at]burpextensions[dot]com>
# Copyright (C) 2011-2012 James Lester <infodel[at]burpextensions[dot]com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 2 as
# published by the Free Software Foundation.  You may not use, modify or
# distribute this program under any other version of the GNU General
# Public License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
################################################################################

import os
import imp
import inspect
import Extension

def getExtensionClassList():
    moduleDict = {}
    classTools = []
    #(\/)(*;;;;*)(\/) - zoidberg will find all your extensions for you.
    for r,d,f in os.walk("lib/extensions/"):
        for files in f:
            if files.endswith(".py"):
                 path = os.path.join(r,files)
                 moduleDict[path] = imp.load_source(files[:-3], path)
                 members = inspect.getmembers(moduleDict[path], lambda m:inspect.isclass(m))
                 for name, member in members:
                    if member != Extension.Extension and issubclass(member, Extension.Extension):
                        classTools.append(member)

    return classTools
