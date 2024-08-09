// RoboFootball servo mount
$fs = 0.2;
$fa = 1;

// servo geometry
motor_block_length = 23;
motor_overall_length = 32;
motor_depth_to_retainer = 19.5;
motor_width = 12;
motor_clearance = 0.2;
motor_base_to_shaft = 32;
motor_protruding_from_mount = motor_base_to_shaft - motor_depth_to_retainer;
motor_hole_offset = 27.7;
motor_hole_outset = (motor_overall_length - motor_hole_offset) / 2;
motor_hole_d = 3.2;

// servo mount geometry
mount_x = 80;
mount_y = 42;
mount_z = 18;
mount_base_thickness = 3;
mount_holder_thickness = 3;
mount_brace = 4;
mount_hole_d = 3.2; 

// kicker geometry
kicker_spline_depth = 3;
kicker_thickness = 4;
kicker_d1 = 10;
kicker_d2 = 8;
kicker_d3 = 6;
kicker_screwhole_d = 2;
kicker_boot_screwhole = 3.2;

module mount_profile() {
  x_offset_holder = (mount_x/2) - motor_protruding_from_mount;
  square([mount_x, mount_base_thickness]);
  translate([x_offset_holder-mount_holder_thickness, 0])
    square([mount_holder_thickness, mount_y]);
  // chamfer
  x1 = x_offset_holder - mount_holder_thickness - mount_brace;
  x2 = x1 + mount_brace;
  x3 = x2 + mount_holder_thickness;
  x4 = x3 + mount_brace;
  y1 = mount_base_thickness - 0.001;
  y2 = y1 + mount_brace;
  polygon([
    [x1,y1],
    [x2,y2],
    [x3,y2],
    [x4,y1]
  ]);
}

module solid_mount() {
  linear_extrude(height=mount_z)
    mount_profile();
}

module motor_slot() {
  x_offset_holder = (mount_x/2) - motor_protruding_from_mount;
  motor_slot_length = motor_block_length + (motor_clearance*2);
  motor_slot_width = motor_width + (motor_clearance*2);
  y_offset = 4;
  motor_hole_outset = (motor_overall_length - motor_hole_offset) / 2;
  
  
  translate([x_offset_holder-mount_holder_thickness-1,(mount_y-motor_slot_length)/2+y_offset,(mount_z-motor_slot_width)/2]) {
    cube([mount_holder_thickness+2, motor_slot_length, motor_slot_width]);
    
    // screw holes
    translate([0,-motor_hole_outset,motor_slot_width/2])
      rotate([0,90,0])
        cylinder(d=motor_hole_d, h=mount_holder_thickness+2);
    translate([0,motor_hole_offset-motor_hole_outset,motor_slot_width/2])
      rotate([0,90,0])
        cylinder(d=motor_hole_d, h=mount_holder_thickness+2);
  }
}

module base_screwhole() {
  translate([0,-1,mount_z/2])
    rotate([-90,0,0])
      cylinder(d=mount_hole_d, h=mount_base_thickness+2);
}

module base_screwholes() {
  inset = 10; // they end up being 60mm apart
  translate([inset,0,0])
    base_screwhole();
  translate([mount_x-inset,0,0])
    base_screwhole();
}

module mount() {
  difference() {
    solid_mount();
    // motor slot and screwholes
    motor_slot(); 
  
    // base screwholes
    base_screwholes();
  }
  
}

// ***************************************************
// Kicker
// ***************************************************
module spline_profile() {
    spline_od = 5.3; // 4.8 measured
    spline_tooth_depth = 0.3; // 0.25;
    
    outradius = spline_od/2; // the outside of the 'zigzags' that hold the rubber band
    inradius = outradius - spline_tooth_depth; // the inside of the 'zigzags' that hold the rubber band
    points = 21; // the number of 'zigzags'
    steps = points * 2;
    
    function getangle(point, steps) = point * (360/steps);
    function getradius(point) = ((point % 2) == 0) ? outradius : inradius;
    function getx(point, steps) = getradius(point) * cos(getangle(point, steps));
    function gety(point, steps) = getradius(point) * sin(getangle(point, steps));

    // the zigzag outline
    polypoints = [for (i=[0:1:steps]) [getx(i, steps), gety(i, steps)]  ];
    polygon(polypoints); // zigzaggy outline

//    linear_extrude(height=wheelwidth) {
//        difference() { // cutout for shaft
//            union() {
//                circle(r=hubradius); // the hub
//                // spokes
//                for (i=[0:1:spokes-1]) {
//                    angle = i * (360/spokes);
//                    rotate([0,0,angle])
//                        translate([0,inradius/2,0])
//                        square(size=[spokewidth,inradius], center=true);
//                }
//                difference() {    
//                    polygon(polypoints); // zigzaggy outline
//                    circle(r=rimradius); // cutout for open wheel
//                }
//            }
//            //tt_shaft(); // cutout for shaft
//        }
//    }
    
    
}

module leg() {
  thigh_length = 35;
  thigh_off = sqrt((thigh_length*thigh_length)/2);
  shin_length = 20;
  echo(thigh_off);
  
  hull() {
    cylinder(d=kicker_d1, h=kicker_thickness);
    translate([thigh_off,-thigh_off,0])
      cylinder(d=kicker_d2, h=kicker_thickness);
  }
  difference() {
    hull() {
      translate([thigh_off,-thigh_off,0])
        cylinder(d=kicker_d2, h=kicker_thickness);
      translate([thigh_off,-thigh_off-shin_length,0])
        difference() {
          cylinder(d=kicker_d3, h=kicker_thickness);
          
        }
    }
    translate([thigh_off,-thigh_off-shin_length,-1]) 
      cylinder(d=kicker_boot_screwhole, h=kicker_thickness+2);
  }
}
module kicker() {
//  kicker_spline_depth = 3;
//kicker_thickness = 4;
//kicker_d1 = 8;
//kicker_d2 = 4;
//kicker_screwhole_d = 2;
  offset = 12;

  difference() {
    leg();
    translate([0,0,kicker_thickness-kicker_spline_depth])
    linear_extrude(height=kicker_spline_depth+0.001)
      spline_profile();
    // screwhole
    translate([0,0,-1])
    cylinder(d=kicker_screwhole_d, h=kicker_thickness+2);
  }
  
}

module boot() {
  boot_d = 10;
  ball_d = 62+(boot_d/2); // TODO
  boot_angle = 120;
  
  rotate_extrude(angle=boot_angle/2)
    translate([ball_d/2,0])
      circle(d=boot_d);
  rotate_extrude(angle=-boot_angle/2)
    translate([ball_d/2,0])
      circle(d=boot_d);
      
  rotate([0,0,boot_angle/2])
    translate([ball_d/2,0,0])
      sphere(d=boot_d);
  rotate([0,0,-boot_angle/2])
    translate([ball_d/2,0,0])
      sphere(d=boot_d);
  
  holder_clearance = 0.2;
  holder_x = boot_d * 1.25;
  holder_leg_thickness = 1;
  holder_y = kicker_thickness + (holder_leg_thickness*2) + (holder_clearance*2);
  holder_z = boot_d;
  holder_gap = kicker_thickness + (holder_clearance*2);
  
  translate([ball_d/2, -holder_y/2, -holder_z/2])
  difference() {
    cube([holder_x, holder_y, holder_z]);
    translate([-1,(holder_y-holder_gap)/2,-1])
      cube([holder_x + 2, holder_gap, holder_z+2]);
    translate([holder_x-(kicker_boot_screwhole*1),-1,holder_z/2])
      rotate([-90,0,0])
        cylinder(d=kicker_boot_screwhole, h=holder_y+2);
  }
  
}

//mount();
kicker(); 
//boot();