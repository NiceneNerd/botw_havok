from ..binary import BinaryReader, BinaryWriter
from ..util import Vector4
from .base import HKBase
from .common.hkpConvexShape import hkpConvexShape

if False:
    from ..hk import HK


class hkpCapsuleShape(HKBase, hkpConvexShape):
    vertexA: Vector4
    vertexB: Vector4

    def deserialize(self, hk: "HK", obj):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(self.hkobj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpConvexShape.deserialize(self, hk, br, obj)
        br.align_to(16)

        self.vertexA = br.read_vector4()
        self.vertexB = br.read_vector4()

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpConvexShape.serialize(self, hk, bw, self.hkobj)
        bw.align_to(16)

        bw.write_vector4(self.vertexA)
        bw.write_vector4(self.vertexB)

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = HKBase.asdict(self)
        d.update(hkpConvexShape.asdict(self))
        d.update({"vertexA": self.vertexA.asdict(), "vertexB": self.vertexB.asdict()})

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBase.fromdict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.fromdict(d).__dict__)

        inst.vertexA = Vector4.fromdict(d["vertexA"])
        inst.vertexB = Vector4.fromdict(d["vertexB"])

        return inst
