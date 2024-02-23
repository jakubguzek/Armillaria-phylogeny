echo "Computing the supertree."
echo '1-1'
mkdir -vp "./data/all_supertree/"
cat ./data/family_trees/*bestTree | \
  sed "s/\(Armillaria_[a-z]\+-*[a-z]\+\)-[A-Z0-9]\+.[0-9]/\1/g" | sed "s/-/_/g" > \
  ./data/all_supertree/all_trees.nw
../duptree -i ./data/all_supertree/all_trees.nw -o ./data/all_supertree/supertree.nw

echo 'filtered'
mkdir -vp "./data/filtered_supertree/"
sed "s/\(Armillaria_[a-z]\+-*[a-z]\+\)-[A-Z0-9]\+.[0-9]/\1/g" ./data/filtered_supertree/filtered_trees.nw | sed "s/-/_/g" > \
  ./data/filtered_supertree/filtered_trees.nw.tmp
../duptree -i ./data/all_supertree/filtered_trees.nw.tmp -o ./data/all_supertree/supertree.nw

echo 'with paralogs'
mkdir -vp "./data/paralogs_all_supertree/"
cat ./data/family_trees/*bestTree ./data/paralogs_family_trees/*bestTree | \
  sed "s/\(Armillaria_[a-z]\+-*[a-z]\+\)-[A-Z0-9]\+.[0-9]/\1/g" | sed "s/-/_/g" > \
  ./data/paralogs_all_supertree/all_trees.nw
../duptree -i ./data/paralogs_all_supertree/all_trees.nw -o ./data/paralogs_all_supertree/supertree.nw
