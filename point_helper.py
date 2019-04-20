import json

from vtown.geo.polygon import Polygon


def rand_p(area="1"):
    mypoly = [(30.06657871622343, 31.30840301513672),
              (30.073115284501085, 31.359214782714844),
              (30.039239299161178, 31.36333465576172),
              (30.03686160188358, 31.304969787597656),
              (30.06657871622343, 31.30840301513672)]
    poly = Polygon(*mypoly)
    p = poly.random_point()
    return [p.x, p.y, area]

