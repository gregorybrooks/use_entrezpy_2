from datetime import time
import time

import entrezpy.conduit

start = time.time()
c = entrezpy.conduit.Conduit('gregorybrooks@gmail.com')

fetch_ppl = c.new_pipeline()
sid = fetch_ppl.add_search({'db':'pubmed',
                            'term':'breast[All Fields]',
                            'rettype':'count'})

sid = fetch_ppl.add_summary(dependency=sid)
analyzer = c.run(fetch_ppl)
for uid, summary in analyzer.get_result().summaries.items():
    print("{}\t{}".format(uid, summary.get('caption'),summary.get('sourcedb')))
print("Threads: {}\tSummaries: {}\nDurations: {} [s]".format(c.threads,
                                                len(analyzer.result.summaries),
                                                 time.time()-start))


#fetch_ppl.add_fetch({'retmode':'text', 'rettype':'abstract'}, dependency=sid)
#c.run(fetch_ppl)
