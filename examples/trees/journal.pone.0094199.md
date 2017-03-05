# Phylogenies and phyloreferences from *Crowl et al.*, 2014

This test suite includes phylogenies from 
[*Crowl et al.*, 2014](http://dx.doi.org/10.1371/journal.pone.0094199).
This table summarizes the phylogenies and phyloreferences 
currently built.

|            | Plastid ML tree | PPR ML tree | Plastid + PPR ML tree |
| ---------- | --------------- | ----------- | --------------------- |
| Tree image | [URL](http://journals.plos.org/plosone/article/figure/image?size=large&id=10.1371/journal.pone.0094199.g001) | [URL](http://journals.plos.org/plosone/article/figure/image?size=large&id=10.1371/journal.pone.0094199.g002) | [URL](http://journals.plos.org/plosone/article/figure/image?size=large&id=10.1371/journal.pone.0094199.g003) |
| Nexus file | [URL](http://journals.plos.org/plosone/article/file?type=supplementary&id=info:doi/10.1371/journal.pone.0094199.s020) | [URL](http://journals.plos.org/plosone/article/file?type=supplementary&id=info:doi/10.1371/journal.pone.0094199.s021) | [URL](http://journals.plos.org/plosone/article/file?type=supplementary&id=info:doi/10.1371/journal.pone.0094199.s022) |
| Clade C1 | has_Descendant *value* Campanula_latifolia *and* excludes_lineage_to *value* Trachelium_caeruleum | Missing *Campanula latifolia* | has_Descendant *value* Campanula_latifolia *and* excudes_lineage_to *value* Trachelium_caeruleum |
| Clade D | has_Descendant *value* Wahlenbergia_angustifolia *and* excludes_lineage_to *value* Heterochaenia_ensifolia | Missing *Wahlenbergia angustifolia* and *Heterochaenia ensifolia* | has_Descendant *value* Wahlenbergia_angustifolia *and* excludes_lineage_to *value* Heterochaenia_ensifolia |
| Clade G | has_Descendant *value* Campanula_erinus *and* excludes_lineage_to *value* Campanula_drabifolia | has_Child *some* (excludes_lineage_of *value* Campanula_drabifolia) *and* has_Child *value* Campanula_erinus_AC107 | has_Descendant *value* Campanula_erinus *and* excludes_lineage_to *value* Campanula_drabifolia |
| Clade H | Existing phyloreference doesn't resolve, need to use the same trick as clade G.  | Contains both species, but *Campanula pelviformis* has shifted enough that this clade now incorporates almost the entire tree. | has_Child *some* (has_Descendant *value* Campanula_laciniata *and* excludes_lineage_to *value* Campanula_pelviformis) *and* has_Child *some* (has_Descendant *value* Campanula_pelviformis *and* excludes_lineage_to *value* Campanula_laciniata) |
| Clade H by branch | Existing phyloreference doesn't resolve, need to use the same trick as clade G.  | Contains both species, but *Campanula pelviformis* has shifted enough that this clade now incorporates almost the entire tree. | has_Descendant *value* Campanula_laciniata *and* excludes_lineage_to *value* Campanula_pelviformis |
