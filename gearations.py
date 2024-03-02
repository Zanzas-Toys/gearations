import cadquery as cq
import math

tipDia = 2.6
toTip = 3.6 - 1.3
baseWidth = 3
gapWidth = 3.16
gapHeight = 1.6
gearThickness = 3.2 # 5.2

bw2 = baseWidth / 2
tr2 = tipDia/2
gw2 = gapWidth/2
offsetX = (baseWidth + gapWidth) * -0.5


result = (
    cq.Sketch()
    .segment((0.0, 0), (0.0, 2.0))
    .segment((2.0, 0))
    .close()
    .arc((0.6, 0.6), 0.4, 0.0, 360.0)
    .assemble(tag="face")
    .edges("%LINE", tag="face")
    .vertices()
    .chamfer(0.2)
)

tooth = (
    cq.Workplane("XZ")
    #.center(offsetX,0)
    .moveTo(-bw2, 0)
    .lineTo(-tr2, toTip-tr2)
    .threePointArc((0,toTip),(tr2,toTip-tr2))
    .lineTo(tr2,0)
    .threePointArc((bw2+gw2,-gapHeight),(bw2+gapWidth,0))
    .close()
)

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
    
    
    
    return gear

g = gear(20)
show_object(g)


# cq.exporters.export(g, "gear_20.stl")
# cq.exporters.export(gear(10), "gear_10.stl")
# cq.exporters.export(gear(32), "gear_32.stl")




