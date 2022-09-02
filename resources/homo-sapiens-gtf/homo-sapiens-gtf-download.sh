#!/bin/bash

read -p "Around 158M of files will be downloaded. Proceed? [Y/n] " confirmation

if [ "$confirmation" != "n" -a "$confirmation" != "N" ] 
then
	wget http://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/CHECKSUMS
	wget http://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/Homo_sapiens.GRCh38.107.abinitio.gtf.gz
	wget http://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/Homo_sapiens.GRCh38.107.chr.gtf.gz
	wget http://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/Homo_sapiens.GRCh38.107.chr_patch_hapl_scaff.gtf.gz
	wget http://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/Homo_sapiens.GRCh38.107.gtf.gz
	wget http://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/README
fi
