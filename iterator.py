import math
from IK import *


counter = 0


x = range(-30, 30, 5)
y = range(0, 120, 5)
z = range(0, 160, 5)

# print("X : " + str(len(x)) + " Y: " + str(len(y)) + " Z: " + str(len(z)))

fig = plt.figure(figsize=plt.figaspect(0.5))


# ===============
#  First subplot
# ===============
# set up the axes for the first plot
ax = fig.add_subplot(2, 2, 1, projection='3d')


solutionCounter = 0
noSolutionCounter = 0

solutionBufferX = []
solutionBufferY = []
solutionBufferZ = []

pointXBuffer = []
pointYBuffer = []
pointZBuffer = []


noSolutionXBuffer = []
noSolutionYBuffer = []
noSolutionZBuffer = []

for i in x:
    for j in y:
        for k in z:
            points = getIKPoint(i, j, k)
            if len(points):
                fkPoints = getFKFrame(math.radians(
                    points[0]), math.radians(points[1]), math.radians(points[2]))

                solutionBufferX.append(fkPoints[2][0][3])
                solutionBufferY.append(fkPoints[2][1][3])
                solutionBufferZ.append(fkPoints[2][2][3])

                pointXBuffer.append(i)
                pointYBuffer.append(j)
                pointZBuffer.append(k)
                solutionCounter += 1
            else:
                noSolutionXBuffer.append(i)
                noSolutionYBuffer.append(j)
                noSolutionZBuffer.append(k)
                noSolutionCounter += 1
                # print("No solution %d, %d, %d", (i, j, k))


surf = ax.plot(solutionBufferX, solutionBufferY, solutionBufferZ,  "o-",
               markerSize=2,
               markerFacecolor="orange",
               linewidth=0.2,
               color="red")

ax.set_title("Solution Space Space")
ax.set_xlim3d(-200, 200)
ax.set_ylim3d(-200, 200)
ax.set_zlim3d(-100, 200)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_axisbelow(True)


ax = fig.add_subplot(2, 2, 2, projection='3d')
ax.plot(pointXBuffer, pointYBuffer, pointZBuffer, "o-",
        markerSize=2,
        markerFacecolor="orange",
        linewidth=0.2,
        color="green")


ax.set_title("Trajectory  Space")
ax.set_xlim3d(-200, 200)
ax.set_ylim3d(-200, 200)
ax.set_zlim3d(-100, 200)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_axisbelow(True)


ax = fig.add_subplot(2, 2, 3, projection="3d")
ax.plot(noSolutionXBuffer, noSolutionYBuffer, noSolutionZBuffer, "o-",
        markerSize=2,
        markerFacecolor="orange",
        linewidth=0.2,
        color="orange")

ax.set_title("No Solution  Space")
ax.set_xlim3d(-200, 200)
ax.set_ylim3d(-200, 200)
ax.set_zlim3d(-100, 200)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_axisbelow(True)
print("Solutions: " + str(solutionCounter + noSolutionCounter) +
      " NoSols: " + str(noSolutionCounter) + " Sols: " + str(solutionCounter))

print("Solution Ratio: " + str(solutionCounter /
                               (noSolutionCounter + solutionCounter) * 100))
plt.show()
