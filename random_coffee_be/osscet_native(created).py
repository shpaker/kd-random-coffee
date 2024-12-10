from datetime import datetime
from pytz import UTC

created_at = datetime(2023, 10, 1, 11, 0, tzinfo=UTC)
created_at_naive = created_at.replace(tzinfo=None)