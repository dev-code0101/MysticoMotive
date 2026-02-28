from .models import Train


def get_station_sequence(train: Train) -> list[str]:
    """
    Return the ordered list of station codes for a train,
    taking its direction (FORWARD/BACKWARD) into account.
    """
    stations_qs = train.route.stations.all()
    if train.direction == Train.DIRECTION_BACKWARD:
        stations_qs = stations_qs.order_by("-order")
    return [rs.station.code for rs in stations_qs]

