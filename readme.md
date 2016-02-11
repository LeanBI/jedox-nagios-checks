#Check scripts for monitoring jedox with nagios

##check_jedox_backup
example:
--file-template backup-jedox_leanbi_ch-%s_*.tgz --date-format %Y-%m-%d --backup-time 04:15 --backup-dir /opt/jedox_backup --backup-file-size 30

##check_jedox_ports
example:
--ports 7777,olap --ports 80,http

##check_jedox_services
For this one, you will need to install psutil first
example:
--services tomcat,java,/opt/jedox/ps/tomcat/bin/bootstrap.jar:/opt/jedox/ps/tomcat/bin/tomcat-juli.jar --services SupervisionServ,SupervisionServ --services palo,palo --services core,core.bin

[LeanBI](http://leanbi.ch/big-data/)