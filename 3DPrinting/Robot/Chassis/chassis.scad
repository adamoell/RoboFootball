// RoboFootball Chassis
$fs = 0.4;
$fa = 1;

// chassis dims
chassis_width = 100;
chassis_length = 100;
chassis_radius = 5;
chassis_thickness = 2;

// battery dims
batt_width = 13.5; // spec 13
batt_length = 42; // spec 40;
batt_wall = 1.2;
batt_screwhole_length = 10;
batt_screwhole_d = 3;
batt_screwhole_outset = 3;
battchamber_cover_thickness = 2;

// cable management dims
cm_channel = 6; // width of the cable management chambers
cm_wall = 0.8;
cm_height = 10;
bms_chamber_width = 37.3; // measured 36.3
bms_chamber_height = 7.5; // measured 6.5
bms_wall_offset = 5;
bms_cover_radius = 3;
bms_cover_thickness = 2;
charger_hole_d = 8.1; // measured 7.85
charger_cm_hole_d = 4;

// wheel dims
wheel_diameter = 40;
wheel_clearance = 5;
wheel_width = 15;

board_width = 60;
board_length = 70;
board_hole_offset = 5;
board_hole_diam = 3.2;

// motor dims
motor_thickness = 10;
motor_length = 26; // TODO
motor_width = 12;
motor_retainer_thickness = 5;
motor_retainer_vgap = 0.25;
motor_retainer_hole_d = 3; // suitable for M3 ST
motor_retainer_hole_offset = 15;
motor_retainer_clearance = 0.3;
// motor retainer plate dims
retainer_plate_thickness = 2;
motor_wiring_hole_d = 8;

// castor dims
castor_diameter = 18;
castor_wall = 2;
castor_z_offset = (wheel_diameter/2) + (motor_thickness/2);
castor_ball_clearance = 0.3;

// technic dims
front_beam_holes = 9;
rear_beam_holes = 5;
technic_unit = 0.8;
technic_beam_width = technic_unit*10; // 8mm
technic_beam_height = technic_unit*9; // was 7mm now 7.2mm
technic_pitch = technic_unit*10; // 8mm
technic_beam_inner_diameter = technic_unit*6; // was 5.02mm now 4.8mm
technic_beam_outer_diameter = technic_unit*8; // was 6.08mm now 6.4mm
technic_beam_outer_depth = technic_unit; // 0.8mm

// kicker mount
kicker_screwhole_offset = 60; // separation between the screwholes
kicker_hole_d = 3.2;
kicker_width = 18;
kicker_y_inset = 3;

module solid_chassis_profile() {
  r = chassis_radius;
  // main body
  hull() {
    translate([r,chassis_length-r])
      circle(r=r);
    translate([chassis_width-r,chassis_length-r])
      circle(r=r);
    translate([r,wheel_diameter+wheel_clearance+r])
      circle(r=r);
    translate([chassis_width-r,wheel_diameter+wheel_clearance+r])
      circle(r=r);
  }
  // tail between wheels
  hull() {
    translate([wheel_width+wheel_clearance+r,chassis_length-r])
      circle(r=r);
    translate([chassis_width-wheel_width-wheel_clearance-r,chassis_length-r])
      circle(r=r);
    translate([wheel_width+wheel_clearance+r,r])
      circle(r=r);
    translate([chassis_width-wheel_width-wheel_clearance-r,r])
      circle(r=r);
  }
}

module board_mount_holes() {
  translate([(chassis_width-board_width)/2,0]) {
    translate([board_hole_offset, board_hole_offset]) 
      circle(d=board_hole_diam);
    translate([board_width-board_hole_offset, board_hole_offset]) 
      circle(d=board_hole_diam);
    translate([board_hole_offset, board_length-board_hole_offset]) 
      circle(d=board_hole_diam);
    translate([board_width-board_hole_offset, board_length-board_hole_offset]) 
      circle(d=board_hole_diam);
  }
}

module motor_wiring_hole() {
  
  y_off = (wheel_diameter+wheel_clearance) / 2;
  
  translate([chassis_width/2, y_off])
  circle(d=motor_wiring_hole_d);
}

module chassis_profile() {
  difference() {
    solid_chassis_profile();
    board_mount_holes(); // board mount holes
    // kicker mount holes   
    motor_wiring_hole(); // motor wiring hole
  }
  
}


module castor_splitter() {
  splitter_d = 4;
  
  od = castor_diameter+(castor_wall*2);
  
  
  hull() {
    translate([0,(od/2+1),od/2+splitter_d])
      rotate([90,0,0])
        cylinder(d=4, h=od+2);
    translate([0,(od/2+1),-(od/2)+(od*0.3)])
      rotate([90,0,0])
        cylinder(d=4, h=od+2);
  }
  
}

module castor_splitters() {
  castor_splitter();
  rotate([0,0,90])
  castor_splitter();
}

module castor_holder() {
  castor_ratio = 0.35; // was 0.25 but snapped one time in 3 when putting the bearing in
  
  od = castor_diameter+(castor_wall*2);
  // holder
  difference() {
    sphere(d=od) ;
    sphere(d=castor_diameter+(castor_ball_clearance*2));
    zoff = (od/2) - (od*castor_ratio);
    translate([-od/2, -od/2, zoff])
      cube([od, od, od]);
      
    // splitters to allow flex
    castor_splitters();
  } 
}

module solid_castor() {
  od = castor_diameter+(castor_wall*2);
  translate([0,0,castor_z_offset+chassis_thickness-(castor_diameter/2)])
    castor_holder();
  cylinder(d=od, h=castor_z_offset+chassis_thickness-(castor_diameter/2));
}

module castor() {
  od = castor_diameter+(castor_wall*2);
  z = castor_z_offset+chassis_thickness-(castor_diameter/2);
  translate([chassis_width/2,chassis_length-od/2,0])
  difference() {
    solid_castor();
    translate([0,0,z]) 
      castor_splitters();
    translate([0,0,z]) 
      sphere(d=castor_diameter+(castor_ball_clearance*2));
  }
  
}

module motor_retainer() {
  
  
  x = chassis_width - ((wheel_width+wheel_clearance)*2);
  z = motor_thickness - motor_retainer_vgap + chassis_thickness;
  
  translate([wheel_width+wheel_clearance, 0, 0]) {
    difference() {
      cube([x, motor_retainer_thickness, z]);
      translate([motor_retainer_hole_offset, motor_retainer_thickness/2, -1])
        cylinder(d=motor_retainer_hole_d, h=z+2);
      translate([x-motor_retainer_hole_offset, motor_retainer_thickness/2, -1])
        cylinder(d=motor_retainer_hole_d, h=z+2);
    }
  }
  
}

module solid_retainer_plate(x,y,z) {
  stiffener_thickness = 1.2;
  stiffener_depth = retainer_plate_thickness + 2;
  
  // plate
  cube([x,y,z]);
  // edge stiffeners
  difference() {
    cube([x,y,stiffener_depth]);
    translate([stiffener_thickness,stiffener_thickness,0])
    cube([x-(stiffener_thickness*2),y-(stiffener_thickness*2),stiffener_depth+2]);
  }
  // horizontal
  translate([0,(y-stiffener_thickness)/2,0])
    cube([x, stiffener_thickness, stiffener_depth]);
  // vertical
  translate([(x*0.18)-stiffener_thickness/2,0,0])
    cube([stiffener_thickness, y, stiffener_depth]);
  translate([(x*0.39)-stiffener_thickness/2,0,0])
    cube([stiffener_thickness, y, stiffener_depth]);
  translate([(x*0.61)-stiffener_thickness/2,0,0])
    cube([stiffener_thickness, y, stiffener_depth]);
  translate([(x*0.82)-stiffener_thickness/2,0,0])
    cube([stiffener_thickness, y, stiffener_depth]);
  
}

module retainer_plate() {
  motor_retainer_hole_d2 = 5.5;
  
  y_off = (wheel_diameter+wheel_clearance) / 2;
  
  x = chassis_width - ((wheel_width+wheel_clearance)*2);
  y = (motor_retainer_thickness*2) + motor_width + (motor_retainer_clearance*2);
  z = retainer_plate_thickness;
  
  
  //translate([wheel_width+wheel_clearance,y_off-(y/2),0])
    difference() {  
      solid_retainer_plate(x,y,z);
      translate([motor_retainer_hole_offset, motor_retainer_thickness/2, -1]){
        cylinder(d=motor_retainer_hole_d, h=z+2);
        translate([0,0,z+1])
          cylinder(d=motor_retainer_hole_d2, h=z+5);
      }
      translate([x-motor_retainer_hole_offset, motor_retainer_thickness/2, -1]) {
        cylinder(d=motor_retainer_hole_d, h=z+2);
        translate([0,0,z+1])
          cylinder(d=motor_retainer_hole_d2, h=z+5);
      }
      translate([motor_retainer_hole_offset, y-motor_retainer_thickness/2, -1]) {
        cylinder(d=motor_retainer_hole_d, h=z+2);
        translate([0,0,z+1])
          cylinder(d=motor_retainer_hole_d2, h=z+5);
      }
      translate([x-motor_retainer_hole_offset, y-motor_retainer_thickness/2, -1]) {
        cylinder(d=motor_retainer_hole_d, h=z+2);
        translate([0,0,z+1])
          cylinder(d=motor_retainer_hole_d2, h=z+5);
      }
    }
}

module motor_retainers() {
  
  y_off = (wheel_diameter+wheel_clearance) / 2;
  y_out = (motor_width/2) + motor_retainer_clearance;
  
  translate([0,y_off-motor_retainer_thickness-y_out, 0])
    motor_retainer();
  translate([0,y_off+y_out, 0])
    motor_retainer();
}

module solid_battchamber_profile() {
  w = batt_width + batt_wall*2;
  r = chassis_radius;
  // main body
  hull() {
    translate([r,chassis_length-r])
      circle(r=r);
    translate([r,chassis_length-1])
      square([w-r, 1]);
    translate([r,wheel_diameter+wheel_clearance+r])
      circle(r=r);
    translate([r,wheel_diameter+wheel_clearance])
      square([w-r, 1]);
  }
  
  hull() {
    translate([chassis_width-r,chassis_length-r])
      circle(r=r);
    translate([chassis_width-w,chassis_length-1])
      square([w-r, 1]);
    translate([chassis_width-r,wheel_diameter+wheel_clearance+r])
      circle(r=r);
    translate([chassis_width-w,wheel_diameter+wheel_clearance])
      square([w-r, 1]);
  }
}

module battchamber_profile() {
  w = batt_width + batt_wall*2;
  // this y is the beginning of the hollow chamber (ie nearest wheel well)
  y = (((chassis_length) - (wheel_diameter+wheel_clearance)) / 2) + (wheel_diameter+wheel_clearance) - (batt_length/2);
  difference() {
    solid_battchamber_profile();  
    translate([w-batt_width-batt_wall,y])
      square([batt_width, batt_length]);
    translate([chassis_width-w+batt_wall,y])
      square([batt_width, batt_length]);
  }
  
}



module cable_mgmt_profile() {
  
  
  // this y1 is the beginning of the batt chamber hollow (ie nearest wheel well)
  y1 = (((chassis_length) - (wheel_diameter+wheel_clearance)) / 2) + (wheel_diameter+wheel_clearance) - (batt_length/2);
  // this w is the width of the battery chamber
  w = batt_width + batt_wall*2;
  //y2 is the y pos of the end of the motor chamber
  y2 = ((wheel_diameter+wheel_clearance) / 2) + ((motor_width/2) + motor_retainer_clearance) + motor_retainer_thickness;
  
  x = chassis_width - (w*2) + 0.2;
  y = cm_channel + (cm_wall*2);
  
  bms_x = bms_chamber_width+(cm_wall*2);
  bms_y = bms_chamber_height+(cm_wall*2);
  
  
  difference() {
    union() {
      // connections to cells
      translate([w-0.1,y1])
        square([x,y]);
      
      // connection to motor chamber
      translate([(chassis_width-y)/2,y2-0.1]) 
        square([y,y1-y2+0.2]);
      
      // BMS chamber
      translate([(chassis_width-bms_x)/2,y1+y-cm_wall])
        square([bms_x, bms_y]);
      
      // cover for bms
      bms_cover_profile(batt_screwhole_d);
    }
    // cutout - cells route
    translate([w-1.1,y1+cm_wall])
      square([x+2,y-(cm_wall*2)]);
    // cutout - motor_chamber route
    translate([(chassis_width-y)/2+cm_wall,y2-0.2]) 
      square([y-(cm_wall*2),y1-y2+0.3+cm_wall]);
    // cutout - bms chamber
    translate([(chassis_width-bms_x)/2+cm_wall,y1+y])
      square([bms_x-(cm_wall*2), bms_y-(cm_wall*2)]);
    translate([(chassis_width-bms_x)/2+cm_wall+bms_wall_offset,y1+y-cm_wall-cm_channel-(bms_cover_radius*2)])
      square([bms_x-(cm_wall*2)-(bms_wall_offset*2), bms_y-(cm_wall)+(bms_cover_radius*4)+cm_channel]);
  }
  
  
  
}


module solid_chassis() {
  // the chassis
  linear_extrude(height=chassis_thickness)
    chassis_profile();
  // 13400 battery chambers
  linear_extrude(height=batt_width+chassis_thickness) {
    battchamber_profile();
  }
  // cable management
  linear_extrude(height=cm_height+chassis_thickness) {
    cable_mgmt_profile();
  }
  castor(); // rear castor
  motor_retainers();
  
  // technic beam - rear
  translate([(chassis_width-(rear_beam_holes*technic_pitch))/2,0,0]) 
    solid_technic_beam(rear_beam_holes);
  // technic beam - front
  w = chassis_width - (batt_width*2) - (batt_wall*4);
  translate([(chassis_width-w)/2,chassis_length-technic_beam_width,0]) 
    cube([w, technic_beam_width, technic_beam_height]);
}

module battchamber_cover() {
  
  linear_extrude(height=battchamber_cover_thickness)
  difference() {
    solid_battchamber_profile();
    // this y1 is the beginning of the batt chamber hollow (ie nearest wheel well)
    y1 = (((chassis_length) - (wheel_diameter+wheel_clearance)) / 2) + (wheel_diameter+wheel_clearance) - (batt_length/2);
    // this y2 is the end of the batt chamber hollow
    y2 = y1 + batt_length;
    // this w is the battery chamber width
    w = batt_width + batt_wall*2;
    
    // left
    translate([w/2, y1-batt_screwhole_outset])
      circle(d=batt_screwhole_d+0.2);
    translate([w/2, y2+batt_screwhole_outset])
      circle(d=batt_screwhole_d+0.2);
    // right
    translate([chassis_width-(w/2), y1-batt_screwhole_outset])
      circle(d=batt_screwhole_d+0.2);
    translate([chassis_width-(w/2), y2+batt_screwhole_outset])
      circle(d=batt_screwhole_d+0.2);
  }
}



module cm_holes() {
  // this y1 is the beginning of the batt chamber hollow (ie nearest wheel well)
  y1 = (((chassis_length) - (wheel_diameter+wheel_clearance)) / 2) + (wheel_diameter+wheel_clearance) - (batt_length/2);
  //y2 is the y pos of the end of the motor chamber
  y2 = ((wheel_diameter+wheel_clearance) / 2) + ((motor_width/2) + motor_retainer_clearance) + motor_retainer_thickness;
  
  batt_hole_length = chassis_width-(cm_wall*2)-0.2;
  
  translate([cm_wall+0.1,y1+cm_wall+(cm_channel/2),chassis_thickness+(cm_channel/2)])
    rotate([0,90,0])
      cylinder(d=cm_channel, h=batt_hole_length);
  
  translate([chassis_width/2,y2-motor_retainer_thickness-1,chassis_thickness+(cm_channel/2)])
    rotate([-90,0,0])
      cylinder(d=cm_channel, h=motor_retainer_thickness+2);
}

module batt_screwholes() {
  
  
  // this y1 is the beginning of the batt chamber hollow (ie nearest wheel well)
  y1 = (((chassis_length) - (wheel_diameter+wheel_clearance)) / 2) + (wheel_diameter+wheel_clearance) - (batt_length/2);
  // this y2 is the end of the batt chamber hollow
  y2 = y1 + batt_length;
  // this w is the battery chamber width
  w = batt_width + batt_wall*2;
  
  // left
  translate([w/2, y1-batt_screwhole_outset, batt_width+chassis_thickness-batt_screwhole_length+0.001])
    cylinder(d=batt_screwhole_d, h=batt_screwhole_length);
  translate([w/2, y2+batt_screwhole_outset, batt_width+chassis_thickness-batt_screwhole_length+0.001])
    cylinder(d=batt_screwhole_d, h=batt_screwhole_length);
  // right
  translate([chassis_width-(w/2), y1-batt_screwhole_outset, batt_width+chassis_thickness-batt_screwhole_length+0.001])
    cylinder(d=batt_screwhole_d, h=batt_screwhole_length);
  translate([chassis_width-(w/2), y2+batt_screwhole_outset, batt_width+chassis_thickness-batt_screwhole_length+0.001])
    cylinder(d=batt_screwhole_d, h=batt_screwhole_length);
}

module bms_cover_profile(hole_radius) {
  // this y1 is the beginning of the batt chamber hollow (ie nearest wheel well)
  y1 = (((chassis_length) - (wheel_diameter+wheel_clearance)) / 2) + (wheel_diameter+wheel_clearance) - (batt_length/2);
  // this y2 is the tops edge of the BMS
  y2 = y1 + (cm_wall*3) + cm_channel + bms_chamber_height;
  x_off = (bms_chamber_width/2) + cm_wall - bms_cover_radius;
  difference() {
    hull() {
      translate([(chassis_width/2) + x_off, y2+bms_cover_radius])
        circle(r=bms_cover_radius);
      translate([(chassis_width/2) - x_off, y2+bms_cover_radius])
        circle(r=bms_cover_radius);
      translate([(chassis_width/2) + x_off, y1-bms_cover_radius])
        circle(r=bms_cover_radius);
      translate([(chassis_width/2) - x_off, y1-bms_cover_radius])
        circle(r=bms_cover_radius);
    }
    translate([(chassis_width/2) + x_off, y2+bms_cover_radius])
        circle(d=hole_radius);
      translate([(chassis_width/2) - x_off, y2+bms_cover_radius])
        circle(d=hole_radius);
      translate([(chassis_width/2) + x_off, y1-bms_cover_radius])
        circle(d=hole_radius);
      translate([(chassis_width/2) - x_off, y1-bms_cover_radius])
        circle(d=hole_radius);
  }
}

module bms_cover() {
  linear_extrude(height=bms_cover_thickness)
    bms_cover_profile(batt_screwhole_d+0.2);
}

module charger_hole() {  
  // this y1 is the beginning of the batt chamber hollow (ie nearest wheel well)
  y1 = (((chassis_length) - (wheel_diameter+wheel_clearance)) / 2) + (wheel_diameter+wheel_clearance) - (batt_length/2);
  // y2 is the y pos of the end of the motor chamber
  y2 = ((wheel_diameter+wheel_clearance) / 2) + ((motor_width/2) + motor_retainer_clearance) + motor_retainer_thickness;
  // y3 is the beginning of the covered BMS chamber
  y3 = y1-(bms_cover_radius*2);
  hole_offset = (y3-y2)/2;
  y = hole_offset + y2;
  x = (chassis_width/2) + (cm_channel/2) + cm_wall + hole_offset;
  
  // the hole for the barrel socket
  translate([x,y,-1])
    cylinder(d=charger_hole_d,h=chassis_thickness+2);
    
  translate([chassis_width/2,y,-1]) 
    cylinder(d=cm_channel,h=chassis_thickness+2);

}

module kicker_screwholes() {
  x = chassis_width / 2;
  y = chassis_length - (kicker_width/2) - kicker_y_inset;
  
  translate([x-(kicker_screwhole_offset/2),y,-1])
    cylinder(d=kicker_hole_d, h=chassis_thickness+2);
  translate([x+(kicker_screwhole_offset/2),y,-1])
    cylinder(d=kicker_hole_d, h=chassis_thickness+2);
}

module chassis() {
  difference() {
    solid_chassis();
    // screwholes for battery cover plates
    batt_screwholes();
    // cable management holes
    cm_holes();
    // rear technic beam
    translate([(chassis_width-(rear_beam_holes*technic_pitch))/2,0,0]) 
      technic_beamholes(rear_beam_holes);
    // technic beam - front
    translate([(chassis_width-(front_beam_holes*technic_pitch))/2,chassis_length-technic_beam_width,0]) 
      technic_beamholes(front_beam_holes);
      
    // hole for barrel jack for charging
    charger_hole();
    
    // screwholes for attaching the kicker
    kicker_screwholes();
  }
  
}


module technic_beamhole() {
  translate([0,0,technic_beam_height/2])
    rotate([-90,0,0]) {
      cylinder(d=technic_beam_inner_diameter,h=technic_beam_width);
      translate([0,0,-0.001])
        cylinder(d=technic_beam_outer_diameter,h=technic_beam_outer_depth+0.001);
      translate([0,0,technic_beam_width-technic_beam_outer_depth])
        cylinder(d=technic_beam_outer_diameter,h=technic_beam_outer_depth+0.001);
    }
}
module technic_beamholes(numholes) {
  for (i=[0:numholes-1]) {
    translate([(i+0.5)*technic_pitch,0,0])
    technic_beamhole();
  }
}

module solid_technic_beam(numholes) {
  cube([numholes*technic_pitch, technic_beam_width, technic_beam_height]);
}

module technic_beam(numholes) {
  width = numholes * technic_pitch;
  difference() {
    union() {
      translate([technic_pitch/2,0,0]) 
        solid_technic_beam(numholes-1);
      translate([technic_pitch/2,0,technic_beam_height/2])
        rotate([-90,0,0]) 
          cylinder(d=technic_beam_height, h=technic_beam_width);
      translate([technic_pitch*(numholes-0.5),0,technic_beam_height/2])
        rotate([-90,0,0]) 
          cylinder(d=technic_beam_height, h=technic_beam_width);
    }
    technic_beamholes(numholes);
  }
} 


chassis(); // the main chassis
//retainer_plate(); // the plate that holds the motors
//bms_cover(); // cover plate for the BMS chamber
//battchamber_cover(); // cover plates for the battery chambers

//technic_beam(5);


 