$fs = 0.4;
$fa = 1;

// robofootball canopy
board_x = 60;
board_y = 70;
hole_spacing_x = 50;
hole_spacing_y = 60;
radius = 8;
base_thickness = 0.4;
wall_thickness = 1;
canopy_thickness = 10;
screwhole_d = 3.2;
screwhole_reinforce_d = 6;
screwhole_reinforce_h = 4;

module base_profile(rad) {
  hull() {
    circle(r=rad);
    translate([hole_spacing_x,0])
      circle(r=rad);
    translate([0, hole_spacing_y])
      circle(r=rad);
    translate([hole_spacing_x,hole_spacing_y])
      circle(r=rad);
  }
}

module screwholes_reinforce() {
  translate([0,0,0])
    cylinder(d=screwhole_reinforce_d, h=screwhole_reinforce_h);
  translate([hole_spacing_x,0,0])
    cylinder(d=screwhole_reinforce_d, h=screwhole_reinforce_h);
  translate([0,hole_spacing_y,0])
    cylinder(d=screwhole_reinforce_d, h=screwhole_reinforce_h);
  translate([hole_spacing_x,hole_spacing_y,0])
    cylinder(d=screwhole_reinforce_d, h=screwhole_reinforce_h);
}

module solid_canopy() {
  difference() {
    linear_extrude(height=canopy_thickness)
      base_profile(rad=radius);
    translate([0,0,base_thickness])
      linear_extrude(height=canopy_thickness)
        base_profile(rad=radius-wall_thickness);
  }
  screwholes_reinforce();
}

module screwholes() {
  translate([0,0,-1])
    cylinder(d=screwhole_d, h=canopy_thickness+2);
  translate([hole_spacing_x,0,-1])
    cylinder(d=screwhole_d, h=canopy_thickness+2);
  translate([0,hole_spacing_y,-1])
    cylinder(d=screwhole_d, h=canopy_thickness+2);
  translate([hole_spacing_x,hole_spacing_y,-1])
    cylinder(d=screwhole_d, h=canopy_thickness+2);
}



module canopy() {
  difference() {
    solid_canopy();
    screwholes();
  }
}

canopy();