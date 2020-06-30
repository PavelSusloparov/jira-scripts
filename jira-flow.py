from jira import JIRA
import arrow
import datetime
from collections import defaultdict
import os

# Before running the script, update and source your .env file
JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_USER_NAME = os.getenv('JIRA_USER_NAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
JIRA_PROJECT = os.getenv('JIRA_PROJECT')

print("Connect to JIRA")
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER_NAME, JIRA_PASSWORD))

work = ['In Planning', 'In Progress', 'In Review', 'In release', 'In Testing']
done = ['Resolved', 'Closed', 'Done']


def log_change(log, state, curr_change, prev_change):
    if state in done:
        return prev_change

    log[state] += curr_change - prev_change
    return curr_change


def append_log(master_log, log):
    for key in log.keys():
        master_log[key] += log[key]


def wait_time(log):
    delta = datetime.timedelta()
    for state in log:
        if state not in work:
            delta += log[state]

    return delta


def work_time(log):
    delta = datetime.timedelta()
    for state in log:
        if state in work:
            delta += log[state]

    return delta


master_log = defaultdict(datetime.timedelta)
print('Individual Issues')

projects = [JIRA_PROJECT]
buffer_size = 200
start_at = 0
while buffer_size > 0:
    jql = 'project IN ("{}") AND type in (standardIssueTypes()) AND status in ({}) AND created >= "2020-01-01 00:01" AND created <= "2020-04-01 00:01" ORDER BY key ASC'.format(
        '","'.join(projects), ','.join(done))
    print(jql)
    issues = jira.search_issues(jql, maxResults=buffer_size, startAt=start_at, expand='changelog')
    for issue in issues:
        issue_log = defaultdict(datetime.timedelta)
        prev_change = arrow.get(issue.fields.created)

        changelog = issue.changelog
        for history in changelog.histories:
            for change in history.items:
                if change.field != 'status':
                    continue

                prev_change = log_change(issue_log, str(change.fromString), arrow.get(history.created), prev_change)

        curr_status = str(issue.fields.status)
        log_change(issue_log, curr_status, arrow.now(), prev_change)

        issue_work_time = work_time(issue_log)
        issue_wait_time = wait_time(issue_log)
        issue_time = issue_work_time + issue_wait_time
        print('{:s}: {:0.2f}% ({:s} / {:s}) {:s} [{:s}]'.format(str(issue.permalink()),
                                                                issue_work_time * 100 / issue_time,
                                                                str(issue_work_time), str(issue_time), curr_status,
                                                                str(issue.fields.issuetype)))

        append_log(master_log, issue_log)

    if len(issues) < buffer_size:
        buffer_size = 0
    else:
        start_at += buffer_size

total_work_time = work_time(master_log)
total_wait_time = wait_time(master_log)
total_time = total_work_time + total_wait_time

print()
print('Time in Status Summary')
for status in master_log.keys():
    if master_log[status] != datetime.timedelta():
        print('[{}] {}: {:0.2f}% ({:s} / {:s})'.format('WORK' if status in work else 'WAIT', status,
                                                       master_log[status] * 100 / total_time, str(master_log[status]),
                                                       str(total_time)))

print()
print('Overall')
print('{:0.2f}% ({:s} / {:s})'.format(total_work_time * 100 / total_time, str(total_work_time), str(total_time)))
