/******************************************************************
RoboFootball
(C) 2024 by Adam Oellermann <adam@oellermann.com>

This file is part of RoboFootball.

RoboFootball is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

RoboFootball is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with RoboFootball. If not, see <https://www.gnu.org/licenses/>.
-------------------------------------------------------------------
tyre_v2.scad
Parametric tyre for RoboFootball robots
/******************************************************************/
$fa = 1;
$fs = 0.4;

// PARAMETERS
tyre_od = 40;
tyre_stretch = tyre_od/20; // make the tyre stretch-fit onto the wheel
tyre_thickness = 6;
tyre_id_nominal = tyre_od - (tyre_thickness*2);
tyre_id = tyre_id_nominal - tyre_stretch;
wheel_od = tyre_id_nominal + tyre_stretch;

wheelwidth = 15;

knobble_radius = 2.5; // the size of the circles that make the knobbles
knobble_count = 40;
knobble_twist = 15;

mould_wall_thickness = 1;
mould_base_thickness = 2;
mould_top_overlap = 2;
mould_od = tyre_od + (mould_wall_thickness*2);
mould_pin_diameter = 8;
mould_pin_length = mould_base_thickness+5;
mould_pin_slop = 0.2;
mould_pin_easement = 0.6; // taper for the locating pin

// studs
stud_diam_max = 4;
stud_diam_min = 1;
stud_length = 5;
stud_count = 5;

module tyre_outer_profile() {
  circle(d=tyre_od-(knobble_radius*2));
  
  r = (tyre_od/2) - knobble_radius;
  angle = 360/knobble_count;
  for (i=[0:angle:360]) {
    translate([r*sin(i), r*cos(i)])
      circle(r=knobble_radius);
  }
}

module tyre() {
  linear_extrude(height=wheelwidth/2, twist=knobble_twist) {
    tyre_outer_profile();
  }
  translate([0,0,wheelwidth-0.001]) 
    mirror([0,0,1])
    linear_extrude(height=wheelwidth/2, twist=knobble_twist) {
      tyre_outer_profile();
    }

}

module mould_base() {
  
  difference() {
    union() {
      cylinder(d=mould_od + mould_top_overlap, h=mould_base_thickness);
      cylinder(d=mould_od, h=wheelwidth+mould_base_thickness);
    }
    
    // cut out the tyre
    translate([0,0,mould_base_thickness+0.01])
      tyre();
    
    // cut out the locator pin
    translate([0,0,-0.5])
      cylinder(d=mould_pin_diameter+mould_pin_slop, h=mould_base_thickness+1);
  }
  
}


module stud() {
  offset = (tyre_id/2) - tyre_stretch/2;
  translate([0,offset,wheelwidth/2+mould_base_thickness])
  rotate([-90,0,0])
    cylinder(d1=stud_diam_max,d2=stud_diam_min,h=stud_length);
}

module studs() {
  
  angle = 360/stud_count;
  for(i=[1:1:5]) {
    rotate([0,0,i*angle])
      stud();
  }
}


module mould_top() {
  // base 
  cylinder(d=mould_od + mould_top_overlap, h=mould_base_thickness);
  // wheel inner
  cylinder(d=tyre_id, h=mould_base_thickness+wheelwidth);
  // locator pin 
  translate([0,0,mould_base_thickness+wheelwidth-0.01])
    cylinder(d1=mould_pin_diameter,d2=mould_pin_diameter-mould_pin_easement, h=mould_pin_length);
  studs();
}

mould_base();
//mould_top();