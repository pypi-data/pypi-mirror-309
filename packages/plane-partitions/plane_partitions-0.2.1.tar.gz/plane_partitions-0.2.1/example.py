import plane_partitions
from pprint import pprint

print(plane_partitions.version())
print()
print(plane_partitions.sspp_tp_tspp([[0, 0], [0, 0]]))

print(plane_partitions.sspp_tp_tspp([[1, 0], [0, 0]]))

print(plane_partitions.sspp_tp_tspp([[2, 0], [0, 0]]))

print(plane_partitions.sspp_tp_tspp([[2, 1], [0, 0]]))

print(plane_partitions.sspp_tp_tspp([[2, 1], [1, 0]]))

print()

print(plane_partitions.to_tikz_diagram([[2, 1], [1, 0]]))

print()

part = [[0,0,0],[0,0,0],[0,0,0]]
pprint(plane_partitions.rowmotion_orbit(part))
print()
for i in range(8):
    print(part, plane_partitions.complement(part))
    part = plane_partitions.rowmotion(part)

print()

print(plane_partitions.is_plane_partition([[0, 1],[0,0]]))
