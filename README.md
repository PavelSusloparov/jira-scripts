# jira-scripts

## jira-flow

The script calculates flow efficiency time.
* Based on individual ticket
* Based on status
* Overall efficiency

Before running the script:
1. install python3, pip3
2. Use pip3 to install the script dependencies(feel free to use [virtualenv](https://docs.python-guide.org/dev/virtualenvs/))
```bash
pip3 install jira
pip3 install arrow
pip3 install datetime
```
3. Create .env file on the root level
4. Supply variables similar to `.env-example` file

Example output:
```.env
https://jira.com/browse/XXXX-1111: 65.90% (2 days, 19:10:51.061000 / 4 days, 5:56:24.406000) Done [Bug]
https://jira.com/browse/XXXX-1112: 76.01% (0:18:22.727000 / 0:24:10.833000) Done [Release]
https://jira.com/browse/XXXX-1113: 0.00% (0:00:00 / 3 days, 11:49:44.762000) Done [Bug]
https://jira.com/browse/XXXX-1114: 72.93% (1 day, 22:35:03.867000 / 2 days, 15:52:26.278000) Done [Bug]

Time in Status Summary
[WAIT] Open: 76.47% (1729 days, 6:51:05.278000 / 2261 days, 11:01:34.901000)
[WORK] In Progress: 6.47% (146 days, 6:52:03.557000 / 2261 days, 11:01:34.901000)
[WORK] In Review: 1.60% (36 days, 6:15:01.036000 / 2261 days, 11:01:34.901000)
[WAIT] In Code Review: 1.38% (31 days, 5:15:23.387000 / 2261 days, 11:01:34.901000)
[WORK] In Planning: 0.40% (8 days, 23:33:24.749000 / 2261 days, 11:01:34.901000)
[WAIT] In Development: 7.69% (173 days, 21:44:56.954000 / 2261 days, 11:01:34.901000)
[WAIT] Won't Do: 3.31% (74 days, 18:56:25.892000 / 2261 days, 11:01:34.901000)
[WORK] In release: 2.68% (60 days, 14:25:52.461000 / 2261 days, 11:01:34.901000)
[WAIT] To Do: 0.01% (3:07:21.587000 / 2261 days, 11:01:34.901000)

Overall
11.15% (252 days, 3:06:21.803000 / 2261 days, 11:01:34.901000)
```

