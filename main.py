#! /usr/bin/python
from say_thanks import Thanks
import sys
import data

def year_month_date(argv):
  return int(argv[1]), int(argv[2]), int(argv[3])

def get_birthday_wishes(year,month,date):
  return data.date(year,month,day).feeds()

if __name__ == '__main__':
  year, month, day = year_month_date(sys.argv)
  print 'Loading your all wishes, this may take time... '
  wishes = get_birthday_wishes(year,month,day)
  print 'Ohhh !!!, You have {0} people wishing you happy birthday\n'.format( len(wishes) )

  t = Thanks(wishes, 'Thank you very much')
  t.wish_all()
