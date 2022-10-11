./reset-gene-panel.sh
python3 random-gene-panel-generator.py
echo "Extracting gene transcripts..."
gffread -w ../resources/gene-panel/transcripts.fa -g ../resources/homo-sapiens-fasta/genome.fa ../resources/gene-panel/gene_panel.gtf
echo "Transcripts extracted"
python3 gene_mapping.py
python3 read-generator.py
python3 read_classification_data.py