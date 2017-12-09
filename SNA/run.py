from bigquery_event_collector import *
import datetime

if __name__ == "__main__":
    print(datetime.datetime.now())
    bquery = EventAnalysis()

    folder_name = 'Global_20171210'
    get_repository_from = 'global_200.csv'
    id = 'rlrlaa123'
    pw = 'ehehdd009'

    # bquery.getRepositories(get_repository_from)
    for repo in bquery.REPOSITORY:
        bquery.collectEvent(repo, folder_name, id, pw)
        bquery.snaAnalysis(repo, folder_name)
        bquery.typeCount(repo, folder_name)
        bquery.userCategorize(repo, folder_name)
    bquery.categorizedUserCount(folder_name)
    bquery.snaDensity(folder_name)
    # bquery.classifySWType(folder_name)
    bquery.countRatio(folder_name)
    # bquery.getSWCategory()
    bquery.snaMaxAvg(folder_name)
    print(datetime.datetime.now())