// Goal
$fs = 0.4;
$fa = 1;

goal_mouth_width = 250;
goal_mouth_height = 120;
bezel_width = 20;
bezel_thickness = 2;
liner_thickness = 2;
liner_depth = 38; //3x2 CLS is 63mmx38mm
surround_height = 63;

bezel_x = goal_mouth_width + (bezel_width*2);
bezel_y = goal_mouth_height + (bezel_width);

liner_x = goal_mouth_width + (liner_thickness*2);
liner_y = goal_mouth_height + (liner_thickness);

joiner_wall = 1;
joiner_slop = 0.2;
joiner_length = 40;
  
module solid_goal() {
  // bezel
  cube([bezel_x, bezel_y, bezel_thickness]);
  // liner 
  translate([bezel_width-liner_thickness, 0, 0])
    cube([liner_x, liner_y, liner_depth+bezel_thickness]);
  
}

module goal_mouth() {
  translate([bezel_width,-1,-1])
  cube([goal_mouth_width, goal_mouth_height+1, liner_depth+bezel_thickness+2]);
}

module screwholes() {
  screwhole_d = 3.2;
  screwhole_offset = 15;
  
  translate([0,screwhole_offset, (liner_depth/2)+bezel_thickness])
    rotate([-90,0,-90])
      cylinder(d=screwhole_d, h=bezel_x);
  translate([0,surround_height-screwhole_offset, (liner_depth/2)+bezel_thickness])
    rotate([-90,0,-90])
      cylinder(d=screwhole_d, h=bezel_x);
}

module goal() {
  difference() {
    solid_goal();  
    goal_mouth();
    screwholes();
  }
}

module goal_r() {
  difference() {
    goal();
    translate([bezel_x/2, -1, -1])
      cube([bezel_x, bezel_y+2, liner_depth+4]);
  }
  
}

module goal_l() {
  difference() {
    goal();
    translate([-bezel_x+(bezel_x/2), -1, -1])
      cube([bezel_x, bezel_y+2, liner_depth+4]);
  }
  
}

module joiner_cutout_profile() {
  // holder for the bezel
  bh_x = bezel_width + (joiner_slop*2);
  bh_y = bezel_thickness + (joiner_slop*2);
  square([bh_x, bh_y]);
  
  // holder for the liner
  lh_x = liner_thickness + (joiner_slop*2);
  lh_y = liner_depth + bezel_thickness+ (joiner_slop*2);
  square([lh_x, lh_y]);
}

module joiner_profile() {
  joiner_wall = 1;
  joiner_slop = 0.2;
  
  // holder for the bezel
  bh_x = bezel_width + (joiner_wall*2) + (joiner_slop*2);
  bh_y = bezel_thickness + (joiner_wall*2) + (joiner_slop*2);
  square([bh_x, bh_y]);
  
  // holder for the liner
  lh_x = liner_thickness + (joiner_wall*2) + (joiner_slop*2);
  lh_y = liner_depth + bezel_thickness + (joiner_wall*2) + (joiner_slop*2);
  square([lh_x, lh_y]);
}

module joiner() {
  linear_extrude(height=joiner_length)
  difference() {
    joiner_profile();
    translate([joiner_wall, joiner_wall])
      joiner_cutout_profile();
  }
}

//goal_l();
//goal_r();
joiner();