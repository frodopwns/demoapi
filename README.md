EventsAPI
---------

Receives POSTS with operator/visitor data. Calculates basic event metrics.

To run:

```
docker-compose up
```

To create events:

```
wget --post-data="id=a&from=visitor1&type=message&site_id=1&data_message=hello&timestamp=1" http://localhost:5000/events
wget --post-data="id=b&from=operator1&type=status&site_id=1&data_status=online&timestamp=2" http://localhost:5000/events
wget --post-data="id=c&from=visitor1&type=message&site_id=1&data_message=hello&timestamp=3" http://localhost:5000/events
wget --post-data="id=d&from=operator1&type=status&site_id=1&data_status=offline&timestamp=4" http://localhost:5000/events
wget --post-data="id=e&from=visitor2&type=message&site_id=1&data_message=hello&timestamp=5" http://localhost:5000/events
wget --post-data="id=f&from=operator1&type=status&site_id=1&data_status=online&timestamp=6" http://localhost:5000/events
wget --post-data="id=g&from=visitor2&type=message&site_id=1&data_message=hello&timestamp=7" http://localhost:5000/events
```

To see metrics:

```
wget -qO- http://localhost:5000/stats.json
```

To see the events:

```
wget -qO- http://localhost:5000/events
```
