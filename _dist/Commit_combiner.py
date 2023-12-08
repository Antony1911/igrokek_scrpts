import datetime
import os
import subprocess
import sys
import tempfile
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_SINGLE



def check_pwd_is_git_repo(path):
    if not os.path.exists(os.path.join(path, '.git')):
        raise Exception('Not a normal git repo: %s' % path)


def pull():
    print ('Pulling changes in %s...' % os.getcwd())
    #subprocess.check_call(['git', 'pull'])
    return execute_git(['pull'], no_output=True)


def get_file_history(file):
    logs = execute_git(['log', '--oneline', file])
    file_log = []
    for log in logs:
        file_log.append(log.split(' ')[0])

    return file_log


def get_pure_commit_history(count):
    logs = execute_git(['log', '--pretty=oneline', '-n%d' % count])
    file_log = []
    for log in logs:
        if ('Merge' in log and 'branch' in log) or '[igrotek]' in log.lower():
            continue
        file_log.append(log.split(' ')[0])

    return file_log


def execute_git(args, no_output=False):
    git_args = ['git']
    git_args.extend(args)

    #print ('\tCall git: %s' % git_args)
    if no_output:
        outbuf = None
    else:
        outbuf = tempfile.TemporaryFile()

    process = subprocess.Popen(git_args, stdout=outbuf, shell=True)
    process.wait()

    if no_output:
        results = []
    else:
        outbuf.seek(0)
        results = outbuf.readlines()
        outbuf.close()

    if process.returncode != 0:
        raise Exception('Git execution failed with code %d: %s') % (process.returncode, results)

    #print ('\tGit execution results: %s' % results)
    str_results = []
    for result in results:
        str_results.append(result.decode('utf8'))

    return str_results


def switch_on_branch(branch, home):
    if home == False:
        print ('Stashing local changes...')
        execute_git(['stash'])
    else:
        print ('Applying local changes...')
        execute_git(['stash','apply'])
    print ('Switching on branch %s...' % branch)
    execute_git(['checkout', branch])
    if home == False:
        print ('Stashing local changes %s...' % branch)
        execute_git(['stash'])
    else:
        print ('Applying local changes...')
        execute_git(['stash','apply'])

def transfer_commits(source, target, start_commit):
    # Switch on source branch
    # execute_git(['reset', '--hard'])
    switch_on_branch(source, False)
    pull()
    
    # Retrieve history
    history = get_pure_commit_history(1000)
    idx = history.index(start_commit)
    new_commits = history[:idx]
    
    if len(new_commits) == 0:
        print ('Nothing to sync')
        return start_commit
    else:
        latest_commit = new_commits[0]

    print ('Found %d new commits' % len(new_commits))
    
    # Checkout every commit to fix LFS issues
    i = 1
    for new_commit in new_commits:   
        print ('[%d/%d] Checkouting new commit %s' % (i, len(new_commits), new_commit))
        i += 1
        execute_git(['checkout', new_commit])
    
    # Switch on target branch
    switch_on_branch(target, False)
    execute_git(['pull'])
    
    # Reverse commit history for applying
    new_commits.reverse()
    # Apply new commits
    # Sqash the same task commits

    i = 1
    start_sequence = execute_git(['log', '--pretty=format:%h', 'head', '-1'])[0]
    commit_message = execute_git(['log', '--pretty=format:%s', new_commits[0]])[0].split(':')[0]
    print ('[%d/%d] Apply new commit %s' % (i, len(new_commits), new_commit))
    i += 1
    execute_git(['cherry-pick', new_commit])
    for new_commit in new_commits[1:]:
        if execute_git(['log', '--pretty=format:%s', new_commit])[0].split(':')[0] == commit_message:
            print ('[%d/%d] Apply new commit %s' % (i, len(new_commits), new_commit))
            execute_git(['cherry-pick', new_commit])
            execute_git(['reset', '--soft', start_sequence])
            execute_git(['commit', '-m', commit_message + 
                        ': commit transfer from ' + new_commits[0] + ' to ' + new_commits[-1]])
            i += 1
        else:
            start_sequence = execute_git(['log', '--pretty=format:%h', 'head', '-1'])[0]
            commit_message = execute_git(['log', '--pretty=format:%s', new_commit])[0].split(':')[0]
            print ('[%d/%d] Apply new commit %s' % (i, len(new_commits), new_commit))
            execute_git(['cherry-pick', new_commit])
            i += 1

    return latest_commit
    
    
def get_git_remotes(repo_path):
    cwd = os.getcwd()
    os.chdir(repo_path)
    remotes = execute_git(['remote', '--verbose'])
    os.chdir(cwd)
    
    remotes_list = []
    for remote in remotes:
        remotes_list.append(remote.replace('\t', ' ').split(' ')[1])
    
    return list(dict.fromkeys(remotes_list))


def select_foreign_remote(repo_path):
    remotes = get_git_remotes(repo_path)
    
    for remote in remotes:
        if 'igro-tek' not in remote and 'igrotek' not in remote:
            return remote
    
    raise Exception('Cannot find foreign remote in %s' % remotes)


def get_last_sync_commit_filename(repo_path):
    repo = select_foreign_remote(repo_path) \
        .replace('http://', '') \
        .replace('https://', '') \
        .replace('git@', '') \
        .replace('.git', '') \
        .replace('/', '_') \
        .replace('\\', '_') \
        .replace(':', '_')
    return '.lastsyncedcommit_%s' % repo


def load_last_synced_commit(repo_path):
    with open(get_last_sync_commit_filename(repo_path), 'r') as file:
        return file.read()


def save_last_synced_commit(commit, repo_path):
    with open(get_last_sync_commit_filename(repo_path), 'w') as file:
        file.write(commit)


def UI_input():
    
    repo_list_column = [
    [
        sg.Text("Repo Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-Repo-"),
        sg.FolderBrowse(),
    ],
    [   sg.Text("Source branch"),
        sg.Listbox(values=[], enable_events=True, select_mode=LISTBOX_SELECT_MODE_SINGLE, size=(40, 20), key="-Source branch-"),
        sg.Text("Target branch"),
        sg.Listbox(values=[], enable_events=True, select_mode=LISTBOX_SELECT_MODE_SINGLE, size=(40, 20), key="-Target branch-"),
    ],
    [   sg.Text("-Last commit-"),
        sg.InputText(key="-Last commit-"),
    ],
    [sg.Button('Ok'), sg.Button('Cancel')]
    ]
    window = sg.Window('Branch syncer', repo_list_column)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        repo_path = values['-Repo-'].replace('/','\\')
        try:
            os.chdir(repo_path)
        except OSError:
            continue
        branches = execute_git(['branch', '--list'])
        window.FindElement('-Source branch-').update(branches)
        window.FindElement('-Target branch-').update(branches)
        if event == "-Source branch-":
            source_branch = values["-Source branch-"][0].rstrip().lstrip().replace('* ','')
        if event == "-Target branch-":
            target_branch = values["-Target branch-"][0].rstrip().lstrip().replace('* ','')
        if event == 'Ok': 
            try:
                start_commit = values["-Last commit-"][0].rstrip().lstrip()    
            except IndexError:
                start_commit = None
            window.close()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break      
    return repo_path, source_branch, target_branch, start_commit

if __name__ == '__main__':
    cwd = os.getcwd()
    args = UI_input()
    repo_path = args[0].lower()
    check_pwd_is_git_repo(repo_path)
    
    source_branch = args[1]
    target_branch = args[2]
    if args[3] != None:
        start_commit = args[3]
    else:
        os.chdir(cwd)
        start_commit = load_last_synced_commit(repo_path)

    os.chdir(repo_path)
    last_synced = transfer_commits(source_branch, target_branch, start_commit)
    os.chdir(cwd)
    try:
        switch_on_branch(target_branch, True)
    except:
        pass
    try:
        switch_on_branch(source_branch, True)
    except:
        pass
    # Save last synced commit hash
    if last_synced != start_commit:
        message = 'Save last synced commit %s from %s' % (last_synced, datetime.datetime.now())

        print ('Save last synced commit %s' % message)
        save_last_synced_commit(last_synced, repo_path)
        execute_git(['add', get_last_sync_commit_filename(repo_path)])
        execute_git(['commit', '-m', message])
        execute_git(['push'])
