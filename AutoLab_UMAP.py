from scripts.main import main

if __name__=="__main__":
    main()

# python main.py -f <file> -r ncbiID -c geneID -td FAS_F -mask 0.5
# python main.py -f /home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile -r ncbiID -c geneID -td FAS_F -mask 0.5
# python AutoLab_UMAP.py -f /home/fabian/Documents/data/eukaryots.phyloprofile -r ncbiID -c geneID -od FAS_F --seed 42 -csv