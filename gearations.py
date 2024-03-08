import cadquery as cq
import math

tipDia = 2.6
toTip = 3.6 - 1.3
baseWidth = 3
gapWidth = 3.16
gapHeight = 1.6

shaftRad = 5
pinRad = 2
pinHeight = 3.2
clearance = 0.4

gearThickness = 5.2

bw2 = baseWidth / 2
tr2 = tipDia/2
gw2 = gapWidth/2

def polarPoint(t, r):
    return (math.cos(t) * r, math.sin(t) * r)

def addPolarPoint(wp, t, r):
    x = math.cos(t) * r
    y = math.sin(t) * r
    wp = wp.lineTo(x,y)
    return wp

def simpleTooth(wp, theta, gearRad, toothTheta, taperTheta):
    tB = theta - (toothTheta/4) - taperTheta
    rB = gearRad + (toTip - tr2)
    wp = addPolarPoint(wp, tB, rB)
    
    tC = theta - (toothTheta/4)
    rC = gearRad + toTip
    #wp = addPolarPoint(wp, tC, rC)
    
    tD = theta - (toothTheta/4) + taperTheta
    rD = gearRad + (toTip - tr2)
    #wp = addPolarPoint(wp, tD, rD)
    
    wp = wp.threePointArc(polarPoint(tC, rC),polarPoint(tD, rD))
    
    tE = theta
    rE = gearRad
    wp = addPolarPoint(wp, tE, rE)
    
    tF = theta + (toothTheta/4)
    rF = gearRad - gapHeight
    #wp = addPolarPoint(wp, tF, rF)
    
    tG = theta + (toothTheta/2)
    rG = gearRad
    #wp = addPolarPoint(wp, tG, rG)
    wp = wp.threePointArc(polarPoint(tF, rF), polarPoint(tG, rG))

    return wp

def gear(numTeeth):
    # numTeeth = 20
    toothTheta = (math.pi * 2) / numTeeth
    circumference = (baseWidth + gapWidth) * numTeeth
    gearRad = circumference / (2 * math.pi)
    taperTheta = math.asin(tr2/(gearRad + (toTip - tr2)))

    fpT = 0 + toothTheta/2
    fpR = gearRad
    
    gear = cq.Workplane("XY")
    gear = gear.moveTo(math.cos(fpT) * fpR, math.sin(fpT) * fpR)
    for i in range(numTeeth):
        t = (math.pi * 2) / numTeeth
        gear = simpleTooth(gear, t * (i+1), gearRad, toothTheta, taperTheta)
    gear = gear.close()
    gear = gear.extrude(gearThickness)
    
    shaft = cq.Workplane("XY").circle(shaftRad + clearance).extrude(10)
    
    gear = gear.cut(shaft)
    
    return gear

baseHeight = 6.3
magnetHeight = 3
magnetDia = 25

def base():
    base = cq.Workplane("XY")
    base = base.circle(16).extrude(baseHeight-1)
    
    shaft = cq.Workplane("XY")
    base = base.circle(shaftRad).extrude((baseHeight -1)/2 + gearThickness + 0.4)
    
    magnet = cq.Workplane("XY")
    magnet = magnet.circle(magnetDia/2 + clearance).extrude(magnetHeight)
    
    
    
    #show_object(magnet)
    
    base = base.cut(magnet)
    
    return base

def cap():
    cap = cq.Workplane("XY")
    cap = cap.circle(shaftRad * 1.5).extrude(1.6)
    cap = cap.edges(">Z or <Z").fillet(0.4)
    cap = cap.circle(pinRad).extrude(-0.8 - pinHeight)
    return cap

b = base()
b = b.translate((0,0,1))
#show_object(b)

g = gear(20)
g = g.translate((0,0,baseHeight))
#show_object(g)

c = cap()
c = c.translate((0,0,0))
show_object(c)

# cq.exporters.export(g, "gear_20.stl")
# cq.exporters.export(gear(10), "gear_10.stl")
# cq.exporters.export(gear(32), "gear_32.stl")




