echo "Computing the consensus trees."
mkdir -vp "./data/all_consensus/"
cat ./data/family_trees/*bestTree > ./data/all_consensus/all_trees.nw
../raxml-ng --consense MR --tree ./data/all_consensus/all_trees.nw --prefix ./data/all_consensus/consensus_MR
../raxml-ng --consense MRE --tree ./data/all_consensus/all_trees.nw --prefix ./data/all_consensus/consensus_MRE

mkdir -vp "./data/filtered_consensus/"
../raxml-ng --consense MR --tree ./data/filtered_consensus/filtered_trees.nw --prefix ./data/filtered_consensus/consensus_MR
../raxml-ng --consense MRE --tree ./data/filtered_consensus/filtered_trees_trees.nw --prefix ./data/filtered_consensus/consensus_MRE
