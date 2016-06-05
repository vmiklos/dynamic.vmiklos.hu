#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import calendar
import locale
import random
import sys
import time
locale.setlocale(locale.LC_ALL, "hu_HU.UTF-8")
sys = reload(sys)
sys.setdefaultencoding("utf-8")


class MyCalendar(calendar.LocaleHTMLCalendar):
    def formatday(self, day, weekday):
        """
        Return a day as a table cell, including a random task.
        """
        if day == 0:
            # Day is outside the month.
            return '<td class="noday">&nbsp;</td>'
        else:
            task = random.choice(tasks).decode('utf-8')
            return '<td class="day">%d<br />%s</td>' % (day, task)

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (theyear, calendar.month_name[themonth])
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table, including a visible border.
        """
        v = []
        a = v.append
        a('<table class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatweekday(self, day):
        """
        Return a weekday name as a table header, but use day_name, not
        day_abbr.
        """
        name = calendar.day_name[day].decode('utf-8')
        return '<th class="%s">%s</th>' % (self.cssclasses[day], name)

tasks = [
    "Segítségnyújtés gyermekeinknek az érzéseik elfogadásában (35.&nbsp;o.)",
    "Együttműködésre bírni gyermekeinket (79.&nbsp;o.)",
    "Büntetés helyett (118.&nbsp;o.)",
    "Az önállóság támogatása (151.&nbsp;o.)",
    "Dicséret és önértékelés (182.&nbsp;o.)",
    "Hogy ne kelljen gyermekeinknek szerepet játszaniuk (211.&nbsp;o.)"
]


def formatszihkcal():
    """
    Return a complete HTML page, using MyCalendar().
    """
    ret = []

    cal = MyCalendar()
    ret.append("""<!doctype html>
    <html>
    <head>
        <meta charset="utf-8" />
        <style>
        td.day {
            text-align: center;
        }
        table, td, th {
            border: 1px solid;
            border-spacing: 0;
        }
        </style>
        <title>SZIHK naptár</title>
    </head>
    <body>""".encode('utf-8'))
    now = time.localtime()
    html = cal.formatmonth(now.tm_year, now.tm_mon).encode('utf-8')
    ret.append(html)
    ret.append("""</body>
    </html>""")
    return "".join(ret)


def application(environ, start_response):
    """
    This is used by mod_wsgi.
    """
    status = '200 OK'
    output = formatszihkcal()

    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)

    return [output]

if __name__ == "__main__":
    print(formatszihkcal())

# vim:set shiftwidth=4 softtabstop=4 expandtab:
