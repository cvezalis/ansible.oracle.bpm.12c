db_server_name = '{{ dbserver_name }}'
db_server_port = '{{ dbserver_port }}'
db_service = '{{ dbserver_service }}'
data_source_url='jdbc:oracle:thin:@//' + db_server_name + ':' + db_server_port + '/' + db_service
data_source_user_prefix= '{{ repository_prefix }}'
data_source_test='SQL SELECT 1 FROM DUAL'

domain_application_home = '{{ applications_home }}/{{ domain_name }}'
domain_configuration_home = '{{ domains_home }}/{{ domain_name }}'
domain_name = '{{ domain_name }}'
java_home = '{{ jdk_folder }}'
middleware_home = '{{ middleware_home }}'
weblogic_home = '{{ weblogic_home }}'

weblogic_template=weblogic_home + '/common/templates/wls/wls.jar'
bpm_template=middleware_home + '/soa/common/templates/wls/oracle.bpm_template.jar'

readTemplate(weblogic_template)
setOption('DomainName', domain_name)
setOption('OverwriteDomain', 'true')
setOption('JavaHome', java_home)
setOption('ServerStartMode', 'prod')

cd('/Security/base_domain/User/weblogic')
cmo.setName('{{ weblogic_admin }}')
cmo.setUserPassword('{{ weblogic_admin_pass }}')
cd('/')

writeDomain(domain_configuration_home)
closeTemplate()

readDomain(domain_configuration_home)
addTemplate(bpm_template)
setOption('AppDir', domain_application_home)

jdbcsystemresources = cmo.getJDBCSystemResources()
for jdbcsystemresource in jdbcsystemresources:
    cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' + jdbcsystemresource.getName() + '/JDBCConnectionPoolParams/NO_NAME_0')
    cmo.setInitialCapacity(1)
    cmo.setMaxCapacity(15)
    cmo.setMinCapacity(1)
    cmo.setStatementCacheSize(0)
    cmo.setTestConnectionsOnReserve(java.lang.Boolean('false'))
    cmo.setTestTableName(data_source_test)
    cmo.setConnectionCreationRetryFrequencySeconds(30)
    cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' + jdbcsystemresource.getName() + '/JDBCDriverParams/NO_NAME_0')
    cmo.setUrl(data_source_url)
    cmo.setPasswordEncrypted('{{ datasource_password }}')
   
    cd ('/JDBCSystemResource/' + jdbcsystemresource.getName() + '/JdbcResource/' + jdbcsystemresource.getName() + '/JDBCDriverParams/NO_NAME_0/Properties/NO_NAME_0/Property/user')
    cmo.setValue(cmo.getValue().replace('DEV',data_source_user_prefix))
    cd('/')

create('{{ server_hostname }}','UnixMachine')
cd('/UnixMachine/' + '{{ server_hostname }}')
create('{{ server_hostname }}','NodeManager')
cd('NodeManager/' + '{{ server_hostname }}')
cmo.setNMType('SSL')
cmo.setListenAddress('{{ node_manager_listen_address }}')
cmo.setListenPort({{ node_manager_listen_port }})

cd("/SecurityConfiguration/" + domain_name)
cmo.setNodeManagerUsername('{{ nodemanager_username }}')
cmo.setNodeManagerPasswordEncrypted('{{ nodemanager_password }}')

cd('/Server/' + '{{ admin_server_name }}')
set('Machine', '{{ server_hostname }}')
create('{{ admin_server_name }}','SSL')

cd('SSL/' + '{{ admin_server_name }}')
cmo.setHostnameVerifier(None)

cd('/')
cmo.createServer('{{ managed_server_name }}')

cd('/Servers/' + '{{ managed_server_name }}')
cmo.setListenAddress('{{ server_hostname }}')
cmo.setListenPort({{ managed_server_port }})

set('Machine','{{ server_hostname }}')

setServerGroups('{{ managed_server_name }}', ['SOA-MGD-SVRS'])

updateDomain()
closeDomain()