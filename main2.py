
import os
import sys
import time
import json
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.esearch.esearcher
import entrezpy.esearch.esearch_analyzer
import entrezpy.log.logger
import entrezpy.efetch.efetcher
import entrezpy.esummary.esummarizer

entrezpy.log.logger.LOGLEVEL = 'DEBUG'


def main():

  examples = [
    #{'db':'nucleotide','term':'viruses[orgn]', 'rettype':'count'},
    #{'db':'nucleotide','term':'viruses[orgn]'},
    #{'db':'nucleotide','term':'viruses[orgn]', 'retmax': 110000},
    #{'db':'nucleotide','term':'viruses[orgn]', 'retmax': 0},
    #{'db':'nucleotide','term':'viruses[orgn]', 'reqsize': 100, 'retmax' : 99, 'idtype' : 'acc'},
    #{'db':'pubmed','term':'cancer','reldate':60,'datetype':'edat','retmax':89, 'usehistory':True},
    {'db':'pubmed','term':'cancer','reldate':60,'datetype':'edat','retmax':89, 'rettype':'abstract','usehistory':True},
    #{'db':'pubmed','term':'PNAS[ta] AND 97[vi]', 'retstart':6, 'retmax': 6},
    #{'db':'nlmcatalog','term':'obstetrics AND ncbijournals[filter]', 'retmax':20},
    #{'db':'pmc','term':'stem cells AND free fulltext[filter]'},
    #{'db':'nucleotide','term':'biomol trna', 'field':'prop', 'mindate': 1982, 'maxdate':2017}, # Parameter Fail
    #{'db':'nucleotide','term':'biomol trna', 'field':'prop', 'sort' : 'Date Released', 'mindate': 2018, 'maxdate':2019, 'datetype' : 'pdat'},
    #{'db':'protein','term':'70000:90000[molecular weight]', 'retmax':20}
    ]

  def check_uid_uniqeness(result):
    """This function tests if using multiple requests per query continue
    properly"""
    uniq = {}
    dupl_count = {}
    for i in result.uids:
      if i not in uniq:
        uniq[i] = 0
      uniq[i] += 1
      if uniq[i] > 1:
        dupl_count[i] = uniq[i]
    print(len(uniq), result.size())
    if len(uniq) !=  result.size():
      print("!: ERROR: Found  {} duplicate uids. Not expected. Duplicated UIDs:".format(len(dupl_count)))
      for i in dupl_count:
        print(f"{i}\t{dupl_count[i]}")
      return False
    return True

  email = 'gregorybrooks@gmail.com'
  apikey = None
  start = time.time()
  # Loop over examples
  for i in range(len(examples)):
    qrystart = time.time()
    # Init an Esearcher instance
    a = entrezpy.esearch.esearch_analyzer.EsearchAnalyzer()
    es = entrezpy.esearch.esearcher.Esearcher('esearcher', email, apikey, threads=8)
    ## Query E-Utilities and return the default analyzer
    a = es.inquire(examples[i], analyzer=a)

    print(f"+Query {i}\n+++\tParameters: {examples[i]}\n+++\tStatus:", end='')
    ## Test is query has been successful, e.g. no connection or NCBI errors
    if not a.isSuccess():
      print("\tFailed: Response errors")
      return 0
    print("\tResponse OK")
    ## Test is query resulted in no UIDs
    if a.isEmpty():
      print(f"+++\tWARNING: No results for example {i}")
    print(f"+++\tStart dumping results\n+++%%%\t{json.dumps(a.get_result().dump())}")
    #if 'rettype' not in examples[i] and check_uid_uniqeness(a.get_result()):
      #if a.get_result().retmax == a.result.size():
        #print("+++\tRequest OK")
      #else:
        #print("+++\tRequest failed")
      #print(f"+++\tFetched UIDs ({a.result.size()}):\n\t{','.join(str(x) for x in a.get_result().uids)}")
      #print(f"+++\tFollow-up parameters:\n+++\t\t{a.follow_up()}")
    #print(f"+++\tEnd  Results\n+++\tQuery time:{time.time()-qrystart}sec")
  #print(f"+Total time: {time.time()-start} sec")

  fetch_example = {'db': 'pubmed', 'id': [38935428, 38935426], 'retmode': 'text', 'rettype': 'abstract'}
#  ef = entrezpy.efetch.efetcher.Efetcher('efetcher', email, apikey)
#  a = ef.inquire(fetch_example)

  es = entrezpy.esummary.esummarizer.Esummarizer('esummary', email, apikey)
  a = es.inquire(fetch_example)
  print(f"+++\tStart dumping results\n+++%%%\t{json.dumps(a.get_result().dump())}")
  return 0

if __name__ == '__main__':
  main()
