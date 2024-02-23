echo "Aligning the sequences."
echo "1-1"
mkdir -vp "./data/aligned/"
parallel -j 12 \
  mafft --maxiterate 1000 --inputorder --globalpair \
  {} ">" "./data/aligned/"{/.}"_aligned.fasta" \
  ::: ./data/protein_families/*.fasta > ./align.log 2>&1

echo "with paralogs"
mkdir -vp "./data/paralogs_aligned/"
parallel -j 12 \
  mafft --maxiterate 1000 --inputorder --globalpair \
  {} ">" "./data/paralogs_aligned/"{/.}"_aligned.fasta" \
  ::: ./data/protein_families_with_paralogs/*.fasta > ./align.log 2>&1

