#! /usr/bin/env python
from datetime import datetime, date, timedelta
import sys
from subprocess import call

#Need to add usage and help etc.

account_name =  sys.argv[1]
warning_limit = timedelta(days=(int(sys.argv[2])))
#warning_limit=timedelta(days=14)
critical_limit = timedelta(days=(int(sys.argv[3])))
#critical_limit=timedelta(days=2)

#This is totally a hack
#It also might not work, this line below has not actually been tested, although the ipa command inside has been.
expiration_datetime=check_output("ipa user-show %s --all |grep krbpasswordexpiration | set 's/Z$/UTC/'", shell=True) % account_name
#Need to hook into ipa's python api to pull this value out.
#Add that to TO-DO List.

#Uncomment this to use for testing
#expiration_datetime='2014036021457UTC'

dt=datetime.strptime(expiration_datetime,'%Y%m%d%H%M%S%Z')
print(dt)

#Determine the state of the check and pass to Nagios
#CRITICAL = 2
#WARNING = 1
#OK = 0

days_to_expire= dt.date()-date.today()
#Uncomment at set this value below to test
#days_to_expire =  timedelta(15,5,41038)

if days_to_expire <= critical_limit:
    print "ACCOUNT EXPIRATION CRITICAL: Password will expire in %s days" % (str(days_to_expire.days))
    sys.exit(2)
elif days_to_expire <= warning_limit:
    print "ACCOUNT EXPIRATION WARNING: Password will expire in %s days" % (str(days_to_expire.days))
    sys.exit(1)
else:
    print "ACCOUNT EXPIRATION OK: Password will expire in %s days" % (str(days_to_expire.days))
    sys.exit(0)
