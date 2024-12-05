# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from snaptrade_client.paths.activities import Api

from snaptrade_client.paths import PathValues

path = PathValues.ACTIVITIES