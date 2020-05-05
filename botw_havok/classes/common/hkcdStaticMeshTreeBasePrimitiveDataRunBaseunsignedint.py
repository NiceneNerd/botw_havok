from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8, UInt32
from .hkObject import hkObject

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticMeshTreeBasePrimitiveDataRunBaseunsignedint(hkObject):
    value: UInt32
    index: UInt8
    count: UInt8

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.value = br.read_uint32()
        self.index = br.read_uint8()
        self.count = br.read_uint8()

        br.align_to(4)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint32(self.value)
        bw.write_uint8(self.index)
        bw.write_uint8(self.count)

        bw.align_to(4)

    def asdict(self):
        return {
            "value": self.value,
            "index": self.index,
            "count": self.count,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.value = d["value"]
        inst.index = d["index"]
        inst.count = d["count"]

        return inst
