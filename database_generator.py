#!/usr/bin/env python

# Copyright 2014 Clione Software and Havas Worldwide London
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import os


path = os.path.dirname(os.path.realpath(__file__)).strip('/utils')
sys.path.append(path)
print(sys.path)


import hashlib
import uuid
import random
import string

from peewee import *


from sikre.models.models import User, Item, Service, Group


############################
# Admin user creation      #
############################

create_admin = input("Do you want to create an admin user? (Y/n) ")
if create_admin == 'y' or create_admin == 'Y':
    name = input("Full name: ")
    email = input("E-Mail address: ")
    username = input("Username (no spaces): ")
    password = input("Password (we won't ask twice): ")

    # Process the password for storage
    salt = uuid.uuid4().hex.encode('utf-8')
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt).hexdigest()

    # Create the user object in the database
    new_user = User.create(name=name, email=email, username=username,
                           password=hashed_password, token='dummytoken')
    user = new_user.save()
else:
    print("Admin user not created. You can create it afterwards.")


##########################
# Database generation    #
##########################

# Create a dummy user if there's no admin
if create_admin != 'y' and create_admin != 'Y':
    dummy_user = User.create(name="Dummy", email="dummy@example.com",
                             username="dummy", password="dummy")
    user = dummy_user.save()

# Create some groups
groups = 2

while groups > 0:
    chars = "".join([random.choice(string.ascii_letters) for i in range(10)])
    new_group = Group.create(name=chars,)
    group = new_group.save()
    groups -= 1

# Create some items
items = 5

while items > 0:
    chars = "".join([random.choice(string.ascii_letters) for i in range(15)])
    digits = "".join([random.choice(string.digits) for i in range(8)])
    new_item = Item(name=chars, description=chars * 2, group=group, author=user,
                    allowed_users=user)
    item = new_item.save()
    items -= 1

    # Create some services
    services = 2

    while services > 0:
        chars = "".join([random.choice(string.ascii_letters) for i in range(15)])
        digits = "".join([random.choice(string.digits) for i in range(8)])
        new_service = Service(name=chars, username=chars, password=chars, url=chars,
                              item=item)
        new_service.save()
        services -= 1