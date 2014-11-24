import russe.relatedness as rt
from russe.common import generate_synonyms
from time import time

rt_dir = "/home/sasha/russe/data/rt/"
syn_fpath = rt_dir + "synonyms.xml"
entry_fpath = rt_dir + "text_entry.xml"
concepts_fpath = rt_dir + "concepts.xml"
relations_fpath = rt_dir + "relations.xml"
voc_fpath = rt_dir + "fb-voc-5000.csv"
output_fpath = rt_dir + "rt.csv"
output_syn_fpath = output_fpath + ".syn"
output_rel_fpath = output_fpath + ".rel"
output_cohypo_fpath = output_fpath + ".cohypo"
tic = time()

# syn = rt.load_syn(syn_fpath)
# entries = rt.load_entries(entry_fpath)
# selected_words = rt.load_voc(voc_fpath)
# concepts = rt.load_concepts(concepts_fpath)
# relations = rt.load_relations(relations_fpath)

# synsets = rt.generate_synsets(syn, entries, concepts, selected_words)
# generate_synonyms(synsets, output_syn_fpath, symmetric=True)    
# rt.generate_relations(relations, entries, synsets, output_rel_fpath, symmetric=False)
#     #rt.generate_cohypo(relations, entries, synsets, concepts, output_cohypo_fpath)
# rt.mix_filter_relations(output_syn_fpath, output_rel_fpath, output_cohypo_fpath, output_fpath, selected_words)


selected_words = rt.load_voc(voc_fpath)
rt.mix_filter_relations(output_syn_fpath, output_rel_fpath, output_cohypo_fpath, output_fpath, selected_words)


print time() - tic, "sec."