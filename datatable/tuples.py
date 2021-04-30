from collections import namedtuple

ORDER_STATUSES = namedtuple('ORDER_STATUSES', 'proposal in_progress done rejected')._make(range(4))