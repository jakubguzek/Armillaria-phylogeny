echo "Inferring the ML trees with raxml-ng."
echo "1-1"
mkdir -vp "./data/family_trees/"
parallel -j 4 \
  ../raxml-ng --threads 4 --all --msa {} --model LG+G8+F --bs-trees 100 --prefix "./data/family_trees/"{/.} \
  ::: ./data/aligned/*.fasta

echo 'with paralogs'
mkdir -vp "./data/paralogs_family_trees/"
parallel -j 4 \
  ../raxml-ng --threads 4 --all --msa {} --model LG+G8+F --bs-trees 100 --prefix "./data/paralogs_family_trees/"{/.} \
  ::: ./data/paralogs_aligned/*.fasta
