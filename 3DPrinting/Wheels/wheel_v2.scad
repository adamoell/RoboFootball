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
wheel_v2.scad
Parametric wheel for RoboFootball robots
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

//wheel_od = 40; // the outside diameter of the wheel
rim_thickness = 1.6; // the overall thickness of the rim
tooth_depth = 0.5; // the depth of the "teeth" that grip the wheel

points = 60; // the number of teeth

hubradius = 4.2;
spokes = 3; // was 5
spokewidth = 1.6; // was 1.2
shaftoffset = 0.8; // spacer to ensure wheel doesn't bind;
shaftlength = 7.5;
shaftwasher = 0.6;

shaft_diam = 5.4;
solid_diam = 3.7;
tolerance = 0.3;

wheel_outer_radius = wheel_od/2;
rimradius = wheel_outer_radius - rim_thickness; //23.5; // the inside edge of the 'tyre'
inradius = wheel_outer_radius-tooth_depth; // the inside of the 'zigzags' that hold the rubber band
outradius = wheel_outer_radius; // the outside of the 'zigzags' that hold the rubber band
steps = points * 2;

// studs
stud_diam_max = 4;
stud_diam_min = 1;
stud_length = 5;
stud_count = 5;

module wheel_unmounted() {
    function getangle(point, steps) = point * (360/steps);
    function getradius(point) = ((point % 2) == 0) ? outradius : inradius;
    function getx(point, steps) = getradius(point) * cos(getangle(point, steps));
    function gety(point, steps) = getradius(point) * sin(getangle(point, steps));

    // the zigzag outline
    polypoints = [for (i=[0:1:steps]) [getx(i, steps), gety(i, steps)]  ];
       

    linear_extrude(height=wheelwidth) {
        difference() { // cutout for shaft
            union() {
                circle(r=hubradius); // the hub
                // spokes
                for (i=[0:1:spokes-1]) {
                    angle = i * (360/spokes);
                    rotate([0,0,angle])
                        translate([0,inradius/2,0])
                        square(size=[spokewidth,inradius], center=true);
                }
                difference() {    
                    //polygon(polypoints); // zigzaggy outline
                    circle(r=wheel_outer_radius);
                    circle(r=rimradius); // cutout for open wheel
                }
            }
            //shaft(); // cutout for shaft
        }
    }
    // this pushes the wheel out slightly to prevent rubbing
    shaft_offset();
}

module shaft_offset() {
  linear_extrude(height=wheelwidth+shaftoffset) {
    difference() {
      circle(r=hubradius); // the hub
      //shaft();
    }
      
  }
}

module shaft_clearer() {
  total_width = wheelwidth + shaftoffset;
  clearance = total_width - shaftlength;
  translate([0,0,-0.1]) 
    cylinder(d=shaft_diam+tolerance,h=clearance+0.1) ;
}
module shaft_washer() {
  total_width = wheelwidth + shaftoffset;
  z = total_width - shaftlength - shaftwasher;
  translate([0,0,z]) 
    difference() {
      cylinder(d=shaft_diam+1,h=shaftwasher) ;
      // hole for M2 self-tapper
      translate([0,0,-0.05])
      cylinder(d=2,h=shaftwasher+0.1) ;
    }
}

module shaft() {
    shaftradius = shaft_diam/2;
    solidwidth = solid_diam/2;
    
    sr = shaftradius + tolerance/2;
    sw = solidwidth + tolerance/2;
    difference() {
        circle(r=sr);
        translate([0,sr*2 - sw/2,0])
            square(sr*2, center=true);
        translate([0,-sr*2 + sw/2,0])
            square(sr*2, center=true);
    }
}

module n20_shaft_profile() {
  n20_shaft_d = 3.3; // was 3, 3.2 too tight, 3.4 too loose
  n20_shaft_reducer = .5;
  
  difference() {
    circle(d=n20_shaft_d);
    translate([-n20_shaft_d/2, (n20_shaft_d/2)-n20_shaft_reducer])
      square([n20_shaft_d, n20_shaft_d]);
  }
}

module n20_shaft() {
  n20_shaft_length = 10;
  n20_shaft_clearance = 1;
  n20_easement_depth = 2;
  n20_easement_scale = 1.3;
  
  translate([0,0,-0.001]) {
    // shaft
    linear_extrude(height=n20_shaft_length-n20_shaft_clearance)
      n20_shaft_profile();
    
    // easement
    hull() {
      linear_extrude(height=0.001)
        scale([n20_easement_scale,n20_easement_scale])
          n20_shaft_profile();
      translate([0,0,n20_easement_depth]) 
      linear_extrude(height=0.001)
        n20_shaft_profile();
    }
  }
}

module wheel() {
  difference() {
    wheel_unmounted();
    //shaft_clearer();
    translate([0,0,wheelwidth+shaftoffset+0.001])
      mirror([0,0,1])
        n20_shaft();
  }

  //shaft_washer();
  studs();
}

module stud() {
  
  
  offset = (wheel_od/2) - rim_thickness/2;
  translate([0,offset,wheelwidth/2])
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

//studs();
wheel();
