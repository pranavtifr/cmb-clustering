#!/bin/sh
for i in {1..2}
do
echo $i
qsub -q workq <<END_OF_PBS
#!/bin/sh
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -k oe
#PBS -q new
#PBS -l nodes=1:ppn=2
#PBS -l mem=200gb
#PBS -m ae
#PBS -M pranav.s@theory.tifr.res.in
# The following line specifies the name of the job
#PBS -N cos_spec_$i
cd \${PBS_O_WORKDIR}
echo \${PBS_O_WORKDIR}
#########################################################################
cd predictions
echo \`hostname\` \`date\` >> ./output.txt
/usr/bin/time -o time ../kmeans.py -N $i >> ./output.txt 2>./errors.txt
echo \`date\` >> ./output.txt
cd \${PBS_O_WORKDIR}
exit 0
END_OF_PBS
done
qstat -a
