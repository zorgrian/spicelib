v 20070818 1
C 40000 40000 0 0 0 title-B.sym
C 50200 45600 1 0 0 vdc-1.sym
{
T 50900 46250 5 10 1 1 0 0 1
refdes=V1
T 50900 46450 5 10 0 0 0 0 1
device=VOLTAGE_SOURCE
T 50900 46650 5 10 0 0 0 0 1
footprint=none
T 50900 46050 5 10 1 1 0 0 1
value=DC 5V
}
C 46200 45900 1 0 0 idc-1.sym
{
T 46900 46550 5 10 1 1 0 0 1
refdes=I1
T 46900 46750 5 10 0 0 0 0 1
device=CURRENT_SOURCE
T 46900 46950 5 10 0 0 0 0 1
footprint=none
T 46900 46350 5 10 1 1 0 0 1
value=DC 1uA
}
C 49700 46800 1 0 0 gnd-1.sym
N 46500 47100 50500 47100 4
N 50500 47100 50500 46800 4
N 47400 44900 47400 46500 4
N 47400 46500 48200 46500 4
{
T 47900 46600 5 10 1 1 0 0 1
netname=in
}
N 48900 45800 49400 45800 4
{
T 49200 45900 5 10 1 1 0 0 1
netname=out
}
C 47400 44200 1 0 0 cccs-1.sym
{
T 47600 45250 5 10 0 0 0 0 1
device=SPICE-cccs
T 48000 45050 5 10 1 1 0 0 1
refdes=F1
T 47600 45450 5 10 0 0 0 0 1
symversion=0.1
T 48100 44150 5 10 1 0 0 5 1
value=400
}
N 47400 44300 46500 44300 4
N 46500 44300 46500 45900 4
N 48900 44900 48900 46100 4
N 48900 44300 50500 44300 4
N 50500 44300 50500 45600 4
C 48200 46100 1 0 0 $partname
{
T 48900 46750 5 10 1 1 0 0 1
refdes=$test_refdes
}
