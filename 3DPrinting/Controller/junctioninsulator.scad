// joint insulator
$fs = 0.4;
$fa = 1;

id = 4;
length = 22;
od = 6;
base = 2;

difference() {
  cylinder(d=od,h=length);
  translate([0,0,base])
  cylinder(d=id,h=length);
}