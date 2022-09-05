#!/bin/bash

read -p "Around 3.1G of files will be downloaded. Proceed? [Y/n] " confirmation

if [ "$confirmation" != "n" -a "$confirmation" != "N" ] 
then
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.1.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.1.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.2.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.2.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.3.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.3.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.4.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.4.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.5.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.5.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.6.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.6.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.7.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.7.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.8.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.8.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.9.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.9.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.10.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.10.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.11.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.11.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.12.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.12.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.13.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.13.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.14.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.14.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.15.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.15.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.16.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.16.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.17.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.17.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.18.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.18.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.19.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.19.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.20.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.20.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.21.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.21.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.22.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.22.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.MT.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.MT.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.X.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.X.fa.gz
	
	wget http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.Y.fa.gz
	gzip -d Homo_sapiens.GRCh38.dna.chromosome.Y.fa.gz
fi
