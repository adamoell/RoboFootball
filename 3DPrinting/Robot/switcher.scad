$fs = 0.4;
$fa = 1;

x1 = 0;
x2 = 4;
x3 = 10;
x4 = 28;

y1 = 0;
y2 = 2;
y3 = 4;

skin_thickness = 0.6;
switcher_thickness = 5;
holder_d = 18;

module main_profile() {
  a = [x1,y1];
  b = [x1,y2];
  c = [x2,y3];
  d = [x2,y2];
  e = [x3,y2];
  f = [x3,y3];
  g = [x4,y2];
  h = [x4,y1];
  
  polygon([
    a,b,c,d,e,f,g,h
  ]);
}

module edge_profile() {
  a = [x1,y1];
  b = [x1,y2];
  c = [x2,y3];
  d = [x2,y2];
  e = [x3,y2];
  f = [x3,y3];
  g = [x4,y2];
  h = [x4,y1];
  
  polygon([
    a,b,c,f,g,h
  ]);
}

module body() {
  translate([-x4 - holder_d/2+2,switcher_thickness/2,0])
  rotate([90,0,0]) {
    linear_extrude(height=skin_thickness)
      edge_profile();
    translate([0,0,switcher_thickness-skin_thickness])
      linear_extrude(height=skin_thickness)
        edge_profile();
    linear_extrude(height=switcher_thickness)
      main_profile();
  }
  cylinder(d=holder_d, h=y2);
}

body();