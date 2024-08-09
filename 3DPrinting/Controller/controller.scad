// RoboFootball Controller
$fs = 0.4;
$fa = 1;

// Box Dimensions
box_height = 60;
box_width = 140;
box_depth = 30;
box_wall = 1.2;
box_top = 1.2;

// Thumbstick Dimensions
thumbstick_hole_d = 29;
thumbstick_standoff_length = 12;
thumbstick_mounthole_offset_x = 26.5; // was 25.5
thumbstick_mounthole_offset_y = 20;
thumbstick_pillar_d = 45;
thumbstick_x = box_width-(box_height/2);
thumbstick_y = box_height/2;
thumbstick_screw_d = 3;
thumbstick_easement = 5;
thumbstick_hole_y_offset = 1; // was 1
thumbstick_hole_x_offset = 0.25;

// Switch Dimensions
switch_width = 12.6; // width of the switch: measured 11.56, was 12.0
switch_length = 19.2; // length of the switch: measured 18.7

// Display Dimensions
display_width = 27;
display_slot_width = 3.2;
display_height = 12;

// boost/charge board geometry
esp_clearance = 0.3;
esp_plinth_depth = 1;
esp_wall_thickness = 1;
charge_width = 24;
charge_length = 18;
charge_clearance = 0.3;
charge_plinth_depth = 1;
charge_wall_thickness = 1;
charge_wall_depth = 1;
charge_usb_height = 6 + esp_plinth_depth;
charge_usb_hole_width = 14;
charge_x_off = 22;

// esp32 geometry
esp32_length = 56;
esp32_width = 29;
esp32_wall_depth = 3;
esp32_plinth_depth = 5;
esp_x_off = 16;
esp_y_off = 4;

// 13400 battery geometry

// lid
lid_screwhole_d = 3;
lid_screwhole_dist = 65;
lid_screwhole_edge = 3;
lid_thickness = 1;
lid_slop = 0.2;
lid_rim_thickness = 1.2;
lid_rim_depth = 6;

module solid_box() {
  hull() {
    translate([box_height/2, box_height/2, 0])
      cylinder(d=box_height, h=box_depth);
    translate([box_width-(box_height/2), box_height/2, 0])
      cylinder(d=box_height, h=box_depth);
  }
}



module thumbstick_standoff_mountholes() {
  translate([-(thumbstick_mounthole_offset_x/2),-(thumbstick_mounthole_offset_y/2),box_top])
    cylinder(d=thumbstick_screw_d, h=thumbstick_standoff_length+1);
  translate([-(thumbstick_mounthole_offset_x/2),(thumbstick_mounthole_offset_y/2),box_top])
    cylinder(d=thumbstick_screw_d, h=thumbstick_standoff_length+1);
  translate([(thumbstick_mounthole_offset_x/2),-(thumbstick_mounthole_offset_y/2),box_top])
    cylinder(d=thumbstick_screw_d, h=thumbstick_standoff_length+1);
  translate([(thumbstick_mounthole_offset_x/2),(thumbstick_mounthole_offset_y/2),box_top])
    cylinder(d=thumbstick_screw_d, h=thumbstick_standoff_length+1);
}


module thumbstick_standoff() {
  
  difference() {
    translate([thumbstick_x, thumbstick_y, 0]) 
      cylinder(d=thumbstick_pillar_d, h=thumbstick_standoff_length+box_top);
    translate([thumbstick_x+thumbstick_hole_x_offset, thumbstick_y+thumbstick_hole_y_offset, thumbstick_easement]) 
      thumbstick_standoff_mountholes();
  }
}

module thumbstick_hole() {
  
  translate([thumbstick_x, thumbstick_y, -1])
    cylinder(d=thumbstick_hole_d, h=box_depth+2);
  translate([thumbstick_x, thumbstick_y, -0.001])
    cylinder(d1=thumbstick_hole_d+(thumbstick_easement*2), d2=thumbstick_hole_d, h=thumbstick_easement+1);
}

module thumbstick_groove() {
  groove_width = 14;
  groove_depth = 6;
  groove_length = (thumbstick_pillar_d-thumbstick_hole_d);//20;
  
  translate([thumbstick_x-(thumbstick_pillar_d/2)-1, thumbstick_y-(groove_width/2)+thumbstick_hole_y_offset, thumbstick_standoff_length+box_top-groove_depth+0.001])
    cube([groove_length, groove_width, groove_depth]);
}

module thumbstick_microswitch_cutout() {
  cutout_width = 12;
  cutout_depth = 6;
  cutout_inset = 10;
  //groove_length = (thumbstick_pillar_d-thumbstick_hole_d);//20;
  
  translate([thumbstick_x-(cutout_width/2)+thumbstick_hole_x_offset, thumbstick_y+(thumbstick_hole_d/2-(cutout_inset*0.5)), thumbstick_standoff_length+box_top-cutout_depth+0.001])
    cube([cutout_width, cutout_inset, cutout_depth]);
}

module shell() {
  difference() {
    solid_box();
  
    hull() {
      translate([box_height/2, box_height/2, box_top])
        cylinder(d=box_height-(box_wall*2), h=box_depth);
      translate([box_width-(box_height/2), box_height/2, box_top])
        cylinder(d=box_height-(box_wall*2), h=box_depth);
    }
  }
  thumbstick_standoff();
  charge_mount();
  esp32_mount();
  batt_mount();
}

module switch_cutout() {
  //translate([(box_width-switch_length)/2,-1,(box_depth-switch_width)/2])
  translate([(box_width-switch_length)/2,-1,(box_depth-switch_width-4)])
    cube([switch_length, box_wall+2, switch_width]);
}

module display_cutout() {
  //display_offset_x = (box_width-display_width)/2;
  display_offset_x = -9;
  display_offset_y = 14; 
  translate([(box_height/2)+display_offset_x,display_offset_y,-1])
  cube([display_slot_width, display_height, box_top + 2]);
}

 module charge_mount() { 
  plinth_x = charge_width + ((charge_clearance + charge_wall_thickness)*2); 
  plinth_y = charge_length + charge_clearance + charge_wall_thickness;
  plinth_z = charge_plinth_depth + charge_wall_depth + box_top;
  
  charge_x = thumbstick_x - (thumbstick_pillar_d/2) - plinth_x;
    
  translate([charge_x, box_wall-0.001, box_top])
    difference() {
      cube([plinth_x, plinth_y, plinth_z]);
      translate([charge_wall_thickness,0,charge_plinth_depth])
        cube([plinth_x-(charge_wall_thickness*2), plinth_y-(charge_wall_thickness), plinth_z]);
    }
}

module charge_usb_hole() {  
  plinth_x = charge_width + ((charge_clearance + charge_wall_thickness)*2); 
  charge_x = thumbstick_x - (thumbstick_pillar_d/2) - charge_wall_thickness - charge_usb_hole_width - 1;
  
  translate([charge_x,-1,charge_plinth_depth+box_top])
    cube([charge_usb_hole_width, box_wall+2, charge_usb_height]);
  
}

module esp32_mount_old() { 
  plinth_x = esp32_length + ((esp_clearance + esp_wall_thickness)); 
  plinth_y = esp32_width + ((esp_clearance + esp_wall_thickness)*2); 
  plinth_z = esp32_plinth_depth + esp32_wall_depth + box_top;
  
  translate([esp_x_off, (box_height - plinth_y - box_wall) - esp_y_off, box_top])
    difference() {
      cube([plinth_x, plinth_y, plinth_z]);
      translate([charge_wall_thickness,charge_wall_thickness+0.001,esp32_plinth_depth])
        cube([plinth_x-(charge_wall_thickness)+0.001, plinth_y-(charge_wall_thickness*2), plinth_z]);
    }
}

module esp32_usb_hole() {  
  esp32_width = 18;
  esp32_length = 23;
  esp32_xoffset = 6;
  
  plinth_x = esp32_width + ((esp_clearance + esp_wall_thickness)*2); 
  esp_x = thumbstick_x - (thumbstick_pillar_d/2) - plinth_x - esp32_xoffset;
  hole_x = esp_x + ((plinth_x - charge_usb_hole_width)/2);
  hole_y = box_height - box_wall - 1;
  
  translate([hole_x,hole_y,charge_plinth_depth+box_top])
    cube([charge_usb_hole_width, box_wall+2, charge_usb_height]);
  
}

module esp32_mount() { 
  esp32_width = 18;
  esp32_length = 23;
  esp32_xoffset = 6;
 
  plinth_x = esp32_width + ((esp_clearance + esp_wall_thickness)*2); 
  plinth_y = esp32_length + esp_clearance + esp_wall_thickness;
  plinth_z = charge_plinth_depth + charge_wall_depth + box_top;
  
  esp_x = thumbstick_x - (thumbstick_pillar_d/2) - plinth_x - esp32_xoffset;
  esp_y = box_height-plinth_y-box_wall+0.001;
    
  translate([esp_x, esp_y, box_top])
    difference() {
      cube([plinth_x, plinth_y, plinth_z]);
      translate([charge_wall_thickness,charge_wall_thickness+0.001,charge_plinth_depth])
        cube([plinth_x-(charge_wall_thickness*2), plinth_y-(charge_wall_thickness), plinth_z]);
    }
}

module batt_mount() {
  batt_length = 43; // strictly speaking, 40
  batt_diam = 13.5; // strictly speaking, 13
  
  batt_wall_thickness = 1;
  batt_x_offset = 5;
  batt_y_offset = 4;
  
  plinth_y = batt_length + (batt_wall_thickness*2); 
  plinth_x = batt_diam + (batt_wall_thickness*2); 
  plinth_z = batt_diam + box_top;
  
  batt_x = box_height/2;
  batt_y = (box_height-plinth_y)/2;
  
  //translate([esp_x_off, (box_height - plinth_y - box_wall) - esp_y_off, box_top])
  translate([batt_x, batt_y, 0])
    difference() {
      cube([plinth_x, plinth_y, plinth_z]);
      translate([batt_wall_thickness,batt_wall_thickness,0.001])
        cube([plinth_x-(batt_wall_thickness*2), plinth_y-(batt_wall_thickness*2), plinth_z]);
    }
}

module controller_screwholes() {
//  lid_screwhole_d = 3;
//  lid_screwhole_dist = 40;
//  lid_screwhole_edge = 5;
  
  x_off = (box_width - lid_screwhole_dist) / 2;
  translate([x_off, -1, box_depth-lid_screwhole_edge])
    rotate([-90,0,0])
      cylinder(d=lid_screwhole_d, h=box_height+2);
  translate([x_off+lid_screwhole_dist, -1, box_depth-lid_screwhole_edge])
    rotate([-90,0,0])
      cylinder(d=lid_screwhole_d, h=box_height+2);
}

module controller_body() {
  difference() {
    shell(); // the controller body
    switch_cutout(); // power switch
    thumbstick_hole(); // thumbstick hole
    thumbstick_groove(); // cable management groove
    thumbstick_microswitch_cutout(); // cutout so the microswitch doesn't foul the alignment
    display_cutout(); // screen hole
    charge_usb_hole(); // charge port USB
    esp32_usb_hole(); // hole for programming ESP32-C3
    controller_screwholes(); // screwholes for attaching the lid
  }
}


// **********************************************************************
// Lid
// **********************************************************************

module lid_screwholes() {
//  lid_screwhole_d = 3;
//  lid_screwhole_dist = 40;
//  lid_screwhole_edge = 5;
  
  x_off = (box_width - lid_screwhole_dist) / 2;
  translate([x_off, -1, lid_thickness+lid_screwhole_edge])
    rotate([-90,0,0])
      cylinder(d=lid_screwhole_d, h=box_height+2);
  translate([x_off+lid_screwhole_dist, -1, lid_thickness+lid_screwhole_edge])
    rotate([-90,0,0])
      cylinder(d=lid_screwhole_d, h=box_height+2);
}

module lid_screwhole_catchers() {
//  lid_screwhole_d = 3;
//  lid_screwhole_dist = 40;
//  lid_screwhole_edge = 5;
  
  x_off = (box_width - lid_screwhole_dist) / 2;
  translate([x_off-(lid_rim_depth/2), (box_wall+lid_slop+lid_rim_thickness-0.001), lid_thickness])
    cube([lid_rim_depth, lid_rim_depth, lid_rim_depth]);
  translate([x_off-(lid_rim_depth/2), box_height-lid_rim_depth-box_wall-lid_slop-lid_rim_thickness+0.001, lid_thickness])
    cube([lid_rim_depth, lid_rim_depth, lid_rim_depth]);
  translate([x_off-(lid_rim_depth/2)+lid_screwhole_dist, (box_wall+lid_slop+lid_rim_thickness-0.001), lid_thickness])
    cube([lid_rim_depth, lid_rim_depth, lid_rim_depth]);
  translate([x_off-(lid_rim_depth/2)+lid_screwhole_dist, box_height-lid_rim_depth-box_wall-lid_slop-lid_rim_thickness+0.001, lid_thickness])
    cube([lid_rim_depth, lid_rim_depth, lid_rim_depth]);
}

module solid_lid() {  
  rim_od = box_height - (box_wall*2) - (lid_slop*2);
  rim_id = rim_od - (lid_rim_thickness*2);
  
  // base
  hull() {
    translate([box_height/2, box_height/2, 0])
      cylinder(d=box_height, h=lid_thickness);
    translate([box_width-(box_height/2), box_height/2, 0])
      cylinder(d=box_height, h=lid_thickness);
  }
  
  // rim
  difference() {
    hull() {
      translate([box_height/2, box_height/2, 0])
        cylinder(d=rim_od, h=lid_thickness+lid_rim_depth);
      translate([box_width-(box_height/2), box_height/2, 0])
        cylinder(d=rim_od, h=lid_thickness+lid_rim_depth);
    }
    hull() {
      translate([box_height/2, box_height/2, -1])
        cylinder(d=rim_id, h=lid_thickness+lid_rim_depth+2);
      translate([box_width-(box_height/2), box_height/2, -1])
        cylinder(d=rim_id, h=lid_thickness+lid_rim_depth+2);
    }
  }
  
  // screwhole catchers
  lid_screwhole_catchers();
}

module lid_switch_cutout() {
  translate([(box_width-switch_length-8)/2,-1,lid_thickness])
    cube([switch_length+8, box_wall+lid_rim_thickness+2, switch_width]);
}

module lid() {
  difference() {
    solid_lid();
    lid_screwholes();
    // cutout for switch
    lid_switch_cutout();
  }
}
controller_body();
//lid();






