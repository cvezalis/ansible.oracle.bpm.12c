#!/bin/bash

JAVA_HOME={{ jdk_folder }}
export JAVA_HOME

{{ middleware_home }}/oracle_common/bin/rcu -silent -responseFile {{ mw_installer_folder }}/rcu.soa.rsp -f < {{ mw_installer_folder }}/rcu.passwd.txt