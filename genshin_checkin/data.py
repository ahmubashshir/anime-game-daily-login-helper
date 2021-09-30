from os import environ as ENV

EVENT_DOMAIN = 'hk4e-api-os'
ACT_ID = 'e202102251931481'

URL = 'https://%s.mihoyo.com/event/sol/{}?lang=en-us&act_id=%s' % (
    EVENT_DOMAIN, ACT_ID
)

# vim: ft=python3:ts=4:et:
