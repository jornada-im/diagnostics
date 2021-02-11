import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os


def load_xml(xmlname):
    """
    
    """
    tree = ET.parse(xmlname)
    root = tree.getroot()
    return(root)
    
def ediroot_to_df(ediroot):
    """
    Convert an Element Tree object to a dataframe. Each element has
    date, packageid, and service method extracted into a row in the 
    dataframe.
    """
    # Iterate over each element in ediroot and extract the variables
    df = pd.DataFrame({'date':[date.text for date in ediroot.iter('date')],
                   'pkgid':[int(ID.text) for ID in ediroot.iter('identifier')],
                   'action':[sm.text for sm in ediroot.iter('serviceMethod')]}
                     )
    return(df)
                      
    
def load_archived(archivedir='./edi_requests/', scope='knb-lter-jrn',
                  parsedt=False):
    """
    """
    files = os.listdir(archivedir)
    scopefiles = sorted([f for f in files if scope in f])
    for i, f in enumerate(scopefiles):
        root = load_xml(os.path.join('edi_requests', f))
        df = ediroot_to_df(root)
        if i==0:
            df_out = df
        else:
            df_out = pd.concat([df_out, df])
    if parsedt:
        df_out.index = pd.to_datetime(df_out['date'])#, format='%Y-%b-%dT%H:%M:%S.%f')
    return(df_out)




def make_request(scope, fromdt, todt=None):
    """
    This is the _list recent changes_ call.

    curl -i -X GET 'https://pasta.lternet.edu/package/changes/eml?fromDate=2017-02-01T12:00:00&toDate=2020-01-28&scope=knb-lter-jrn'

    see: https://pastaplus-core.readthedocs.io/en/latest/doc_tree/pasta_api/data_package_manager_api.html#list-recent-changes
    """
    if todt is None:
        from datetime import datetime
        todt = datetime.today().strftime('%Y-%m-%d')
    base_url = 'https://pasta.lternet.edu/package/changes/eml'
    params = (
        ('fromDate', fromdt),
        ('toDate', todt),
        ('scope', scope))#
        #('environment', 'production'))
    response = requests.get(base_url, params=params)
    # response = long XML string that can be parsed with elementtree,
    # beautifulsoup, etc. response.text should output the text
    return(response)
        
def load_new_request(fromdt, todt=None, scope='knb-lter-jrn', parsedt=False):
    """
    """
    resp = make_request(scope, fromdt, todt)
    # Probably need some testing here...
    # Parse with ElementTree
    root = ET.fromstring(resp.text)
    # len(root)
    # Convert elements to rows in dataframe
    df_out = ediroot_to_df(root)
    if parsedt:
        df_out.index = pd.to_datetime(df_out['date'])#, format='%Y-%b-%dT%H:%M:%S.%f')
    return(df_out)

def get_counts(df):
    """
    """
    #df.index = pd.to_datetime(df['date'])#, format='%Y-%b-%dT%H:%M:%S.%f')
    # Add columns - number of updates and creates, + extracted study id
    df['n_update'] = 0
    df['n_create'] = 0
    df['n_delete'] = 0
    df['n_tot'] = 0
    df['studyid'] = df.pkgid.astype(str).str[-6:-3] #convert to str, studyid excludes mistaken 0
    # Fill in number of updates or create for each record
    df.loc[df.action=='updateDataPackage','n_update'] = 1
    df.loc[df.action=='createDataPackage','n_create'] = 1
    df.loc[df.action=='deleteDataPackage','n_delete'] = 1
    # for totals, create = +1, delete = -1
    df.loc[df.action=='createDataPackage','n_tot'] = 1
    df.loc[df.action=='deleteDataPackage','n_tot'] = -1
    return(df)

def find_duplicates():
    """
    """
    # There are duplicate deletions (9 at last count)
    df_dd = df.drop_duplicates()
    n_dupdeletes = df.shape[0] - df_dd.shape[0]
    df = df_dd
    # Count deleted packages
    deleted_pkgs = df.loc[df.action=='deleteDataPackage','pkgid']
    print(df.shape)
    print(deleted_pkgs)
    print(n_dupdeletes)

def counts_to_daily(df, startdt = None):
    """
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df['date'])#, format='%Y-%b-%dT%H:%M:%S.%f')
    if startdt is not None:
        df_out = df.loc[df.index > startdt,
                ['n_update', 'n_create', 'n_tot']].resample('D').sum()
    else:
        df_out = df.loc[:,['n_update','n_create','n_tot']].resample('D').sum()
    return(df_out)
        

def get_pkg_revision(pkgid=None, scope='knb.lter.jrn', filt='newest'):
    """
    """
    url = 'https://pasta.lternet.edu/package/eml/' + scope + '/' + pkgid

    params = (
        ('filter', filt)
    )
    response = requests.get(url, params=params)

    return response.text
